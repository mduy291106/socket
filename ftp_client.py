import connection
import command
import os
import msvcrt
from ftp_config import ftpconfig
import side_function

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("═" * 60)
    print(" " * 25 + "FTP CLIENT")
    print("═" * 60)
    ip = input("[Client] Enter FTP server IP: ") or ftpconfig.host
    port = int(input("[Client] Enter FTP server port: ") or ftpconfig.port)
    user = input("[Client] Enter username: ") or ftpconfig.username
    password = input("[Client] Enter password: ") or ftpconfig.password
    control_socket = connection.open_control_connection(ip, port, user, password)
    choice = 1
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("═" * 60)
        print(" " * 19 + "FTP CLIENT - MAIN MENU")
        print("═" * 60)
        print(("🔸 " if choice == 1 else " ") + "1. File and Directory Operations")
        print(("🔸 " if choice == 2 else " ") + "2. Upload/Download")
        print(("🔸 " if choice == 3 else " ") + "3. Session Management")
        print(("🔸 " if choice == 0 else " ") + "Exit")
        print("═" * 60)
        key = msvcrt.getch()
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                choice -= 1
                if choice < 0: choice = 3
            elif key == b'P':
                choice += 1
                if choice > 3: choice = 0
        elif key == b'\r':
            os.system("cls" if os.name == "nt" else "clear")
            if choice == 1:
                change = 1
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("═" * 60)
                    print(" " * 16 + "FILE AND DIRECTORY OPERATION")
                    print("═" * 60)
                    print(("🔸 "if change == 1 else " ") + "1. List files and folders on the FTP server")
                    print(("🔸 "if change == 2 else " ") + "2. Change directory (on server or local)")
                    print(("🔸 "if change == 3 else " ") + "3. Show the current directory on the FTP server")
                    print(("🔸 "if change == 4 else " ") + "4. Create folders on the FTP server")
                    print(("🔸 "if change == 5 else " ") + "5. Delete folders on the FTP server")
                    print(("🔸 "if change == 6 else " ") + "6. Delete a file on the FTP server")
                    print(("🔸 "if change == 7 else " ") + "7. Rename a file on the FTP server")
                    print(("🔸 "if change == 0 else " ") + "Back to main menu")
                    print("═" * 60)

                    key = msvcrt.getch()
                    if key == b'\xe0':
                        key = msvcrt.getch()
                        if key == b'H':
                            change -= 1
                            if change < 0: change = 7
                        elif key == b'P':
                            change += 1
                            if change > 7: change = 0
                    elif key == b'\r':
                        if change == 0:
                            break
                        elif change == 1:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            path = input("[Client] Enter path to list files: ")
                            side_function.print_formatted_list(command.ls(control_socket, path))
                            os.system("pause")
                        elif change == 2:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            a = 1
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(("🔸 "if a == 1 else " ") + "On Server")
                                print(("🔸 "if a == 2 else " ") + "On Local")
                                print(("🔸 "if a == 0 else " ") + "Back to File and Directory Operations")
                                key = msvcrt.getch()
                                if key == b'\xe0':
                                    key = msvcrt.getch()
                                    if key == b'H':
                                        a -= 1
                                        if a < 0: a = 2
                                    elif key == b'P':
                                        a += 1
                                        if a > 2: a = 0
                                elif key == b'\r':
                                    if a == 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        path = input("[Client] Enter path to change directory on server: ")
                                        command.cd(control_socket, path)
                                        os.system("pause")
                                    elif a == 2:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        path = input("[Client] Enter path to change directory on local: ")
                                        if not os.path.isdir(path):
                                            print(f"[Client] Directory does not exist: {path}")
                                            os.system("pause")
                                            continue
                                        os.chdir(path)
                                        print(f"[Client] Changed local directory to: {os.getcwd()}")
                                        os.system("pause")
                                    elif a == 0:
                                        break
                        elif change == 3:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            print(f"[Client] Remote Directory: {command.pwd(control_socket)}")
                            print(f"[Client] Local Directory: {os.getcwd()}")
                            os.system("pause")
                        elif change == 4:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            path = input("[Client] Enter path to create directory: ")
                            command.mkdir(control_socket, path)
                            os.system("pause")
                        elif change == 5:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            path = input("[Client] Enter path to remove directory: ")
                            command.rmdir(control_socket, path)
                            os.system("pause")
                        elif change == 6:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            file = input("[Client] Enter file to delete: ")
                            command.delete(control_socket, file)
                            os.system("pause")
                        elif change == 7:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            old_name = input("[Client] Enter old file name: ")
                            new_name = input("[Client] Enter new file name: ")
                            command.rename(control_socket, old_name, new_name)
                            os.system("pause")
            elif choice == 2:
                change = 1
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("═" * 60)
                    print(" " * 17 + "UPLOAD/DOWNLOAD MANAGEMENT")
                    print("═" * 60)
                    print(("🔸 " if change == 1 else " ") + "1. Download a single file")
                    print(("🔸 " if change == 2 else " ") + "2. Upload a single file")
                    print(("🔸 " if change == 3 else " ") + "3. Download multiple files (wildcard support)")
                    print(("🔸 " if change == 4 else " ") + "4. Upload multiple files (wildcard support)")
                    print(("🔸 " if change == 5 else " ") + "5. Download a directory")
                    print(("🔸 " if change == 6 else " ") + "6. Upload a directory")
                    print(("🔸 " if change == 0 else " ") + "Back to main menu")
                    print("═" * 60)

                    key = msvcrt.getch()
                    if key == b'\xe0':
                        key = msvcrt.getch()
                        if key == b'H':
                            change -= 1
                            if change < 0: change = 6
                        elif key == b'P':
                            change += 1
                            if change > 6: change = 0
                    elif key == b'\r':
                        if change == 0:
                            break
                        elif change == 1:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            file = input("[Client] Enter file to download: ")
                            command.get(control_socket, file)
                            os.system("pause")
                        elif change == 2:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            file = input("[Client] Enter file to upload: ")
                            command.put(control_socket, file)
                            os.system("pause")
                        elif change == 3:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            files = input("[Client] Enter files to download (space-separated): ")
                            file_list = command.prompt(control_socket, files, 'mget')
                            check = input("[Client] Do you want to download these files? (y/n): ").strip().lower()
                            if check == 'y':
                                command.mget(control_socket, file_list)
                            else:
                                print("[Client] Download cancelled.")
                            os.system("pause")
                        elif change == 4:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            files = input("[Client] Enter files to upload (space-separated): ")
                            file_list = command.prompt(control_socket, files, 'mput')
                            check = input("[Client] Do you want to upload these files? (y/n): ").strip().lower()
                            if check == 'y':
                                command.mput(control_socket, file_list)
                            else:
                                print("[Client] Upload cancelled.")
                            os.system("pause")
                        elif change == 5:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            directory = input("[Client] Enter directory to download: ")
                            command.directory_get(control_socket, directory)
                            os.system("pause")
                        elif change == 6:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            directory = input("[Client] Enter directory to upload: ")
                            command.directory_put(control_socket, directory)
                            os.system("pause")
            elif choice == 3:
                change = 1
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("═" * 60)
                    print(" " * 21 + "SESSION MANAGEMENT" )
                    print("═" * 60)
                    print(("🔸 " if change == 1 else " ") + "1. Set file transfer mode (text/binary)")
                    print(("🔸 " if change == 2 else " ") + "2. Show current session status")
                    print(("🔸 " if change == 3 else " ") + "3. Toggle between passive and active FTP mode")
                    print(("🔸 " if change == 4 else " ") + "4. Connect to the FTP server")
                    print(("🔸 " if change == 5 else " ") + "5. Disconnect from the FTP server")
                    print(("🔸 " if change == 6 else " ") + "6. Exit the FTP client")
                    print(("🔸 " if change == 7 else " ") + "7. Show help text for commands")
                    print(("🔸 " if change == 0 else " ") + "Back to main menu")
                    print("═" * 60)

                    key = msvcrt.getch()
                    if key == b'\xe0':
                        key = msvcrt.getch()
                        if key == b'H':
                            change -= 1
                            if change < 0: change = 7
                        elif key == b'P':
                            change += 1
                            if change > 7: change = 0
                    elif key == b'\r':
                        if change == 0:
                            break
                        elif change == 1:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            mode = input("[Client] Enter transfer mode (A for ASCII, I for Binary): ").strip().upper()
                            if mode in ["A", "I"]:
                                command.transfer_ascii_binary_mode(control_socket, mode)
                            else:
                                print("[Client] Invalid mode. Use 'A' for ASCII or 'I' for Binary.")
                            os.system("pause")
                        elif change == 2:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            command.status(control_socket)
                            os.system("pause")
                        elif change == 3:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            command.transfer_mode(control_socket)
                            os.system("pause")
                        elif change == 4:
                            os.system("cls" if os.name == "nt" else "clear")
                            ip = input("[Client] Enter FTP server IP: ") or ftpconfig.host
                            port = int(input("[Client] Enter FTP server port: ") or ftpconfig.port)
                            user = input("[Client] Enter username: ") or ftpconfig.username
                            password = input("[Client] Enter password: ") or ftpconfig.password
                            control_socket = connection.open_control_connection(ip, port, user, password)
                            print("[Client] Connected to the FTP server.")
                            os.system("pause")
                        elif change == 5:
                            os.system("cls" if os.name == "nt" else "clear")
                            if ftpconfig.is_quit:
                                print("[Client] No active connection to FTP server. Please connect first.")
                                os.system("pause")
                                continue
                            check = input("[Client] Are you sure you want to disconnect? (y/n): ").strip().lower()
                            if check == 'y':
                                connection.close_control_connection(control_socket)
                                print("[Client] Disconnected from the FTP server.")
                            else:
                                print("[Client] Disconnection cancelled.")
                            os.system("pause")
                        elif change == 6:
                            os.system("cls" if os.name == "nt" else "clear")
                            check = input("[Client] Are you sure you want to exit? (y/n): ").strip().lower()
                            if check == 'y':
                                os.system("cls" if os.name == "nt" else "clear")
                                print("[Client] Thank you for using the FTP client!")
                                exit(0)
                            else:
                                print("[Client] Exit cancelled.")
                                os.system("pause")
                        elif change == 7:
                            panda = 1
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print("═" * 60)
                                print(" " * 19 + "HELP TEXT FOR COMMANDS")
                                print("═" * 60)
                                print(("🔸 " if panda == 1 else " ") + "List files and folders on the FTP server")
                                print(("🔸 " if panda == 2 else " ") + "Change directory (on server or local)")
                                print(("🔸 " if panda == 3 else " ") + "Show the current directory on the server")
                                print(("🔸 " if panda == 4 else " ") + "Create folders on the FTP server")
                                print(("🔸 " if panda == 5 else " ") + "Delete folders on the FTP server")
                                print(("🔸 " if panda == 6 else " ") + "Delete a file on the FTP server")
                                print(("🔸 " if panda == 7 else " ") + "Rename a file on the FTP server")
                                print(("🔸 " if panda == 8 else " ") + "Download a file from the FTP server")
                                print(("🔸 " if panda == 9 else " ") + "Upload a single file")
                                print(("🔸 " if panda == 10 else " ") + "Download multiple files")
                                print(("🔸 " if panda == 11 else " ") + "Upload multiple files")
                                print(("🔸 " if panda == 12 else " ") + "Download a directory")
                                print(("🔸 " if panda == 13 else " ") + "Upload a directory")
                                print(("🔸 " if panda == 14 else " ") + "Set file transfer mode (text/binary)")
                                print(("🔸 " if panda == 15 else " ") + "Show current session status")
                                print(("🔸 " if panda == 16 else " ") + "Toggle between passive and active FTP mode")
                                print(("🔸 " if panda == 17 else " ") + "Connect to the FTP server")
                                print(("🔸 " if panda == 18 else " ") + "Disconnect from the FTP server")
                                print(("🔸 " if panda == 19 else " ") + "Exit the FTP client")
                                print(("🔸 " if panda == 0 else " ") + "Back to Session Management")
                                print("═" * 60)

                                key = msvcrt.getch()
                                if key == b'\xe0':
                                    key = msvcrt.getch()
                                    if key == b'H':
                                        panda -= 1
                                        if panda < 0: panda = 19
                                    elif key == b'P':
                                        panda += 1
                                        if panda > 19: panda = 0
                                elif key == b'\r':
                                    if panda == 0:
                                        break
                                    elif panda == 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_ls())
                                        os.system("pause")
                                    elif panda == 2:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_cd())
                                        os.system("pause")
                                    elif panda == 3:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_pwd())
                                        os.system("pause")
                                    elif panda == 4:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_mkdir())
                                        os.system("pause")
                                    elif panda == 5:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_rmdir())
                                        os.system("pause")
                                    elif panda == 6:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_delete())
                                        os.system("pause")
                                    elif panda == 7:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_rename())
                                        os.system("pause")
                                    elif panda == 8:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_get())
                                        os.system("pause")
                                    elif panda == 9:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_put())
                                        os.system("pause")
                                    elif panda == 10:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_mget())
                                        os.system("pause")
                                    elif panda == 11:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_mput())
                                        os.system("pause")
                                    elif panda == 12:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_dget())
                                        os.system("pause")
                                    elif panda == 13:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_dput())
                                        os.system("pause")
                                    elif panda == 14:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_transfer_mode())
                                        os.system("pause")
                                    elif panda == 15:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_status())
                                        os.system("pause")
                                    elif panda == 16:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_passive())
                                        os.system("pause")
                                    elif panda == 17:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_connect())
                                        os.system("pause")
                                    elif panda == 18:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_disconnect())
                                        os.system("pause")
                                    elif panda == 19:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(side_function.help_for_quit())
                                        os.system("pause")
            elif choice == 0:
                os.system("cls" if os.name == "nt" else "clear")
                print("[Client] Thank you for using the FTP client!")
                break
            
if __name__ == "__main__":
    main()