import subprocess
import socket
import os
import sys
from ftp_config import ftpconfig

script_dir = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(script_dir, 'ClamAV uploads')

def scan_file(file_path):
    result = subprocess.run(['clamscan', file_path], capture_output=True, text=True)
    
    if (result.returncode == 2):
        return "Error: ClamAV encountered an error while scanning."
    elif (result.returncode == 1):
        return "INFECTED" 
    else:
        return "OK"

def main():
    server_socket = None
    try:
        os.makedirs(uploads_dir, exist_ok=True)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ftpconfig.clamav_host, ftpconfig.clamav_port))
        server_socket.listen(1)
        print(f"[ClamAV Agent] Successfully started on {ftpconfig.clamav_host}:{ftpconfig.clamav_port}")

        try:
            connection, address = server_socket.accept()
            print(f"[ClamAV Agent] Connection from {address}")
            with connection:
                filename_size = int.from_bytes(connection.recv(4), 'big')
                filename = connection.recv(filename_size).decode('utf-8')
                print(f"[ClamAV Agent] Receiving file: {filename}")

                file_size = int.from_bytes(connection.recv(8), 'big')
                bytes_received = 0
                filepath = os.path.join(uploads_dir, filename)

                with open(filepath, 'wb') as f:
                    while bytes_received < file_size:
                        remaining = file_size - bytes_received
                        chunk_size = min(4096, remaining)
                        data = connection.recv(chunk_size)
                        
                        if not data:
                            break

                        f.write(data)
                        bytes_received += len(data)

                connection.sendall(b'OK') 
                
                result = scan_file(filepath)
                
                try:
                    os.remove(filepath)
                    print(f"[ClamAV Agent] Cleaned up: {filepath}")
                except OSError as e:
                    print(f"[ClamAV Agent] Failed to remove {filepath}: {e}")
                
                connection.sendall(result.encode('utf-8'))
                print(f"[ClamAV Agent] Sent result to client")
        except Exception as e:
            print(f"[ClamAV Agent] Error handling client: {e}")

    except OSError as e:
        if hasattr(e, 'winerror') and e.winerror == 10048:
            print(f"[ClamAV Agent] ERROR: Port {ftpconfig.clamav_port} is already in use!")
            print(f"[ClamAV Agent] Please kill existing processes or use a different port.")
            print(f"[ClamAV Agent] Run: tasklist | findstr python")
            print(f"[ClamAV Agent] Then: taskkill /f /pid <PID>")
        else:
            print(f"[ClamAV Agent] Socket error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ClamAV Agent] Unexpected error: {e}")
        sys.exit(1)
    finally:
        print("[ClamAV Agent] Performing cleanup...")
        if server_socket:
            try:
                server_socket.close()
                print("[ClamAV Agent] Server socket closed")
            except:
                pass
        print("[ClamAV Agent] Shutdown complete")

if __name__ == "__main__":
    main()