import subprocess
import socket
import os
from ftp_config import ftpconfig

def scan_file(file_path):
    result = subprocess.run(['clamscan', file_path], capture_output=True, text=True)
    print('[ClamAV Agent] Scan completed')
    if (result.returncode == 2):
        return "Error: ClamAV encountered an error while scanning."
    elif (result.returncode == 1):
        return "INFECTED" 
    else:
        return "OK"

def main():
    try:
        create_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clamav_agent')
        os.makedirs(create_directory, exist_ok=True)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((ftpconfig.clamav_host, ftpconfig.clamav_port))
            server_socket.listen(1)
            try:
                connect, addr = server_socket.accept()
                print(f"[ClamAV Agent] Connection from {addr}")

                with connect:
                    filename_size = int.from_bytes(connect.recv(4), 'big')
                    filename = connect.recv(filename_size).decode('utf-8')

                    file_size = int.from_bytes(connect.recv(8), 'big')
                    bytes_received = 0
                    filepath = os.path.join(filename)

                    with open(filepath, 'wb') as f:
                        while bytes_received < file_size:
                            remaining = file_size - bytes_received
                            chunk_size = min(ftpconfig.buffer_size, remaining)
                            data = connect.recv(chunk_size)
                            if not data:
                                break
                            f.write(data)
                            bytes_received += len(data)

                    connect.sendall(b'OK') 
                    
                    result = scan_file(filepath)
                    connect.sendall(result.encode('utf-8'))
                    connect.close()
            except Exception as e:
                raise OSError(f"[ClamAV Agent] Error handling connection: {e}")                    
    except OSError as e:
        raise OSError(f"[ClamAV Agent] Error: {e}")

if __name__ == "__main__":
    main()