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
    if total <= 0:
        current = total = 1
    percent = current / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r|{bar}| {percent:.2%}', end='\r')
    if current == total:
        print()

def help_for_ls() -> str:
    return (
        "Usage: ls [path]\n"
        "List files in the specified directory. If no path is provided, lists files in the current directory.\n"
        "Example: ls /home/user/documents\n"
    )

def help_for_cd() -> str:
    return (
        "Usage: cd [path]\n"
        "Change the current directory to the specified path.\n"
        "Example: cd /home/user/documents\n"
    )

def help_for_pwd() -> str:
    return (
        "Usage: pwd\n"
        "Print the current working directory on the FTP server.\n"
    )

def help_for_mkdir() -> str:
    return (
        "Usage: mkdir [path]\n"
        "Create a new directory at the specified path on the FTP server.\n"
        "Example: mkdir /home/user/new_folder\n"
    )

def help_for_rmdir() -> str:
    return (
        "Usage: rmdir [path]\n"
        "Remove the directory at the specified path on the FTP server.\n"
        "Example: rmdir /home/user/old_folder\n"
    )

def help_for_delete() -> str:
    return (
        "Usage: delete [file]\n"
        "Delete the specified file on the FTP server.\n"
        "Example: delete /home/user/file.txt\n"
    )

def help_for_rename() -> str:
    return (
        "Usage: rename [old_name] [new_name]\n"
        "Rename a file on the FTP server.\n"
        "Example: rename /home/user/old.txt /home/user/new.txt\n"
    )

def help_for_get() -> str:
    return (
        "Usage: get [file]\n"
        "Download the specified file from the FTP server.\n"
        "Example: get /home/user/file.txt\n"
    )

def help_for_put() -> str:
    return (
        "Usage: put [file]\n"
        "Upload the specified file to the FTP server.\n"
        "Example: put /home/user/file.txt\n"
    )

def help_for_mget() -> str:
    return (
        "Usage: mget [file1 file2 ...]\n or mget [*.txt]\n"
        "Download multiple files from the FTP server.\n"
        "Example: mget /home/user/file1.txt /home/user/file2.txt\n"
    )

def help_for_mput() -> str:
    return (
        "Usage: mput [file1 file2 ...]\n or mput [*.txt]\n"
        "Upload multiple files to the FTP server.\n"
        "Example: mput /home/user/file1.txt /home/user/file2.txt\n"
    )

def help_for_dput() -> str:
    return (
        "Usage: dput [directory]\n"
        "Upload a directory to the FTP server.\n"
        "Example: dput /home/user/my_folder\n"
    )

def help_for_dget() -> str:
    return (
        "Usage: dget [directory]\n"
        "Download a directory from the FTP server.\n"
        "Example: dget /home/user/my_folder\n"
    )

def help_for_transfer_mode() -> str:
    return (
        "Usage: ascii or binary\n"
        "Set the transfer mode to ASCII or binary.\n"
        "Example: ascii\n"
    )

def help_for_status() -> str:
    return (
        "Usage: status\n"
        "Show the current status of the FTP connection, including server response and current directory.\n"
    )

def help_for_passive() -> str:
    return (
        "Usage: passive\n"
        "Switch the FTP connection to passive mode.\n"
        "In passive mode, the client initiates the data connection.\n"
    )

def help_for_connect() -> str:
    return (
        "Usage: connect [host] [port]\n"
        "Connect to the specified FTP server.\n"
        "Example: connect ftp.example.com 21\n"
        "Input: IP address and port number of the FTP server.\n"
        "If no host or port is provided, it uses the default values from the configuration.\n"
        "Input: Username and password for authentication (if required).\n"
        "if no username or password is provided, it uses the default values from the configuration.\n"
    )

def help_for_disconnect() -> str:
    return (
        "Usage: disconnect\n"
        "Disconnect from the current FTP server.\n"
        "This command closes the control connection and any data connections.\n"
        "If you are not connected to any server, it will simply return without action.\n"
    )

def help_for_quit() -> str:
    return (
        "Usage: quit\n"
        "Exit the FTP client.\n"
    )
