import os
import socket
from ftp_config import ftpconfig, FTPMode
import connection
import side_function

def pwd(control_socket: socket.socket) -> str:
    try:
        response = side_function.send_command(control_socket, "PWD")
        if not response.startswith('257'):
            print(f"PWD command failed: {response}")
            return ""
        return response.split('"')[1]
    except Exception as e:
        print(f"[Client] Error getting current directory: {e}")
        return ""

def ls(control_socket: socket.socket, directory: str = '') -> str:
    if not pwd(control_socket):
        return []
    if ftpconfig.mode == FTPMode.PASSIVE:
        data_sock = connection.create_data_socket_passive(control_socket, "LIST " + directory)
    else:
        data_sock = connection.create_data_socket_active(control_socket, "LIST " + directory)
    data = b""
    while True:
        chunk = data_sock.recv(ftpconfig.buffer_size)
        if not chunk:
            break
        data += chunk
    if ftpconfig.use_ssl:
        data_sock.unwrap()
    data_sock.close()

    response = side_function.receive_response(control_socket)
    if not response.startswith('226'):
        print(f"LIST command failed: {response}")
        return ""
    return data.decode('utf-8', errors='ignore')

def cd(control_socket: socket.socket, path: str) -> bool:
    if not path:
        print("Path cannot be empty")
        return False
    try:
        response = side_function.send_command(control_socket, f"CWD {path}")
        if not response.startswith('250'):
            print(f"CWD command failed: {response}")
            return False
        current_path = pwd(control_socket)
        print(f"[Client] Changed directory to {current_path}")
        return True
    except Exception as e:
        print(f"[Client] Error changing directory: {e}")
        return False

def mkdir(control_socket: socket.socket, path: str) -> bool:
    if not path:
        print("Directory name cannot be empty")
        return False
    try:
        response = side_function.send_command(control_socket, f'MKD {path}')
        if not response.startswith('257'):
            print(f"MKD command failed: {response}")
            return False
        print(f"[Client] Created directory {path}")
        return True
    except Exception as e:
        print(f"[Client] Error creating directory: {e}")
        return False
    
def remove_directory_recursively(control_socket: socket.socket, path: str) -> bool:
    current_directory = pwd(control_socket)
    if not cd(control_socket, path):
        return False
    items = ls(control_socket).splitlines()
    if items is None:
        response = side_function.send_command(control_socket, f"RMD {path}")
        if not response.startswith('250'):
            print(f"RMD command failed: {response}")
            return False
        print(f"[Client] Removed directory {path}")
        return True

    for item in items:
        parts = item.split()
        name = parts[-1]

        if item.lower().startswith("d"):
            if not remove_directory_recursively(control_socket, name):
                cd(control_socket, current_directory)
                return False
        else:
            if not delete(control_socket, name):
                cd(control_socket, current_directory)
                return False

    print(pwd(control_socket)) 
    cd(control_socket, current_directory)

    response = side_function.send_command(control_socket, f"RMD {path}")
    if not response.startswith('250'):
        print(f"RMD command failed: {response}")
        return False
    print(f"[Client] Removed directory {path}")
    return True


def rmdir(control_socket: socket.socket, path: str) -> bool:
    if not path:
        print("Directory name cannot be empty")
        return False
    try:
        isRemoved = remove_directory_recursively(control_socket, path)
        return isRemoved
    except Exception as e:
        print(f"[Client] Error removing directory: {e}")
        return False
    
def delete(control_socket: socket.socket, file_name: str) -> bool:
    if not file_name:
        print("File name cannot be empty")
        return False
    try:
        response = side_function.send_command(control_socket, f"DELE {file_name}")
        if not response.startswith('250'):
            print(f"DELE command failed: {response}")
            return False
        print(f"[Client] Deleted file {file_name}")
        return True
    except Exception as e:
        print(f"[Client] Error deleting file: {e}")
        return False

def rename(control_socket: socket.socket, old_name: str, new_name: str) -> bool:
    if not old_name or not new_name:
        print("Old and new file names cannot be empty")
        return False
    try:
        response = side_function.send_command(control_socket, f"RNFR {old_name}")
        if not response.startswith('350'):
            print(f"RNFR command failed: {response}")
            return False
        response = side_function.send_command(control_socket, f"RNTO {new_name}")
        if not response.startswith('250'):
            print(f"RNTO command failed: {response}")
            return False
        print(f"[Client] Renamed {old_name} to {new_name}")
        return True
    except Exception as e:
        print(f"[Client] Error renaming file: {e}")
        return False

def get(control_socket: socket.socket, file_name: str, local_path: str = None) -> bool:
    if local_path is None:
        os.makedirs('downloads_from_server', exist_ok=True)
        local_path = os.path.join('downloads_from_server', file_name)

    if not file_name:
        print("File name cannot be empty")
        return False

    file_size = side_function.size_command(control_socket, file_name)
    if file_size is None:
        file_size = 0
    if file_size is bool:
        print(f"[Client] Failed to get size for {file_name}")
        return False

    if ftpconfig.mode == FTPMode.PASSIVE:
        data_sock = connection.create_data_socket_passive(control_socket, f"RETR {file_name}")
    else:
        data_sock = connection.create_data_socket_active(control_socket, f"RETR {file_name}")

    downloaded = 0
    print(f"[Client] Downloading {file_name} to {local_path} ({file_size} bytes)")
    with open(local_path, 'wb') as f:
        while downloaded <= file_size:
            remaining = file_size - downloaded
            chunk_size = min(ftpconfig.buffer_size, remaining)
            data = data_sock.recv(chunk_size)
            if not data:
                break
            f.write(data)
            downloaded += len(data)
            side_function.progress_bar(downloaded, file_size)
        if file_size == 0:
            side_function.progress_bar(0, 0)

    data_sock.close()
    
    response = side_function.receive_response(control_socket)
    if not response.startswith('226'):
        print(f"RETR command failed: {response}")
        return False
        
    if not connection.scan_for_virus(local_path):
        print(f"[Client] File {local_path} is infected. Download aborted.")
        os.remove(local_path)
        return False
    
    print(f"[Client] File {file_name} downloaded successfully as {local_path}")
    return True

def put(control_socket: socket.socket, file_name: str, remote_file_name: str = '') -> bool:
    if not os.path.isfile(file_name):
        print(f"File {file_name} does not exist")
        return False

    if remote_file_name == '':
        remote_file_name = os.path.basename(file_name)

    if not connection.scan_for_virus(file_name):
        print(f"[Client] File {file_name} is infected. Upload aborted.")
        return False

    if ftpconfig.mode == FTPMode.PASSIVE:
        data_sock = connection.create_data_socket_passive(control_socket, f"STOR {remote_file_name}")
    else:
        data_sock = connection.create_data_socket_active(control_socket, f"STOR {remote_file_name}")

    file_size = os.path.getsize(file_name)
    print(f"[Client] Uploading {file_name} to {remote_file_name} ({file_size} bytes)")
    with open(file_name, 'rb') as f:
        bytes_sent = 0
        while bytes_sent <= file_size:
            remaining = file_size - bytes_sent
            chunk_size = min(ftpconfig.buffer_size, remaining)
            data = f.read(chunk_size)
            if not data:
                break
            data_sock.sendall(data)
            bytes_sent += len(data)
            side_function.progress_bar(bytes_sent, file_size)
        if file_size == 0:
            side_function.progress_bar(0, 0)

    if ftpconfig.use_ssl:
        data_sock.unwrap()
    data_sock.close()

    response = side_function.receive_response(control_socket)
    if not response.startswith('226'):
        print(f"STOR command failed: {response}")
        return False

    print(f"[Client] File {file_name} uploaded successfully to server as {remote_file_name}")
    return True

def prompt(control_socket: socket.socket, file_list, command: str) -> list[str]:
    files = []    
    if command == 'mput':
        if '*' in file_list:
            file_type = file_list.split('*')[-1]
            path = file_list.split('*')[0] if file_list.split('*')[0] else '.'
            
            try:
                current_dir = os.getcwd()
                os.chdir(path)
                items = os.listdir('.')
                os.chdir(current_dir)

                if not items:
                    print(f"[Client] No files found in directory {path}")
                    return []

                print(f"[Client] Matched item:")
                for item in items:
                    if item.endswith(file_type) and os.path.isfile(os.path.join(path, item)):
                        print(item)
                        files.append(os.path.join(path, item))
            except OSError as e:
                print(f"[Client] Failed to access directory {path}: {e}")
                return []
        else:
            files = file_list.split() if isinstance(file_list, str) else file_list
        return files
    else:
        if '*' in file_list:
            file_type = file_list.split('*')[-1]
            path = file_list.split('*')[0] if file_list.split('*')[0] else '.'
            
            if not path == '.':
                if not cd(control_socket, path):
                    print(f"[Client] Failed to change to directory {path}")
                    return []
            
            items = ls(control_socket).splitlines()
            if items is None:
                print("[Client] Failed to list directory")
                return []
            print(f"[Client] Matched item:")
            for item in items:
                parts = item.split()
                if len(parts) > 0:
                    file_name = parts[-1]
                    if file_name.endswith(file_type) and not item.lower().startswith("d"):
                        print(file_name)
                        files.append(file_name)
        else:
            files = file_list.split() if isinstance(file_list, str) else file_list
        return files

def mput(control_socket: socket.socket, file_names: list[str]) -> None:
    for file_name in file_names:
        put(control_socket, file_name)


def mget(control_socket: socket.socket, file_names: list[str]) -> None:
    for file_name in file_names:
        get(control_socket, file_name)

def transfer_ascii_binary_mode(control_socket: socket.socket, mode: str) -> bool:
    if mode not in ['I', 'A']:
        print("[Client] Invalid transfer mode. Use 'I' for binary or 'A' for ASCII.")
        return False
    try:
        response = side_function.send_command(control_socket, f"TYPE {mode}")

        if response.startswith("200"):
            return True
        else:
            print(f"[Client] Failed to set transfer mode: {response.strip()}")
            return False
    except socket.error as e:
        print(f"[Client] Socket error while setting transfer mode: {e}")
        return False

def status(control_socket: socket.socket) -> bool:
    try:
        response = side_function.send_command(control_socket, "STAT")
        if not response.startswith('211'):
            print(f"STAT command failed: {response}")
            return False
        peer_name = control_socket.getpeername()
        remote_dir = pwd(control_socket)
        print("Session Status:")

        print(f"🔗 Connected to: {peer_name[0]}:{peer_name[1]}")
        
        print(f"📦 Transfer Mode: {ftpconfig.transfer_mode.name}")
        passive_status = 'ON' if ftpconfig.mode == FTPMode.PASSIVE else 'OFF'
        print(f"📡 Passive Mode: {passive_status}")
        
        print(f"🖥️  Remote Directory: {remote_dir}")
        print(f"💻 Local Directory: {os.getcwd()}")
        print(f"[Client] Server status: {response}")
        return True
    except Exception as e:
        print(f"[Client] Error getting server status: {e}")
        return False

def transfer_passive_mode(control_socket: socket.socket) -> bool:
    try:
        ftpconfig.mode = FTPMode.PASSIVE
        response = side_function.send_command(control_socket, "PASV")

        if response.startswith('200') or response.startswith('227'):
            print(f"[Client] Switched to {ftpconfig.mode} mode")
            return True
        else:
            print(f"[Client] Failed to switch to passive mode: {response.strip()}")
            return False
    except socket.error as e:
        print(f"[Client] Socket error while switching mode: {e}")
        return False
    
def directory_put(control_socket: socket.socket, local_path: str, remote_path: str = None) -> bool:
    if not os.path.isdir(local_path):
        print(f"[Client] Local path {local_path} is not a directory")
        return False
    
    if remote_path is None:
        remote_path = os.path.basename(local_path)
        
    current_remote_path = pwd(control_socket)

    if not current_remote_path:
        print("[Client] Failed to get current remote directory")
        return False
    
    if not cd(control_socket, remote_path):
        if not mkdir(control_socket, remote_path):
            print(f"[Client] Failed to create remote directory {remote_path}")
            return False
        if not cd(control_socket, remote_path):
            print(f"[Client] Failed to change to remote directory {remote_path}")
            return False
        
    items = os.listdir(local_path)
    for item in items:
        item_path = os.path.join(local_path, item)
        if os.path.isdir(item_path):
            if not directory_put(control_socket, item_path, item):
                print(f"[Client] Failed to upload directory {item_path}")
                return False
        elif os.path.isfile(item_path):
            if not put(control_socket, item_path, item):
                print(f"[Client] Failed to upload file {item_path}")
                return False
            
    if not cd(control_socket, current_remote_path):
        print(f"[Client] Failed to return to previous directory {current_remote_path}")
        return False
    
    return True

def directory_get(control_socket: socket.socket, remote_path: str, local_path: str = None) -> bool:
    if not remote_path:
        print("[Client] Remote path cannot be empty")
        return False
    
    if local_path is None:
        local_path = 'downloads_from_server'

    os.makedirs(local_path, exist_ok=True)

    current_remote_path = pwd(control_socket)
    if not current_remote_path:
        print("[Client] Failed to get current remote directory")
        return False
    
    if not cd(control_socket, remote_path):
        print(f"[Client] Failed to change to remote directory {remote_path}")
        return False
    
    items = ls(control_socket).splitlines()
    if items is None:
        print("[Client] Failed to list remote directory")
        return False
    for item in items:
        parts = item.split()
        file_name = parts[-1]

        if item.lower().startswith("d"):
            if not directory_get(control_socket, file_name, os.path.join(local_path, file_name)):
                print(f"[Client] Failed to download directory {file_name}")
                return False
        elif os.path.isfile(file_name):
            if not get(control_socket, file_name, os.path.join(local_path, file_name)):
                print(f"[Client] Failed to download file {file_name}")
                return False
            
    if not cd(control_socket, current_remote_path):
        print(f"[Client] Failed to return to previous directory {current_remote_path}")
        return False
    
    return True