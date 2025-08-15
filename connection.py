import socket
import ssl
import subprocess
import os
import time
import threading
from ftp_config import ftpconfig

def scan_for_virus(file_path, server_ip=ftpconfig.clamav_host, port=ftpconfig.clamav_port):
    process = subprocess.Popen(['python', 'C:\\Users\\mduy\\source\\repos\\socket\\clamav.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_socket.settimeout(ftpconfig.timeout)
        control_socket.connect((ip, port))
    except socket.timeout:
        print(f"Connection timeout to FTP server {ip}:{port}")
        return None
    except socket.error as e:
        print(f"Socket error: {e}")
        return None
    
    response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')

    if not response.startswith('220'):
        print(f"Failed to connect: {response}")
        return None
    
    if ftpconfig.use_ssl:
        control_socket.sendall(b"AUTH TLS\r\n")
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('234'):
            print(f"Failed to start TLS: {response}")
            return None
        
        control_socket = context.wrap_socket(control_socket, server_hostname=ftpconfig.host)
        control_socket.sendall(b"PBSZ 0\r\n")
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('200'):
            print(f"Failed to set protection buffer size: {response}")
            return None
        
        control_socket.sendall(b"PROT P\r\n")
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('200'):
            print(f"Failed to set data channel protection: {response}")
            return None
        
        ftpconfig.is_quit = False
        
    control_socket.sendall(f"USER {user}\r\n".encode('utf-8'))
    response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
    if not response.startswith('331'):
        print(f"User authentication failed: {response}")
        return None
    
    control_socket.sendall(f"PASS {password}\r\n".encode('utf-8'))
    response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
    if not response.startswith('230'):
        print(f"Password authentication failed: {response}")
        return None
    
    return control_socket

def create_data_socket_active(control_socket: socket.socket, command: str) -> socket.socket:
    listen_socket = None
    data_socket = None
    try:
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.settimeout(ftpconfig.timeout)
        listen_socket.bind(('', 0))
        listen_socket.listen(1)
        
        ip = control_socket.getsockname()[0]
        port = listen_socket.getsockname()[1]
        port_command = f"PORT {ip.replace('.', ',')},{port // 256},{port % 256}"

        control_socket.sendall(port_command.encode('utf-8') + b'\r\n')
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('200'):
            print(f"Failed to set PORT mode: {response}")
            return None

        control_socket.sendall(command.encode('utf-8') + b'\r\n')
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('150') and not response.startswith('125'):
            print(f"Failed to retrieve file: {response}")
            return None

        data_socket, address = listen_socket.accept()
        data_socket.settimeout(ftpconfig.timeout)
        
        if ftpconfig.use_ssl:
            data_socket = context.wrap_socket(data_socket, server_hostname=control_socket.getsockname()[0], session=control_socket.session)
        
        listen_socket.close()
        return data_socket
        
    except socket.timeout:
        print(f"[Client] Timeout while creating active data connection")
        if listen_socket:
            listen_socket.close()
        if data_socket:
            data_socket.close()
        print("Active data connection timeout")
        return None
    except socket.error as e:
        print(f"[Client] Socket error in active mode: {e}")
        if listen_socket:
            listen_socket.close()
        if data_socket:
            data_socket.close()
        print(f"Active data connection failed: {e}")
        return None
    except Exception as e:
        if listen_socket:
            listen_socket.close()
        if data_socket:
            data_socket.close()
        print(f"[Client] Error creating active data connection: {e}")
        return None

def create_data_socket_passive(control_socket: socket.socket, command: str) -> socket.socket:
    data_socket = None
    try:
        control_socket.sendall(b"PASV\r\n")
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('227'):
            print(f"Failed to enter passive mode: {response}")
            return None

        parts = response.split('(')[1].split(')')[0].split(',')
        ip = '.'.join(parts[:4])
        port = int(parts[4]) * 256 + int(parts[5])  
        
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.settimeout(ftpconfig.timeout)
        data_socket.connect((ip, port))
        
        if ftpconfig.use_ssl:
            data_socket = context.wrap_socket(data_socket, server_hostname=control_socket.getpeername()[0], session=control_socket.session)

        control_socket.sendall(command.encode('utf-8') + b'\r\n')
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('150') and not response.startswith('125'):
            print(f"Failed to execute command: {response}")
            return None

        return data_socket
        
    except socket.timeout:
        print(f"[Client] Timeout while creating passive data connection")
        if data_socket:
            data_socket.close()
        print("Passive data connection timeout")
        return None
    except socket.error as e:
        print(f"[Client] Socket error in passive mode: {e}")
        if data_socket:
            data_socket.close()
        print(f"Passive data connection failed: {e}")
        return None
    except Exception as e:
        if data_socket:
            data_socket.close()
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
        response = control_socket.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
        if not response.startswith('221'):
            print(f"Failed to close control connection: {response}")
        control_socket.close()
        ftpconfig.is_quit = True
        print("[Client] Control connection closed.")