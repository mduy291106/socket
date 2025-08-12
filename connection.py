import socket
import ssl
import subprocess
import os
import time
import threading
import side_function
from ftp_config import ftpconfig

def scan_for_virus(file_path, server_ip=ftpconfig.clamav_host, port=ftpconfig.clamav_port):
    process = subprocess.Popen(['python', 'clamav.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    client = socket.socket()
    try:
        client.settimeout(ftpconfig.timeout)  
        client.connect((ftpconfig.clamav_host, ftpconfig.clamav_port))
        client.settimeout(None)
    except socket.timeout:
        print(f"[Client] Connection timeout to clamav agent {server_ip}:{port}")
        client.close()
        return None
    except socket.error as e:
        print(f"[Client] Failed to connect to clamav agent: {e}")
        client.close()
        return None

    print("[Client] Connected to clamav agent.")

    if file_path is None or not os.path.isfile(file_path):
        print(f"[Client] File does not exist: {file_path}")
        client.close()
        return None

    filename = os.path.basename(file_path)
    client.sendall(len(filename).to_bytes(4, 'big'))  
    client.sendall(filename.encode('utf-8'))
    print("[Client] Sent filename:", filename)

    file_size = os.path.getsize(file_path)
    client.sendall(file_size.to_bytes(8, 'big'))  

    with open(file_path, 'rb') as f:
        while (data := f.read(ftpconfig.buffer_size)):
            client.sendall(data)

    reply = client.recv(1024)
    if reply != b'OK':
        print(f"[Client] Failed to send file {filename} to ClamAV agent.")
        client.close()
        return None
    print(f"[ClamAV Agent] Received file: {filename}")

    scanning, animation_thread = wait_for_scan()
    scan_result = client.recv(1024)
    client.close()
    scanning[0] = False
    animation_thread.join(timeout=0.1)
    process.terminate()
    return scan_result.decode('utf-8')
    
def wait_for_scan():
    scanning = [True]
    def animate_scan():
        chars = "⋅⋅⋅⋅⋅•••••"
        idx = 0
        while scanning[0]:
            print(f'\r[ClamAV Agent] Scanning, please wait {chars[idx % len(chars)]}{chars[(idx + 1) % len(chars)]}{chars[(idx + 2) % len(chars)]}{chars[(idx + 3) % len(chars)]}{chars[(idx + 4) % len(chars)]}\r', end='', flush=True)
            idx -= 1
            time.sleep(0.2)           

    animation_thread = threading.Thread(target=animate_scan)
    animation_thread.daemon = True
    animation_thread.start()

    return scanning, animation_thread

def create_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

def create_control_socket(ip: str = ftpconfig.host, port: int = ftpconfig.port, user: str = ftpconfig.username, password: str = ftpconfig.password) -> socket.socket:
    try:
        ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ctrl_sock.settimeout(ftpconfig.timeout)
        ctrl_sock.connect((ip, port))
    except socket.timeout:
        print(f"Connection timeout to FTP server {ip}:{port}")
        return None
    except socket.error as e:
        print(f"Socket error: {e}")
        return None
    ftp_ctrl = side_function.receive_response(ctrl_sock)
    if not ftp_ctrl.startswith('220'):
        print(f"Failed to connect: {ftp_ctrl}")
        return None
    if ftpconfig.use_ssl:
        ftp_ctrl = side_function.send_command(ctrl_sock, f"AUTH TLS")
        if not ftp_ctrl.startswith('234'):
            print(f"Failed to start TLS: {ftp_ctrl}")
            return None
        ctrl_sock = context.wrap_socket(ctrl_sock, server_hostname=ftpconfig.host)
        ftp_ctrl = side_function.send_command(ctrl_sock, "PBSZ 0")
        if not ftp_ctrl.startswith('200'):
            print(f"Failed to set protection buffer size: {ftp_ctrl}")
            return None
        ftp_ctrl = side_function.send_command(ctrl_sock, "PROT P")
        if not ftp_ctrl.startswith('200'):
            print(f"Failed to set data channel protection: {ftp_ctrl}")
            return None
    ftp_ctrl = side_function.send_command(ctrl_sock, f"USER {user}")
    if not ftp_ctrl.startswith('331'):
        print(f"User authentication failed: {ftp_ctrl}")
        return None
    ftp_ctrl = side_function.send_command(ctrl_sock, f"PASS {password}")
    if not ftp_ctrl.startswith('230'):
        print(f"Password authentication failed: {ftp_ctrl}")
        return None
    return ctrl_sock

def create_data_socket_active(control_socket: socket.socket, command: str) -> socket.socket:
    listen_sock = None
    data_sock = None
    try:
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_sock.settimeout(ftpconfig.timeout)
        listen_sock.bind(('', 0))
        listen_sock.listen(1)
        
        ip = control_socket.getsockname()[0]
        port = listen_sock.getsockname()[1]
        port_cmd = f"PORT {ip.replace('.', ',')},{port // 256},{port % 256}"

        response = side_function.send_command(control_socket, port_cmd)
        if not response.startswith('200'):
            print(f"Failed to set PORT mode: {response}")
            return None

        response = side_function.send_command(control_socket, command)
        if not response.startswith('150') and not response.startswith('125'):
            print(f"Failed to retrieve file: {response}")
            return None

        data_sock, addr = listen_sock.accept()
        data_sock.settimeout(ftpconfig.timeout)
        
        if ftpconfig.use_ssl:
            data_sock = context.wrap_socket(data_sock, server_hostname=control_socket.getsockname()[0], session=control_socket.session)
        
        listen_sock.close()
        return data_sock
        
    except socket.timeout:
        print(f"[Client] Timeout while creating active data connection")
        if listen_sock:
            listen_sock.close()
        if data_sock:
            data_sock.close()
        print("Active data connection timeout")
        return None
    except socket.error as e:
        print(f"[Client] Socket error in active mode: {e}")
        if listen_sock:
            listen_sock.close()
        if data_sock:
            data_sock.close()
        print(f"Active data connection failed: {e}")
        return None
    except Exception as e:
        if listen_sock:
            listen_sock.close()
        if data_sock:
            data_sock.close()
        print(f"[Client] Error creating active data connection: {e}")
        return None

def create_data_socket_passive(control_socket: socket.socket, command: str) -> socket.socket:
    data_sock = None
    try:
        control_socket.sendall(b"PASV\r\n")
        response = side_function.receive_response(control_socket)
        if not response.startswith('227'):
            print(f"Failed to enter passive mode: {response}")
            return None

        parts = response.split('(')[1].split(')')[0].split(',')
        ip = '.'.join(parts[:4])
        port = int(parts[4]) * 256 + int(parts[5])  
        
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.settimeout(ftpconfig.timeout)
        data_sock.connect((ip, port))
        
        if ftpconfig.use_ssl:
            data_sock = context.wrap_socket(data_sock, server_hostname=control_socket.getpeername()[0], session=control_socket.session)

        response = side_function.send_command(control_socket, command)
        if not response.startswith('150') and not response.startswith('125'):
            print(f"Failed to execute command: {response}")
            return None

        return data_sock
        
    except socket.timeout:
        print(f"[Client] Timeout while creating passive data connection")
        if data_sock:
            data_sock.close()
        print("Passive data connection timeout")
        return None
    except socket.error as e:
        print(f"[Client] Socket error in passive mode: {e}")
        if data_sock:
            data_sock.close()
        print(f"Passive data connection failed: {e}")
        return None
    except Exception as e:
        if data_sock:
            data_sock.close()
        print(f"[Client] Error creating passive data connection: {e}")
        return None

def open_control_connection(ip: str = ftpconfig.host, port: int = ftpconfig.port, user: str = ftpconfig.username, password: str = ftpconfig.password) -> socket.socket:
    if ftpconfig.use_ssl:
        global context
        context = create_context()
    control_socket = create_control_socket(ip, port, user, password)
    return control_socket

def close_control_connection(control_socket: socket.socket):
    if control_socket:
        control_socket.sendall(b"QUIT\r\n")
        response = side_function.receive_response(control_socket)
        if not response.startswith('221'):
            print(f"Failed to close control connection: {response}")
        control_socket.close()
        print("[Client] Control connection closed.")