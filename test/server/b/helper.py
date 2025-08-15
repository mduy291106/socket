import socket
from ftp_config import ftpconfig

def receive_response(sock: socket.socket) -> str:
    response = sock.recv(ftpconfig.buffer_size).decode('utf-8', errors='ignore')
    if not response:
        raise Exception("Connection closed by the server")
    return response.strip()

def send_command(sock: socket.socket, command: str) -> None:
    sock.sendall(command.encode('utf-8') + b'\r\n')
    response = receive_response(sock)
    return response.strip()

def size_command(control_socket: socket.socket, filename: str) -> int:
    control_socket.sendall(f'SIZE {filename}\r\n'.encode())
    response = control_socket.recv(1024).decode()
    if response.startswith("213"):
        size = int(response.split()[1])
        return size
    else:
        return None

def progress_bar(current: int, total: int, length: int = 50) -> None:
    percent = current / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r|{bar}| {percent:.2%}', end='\r')
    if current == total:
        print()