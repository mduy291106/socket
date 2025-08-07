import connection
import command
import os
import msvcrt
from ftp_config import ftpconfig
import side_function

def main():
    ip = input("Enter FTP server IP: ") or ftpconfig.host
    port = int(input("Enter FTP server port: ") or ftpconfig.port)
    user = input("Enter username: ") or ftpconfig.username
    password = input("Enter password: ") or ftpconfig.password
    control_socket = connection.open_control_connection(ip, port, user, password)
    choice = 1
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("FTP Client Menu:")
        print(("-> " if choice == 1 else " ") + "1. File and Directory Operations")
        print(("-> " if choice == 2 else " ") + "2. Upload/Download")
        print(("-> " if choice == 3 else " ") + "3. Session Management")
        print(("-> " if choice == 0 else " ") + "Exit")
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
                    print("File and Directory Operations:")
                    print(("-> "if change == 1 else " ") + "1. List files and folders on the FTP server")
                    print(("-> "if change == 2 else " ") + "2. Change directory (on server or local)")
                    print(("-> "if change == 3 else " ") + "3. Show the current directory on the server")
                    print(("-> "if change == 4 else " ") + "4. Create folders on the FTP server")
                    print(("-> "if change == 5 else " ") + "5. Delete folders on the FTP server")
                    print(("-> "if change == 6 else " ") + "6. Delete a file on the FTP server")
                    print(("-> "if change == 7 else " ") + "7. Rename a file on the FTP server")
                    print(("-> "if change == 0 else " ") + "Back to main menu")

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
                            path = input("Enter path to list files: ")
                            print(command.ls(control_socket, path))
                            os.system("pause")
                        elif change == 2:
                            path = input("Enter path to change directory: ")
                            command.cd(control_socket, path)
                            print(f"Changed directory to: {path}")
                            os.system("pause")
                        elif change == 3:
                            command.pwd(control_socket)
                            os.system("pause")
                        elif change == 4:
                            path = input("Enter path to create directory: ")
                            command.mkdir(control_socket, path)
                            os.system("pause")
                        elif change == 5:
                            path = input("Enter path to remove directory: ")
                            command.rmdir(control_socket, path)
                            os.system("pause")
                        elif change == 6:
                            file = input("Enter file to delete: ")
                            command.delete(control_socket, file)
                            os.system("pause")
                        elif change == 7:
                            old_name = input("Enter old file name: ")
                            new_name = input("Enter new file name: ")
                            command.rename(control_socket, old_name, new_name)
                            os.system("pause")
            elif choice == 2:
                change = 1
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Upload/Download:")
                    print(("-> " if change == 1 else " ") + "1. Download a file from the FTP server")
                    print(("-> " if change == 2 else " ") + "2. Upload a single file")
                    print(("-> " if change == 3 else " ") + "3. Download multiple files (wildcard support)")
                    print(("-> " if change == 4 else " ") + "4. Upload multiple files (wildcard support)")
                    print(("-> " if change == 5 else " ") + "5. Download a directory")
                    print(("-> " if change == 6 else " ") + "6. Upload a directory")
                    print(("-> " if change == 0 else " ") + "Back to main menu")

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
                            file = input("Enter file to download: ")
                            command.get(control_socket, file)
                            os.system("pause")
                        elif change == 2:
                            file = input("Enter file to upload: ")
                            command.put(control_socket, file)
                            os.system("pause")
                        elif change == 3:
                            files = input("Enter files to download (space-separated): ")
                            file_list = command.prompt(control_socket, files, 'mget')
                            check = input("Do you want to download these files? (y/n): ").strip().lower()
                            if check == 'y':
                                command.mget(control_socket, file_list)
                            else:
                                print("Download cancelled.")
                            os.system("pause")
                        elif change == 4:
                            files = input("Enter files to upload (space-separated): ")
                            file_list = command.prompt(control_socket, files, 'mput')
                            check = input("Do you want to upload these files? (y/n): ").strip().lower()
                            if check == 'y':
                                command.mput(control_socket, file_list)
                            else:
                                print("Upload cancelled.")
                            os.system("pause")
                        elif change == 5:
                            directory = input("Enter directory to upload: ")
                            command.directory_put(control_socket, directory)
                            os.system("pause")
                        elif change == 6:
                            directory = input("Enter directory to download: ")
                            command.directory_get(control_socket, directory)
                            os.system("pause")
            elif choice == 3:
                change = 1
                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Session Management:")
                    print(("-> " if change == 1 else " ") + "1. Set file transfer mode (text/binary)")
                    print(("-> " if change == 2 else " ") + "2. Show current session status")
                    print(("-> " if change == 3 else " ") + "3. Toggle passive FTP mode")
                    print(("-> " if change == 4 else " ") + "4. Connect to the FTP server")
                    print(("-> " if change == 5 else " ") + "5. Disconnect from the FTP server")
                    print(("-> " if change == 6 else " ") + "6. Exit the FTP client")
                    print(("-> " if change == 7 else " ") + "7. Show help text for commands")
                    print(("-> " if change == 0 else " ") + "Back to main menu")

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
                            mode = input("Enter transfer mode (A for ASCII, I for Binary): ").strip().upper()
                            if mode in ["A", "I"]:
                                command.transfer_ascii_binary_mode(control_socket, mode)
                            else:
                                print("Invalid mode. Use 'A' for ASCII or 'I' for Binary.")
                            os.system("pause")
                        elif change == 2:
                            command.status()
                            os.system("pause")
                        elif change == 3:
                            command.transfer_passive_mode(control_socket)
                            os.system("pause")
                        elif change == 4:
                            ip = input("Enter FTP server IP: ") or ftpconfig.host
                            port = int(input("Enter FTP server port: ") or ftpconfig.port)
                            user = input("Enter username: ") or ftpconfig.username
                            password = input("Enter password: ") or ftpconfig.password
                            control_socket = connection.open_control_connection(ip, port, user, password)
                            print("Connected to the FTP server.")
                            os.system("pause")
                        elif change == 5:
                            connection.close_control_connection(control_socket)
                            print("Disconnected from the FTP server.")
                            os.system("pause")
                        elif change == 6:
                            check = input("Are you sure you want to exit? (y/n): ").strip().lower()
                            if check == 'y':
                                exit(0)
                            else:
                                print("Exit cancelled.")
                                os.system("pause")
                        elif change == 7:
                            panda = 1
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print("Help Text for Commands:")
                                print(("-> " if panda == 1 else " ") + "ist files and folders on the FTP server")
                                print(("-> " if panda == 2 else " ") + "Change directory (on server or local)")
                                print(("-> " if panda == 3 else " ") + "Show the current directory on the server")
                                print(("-> " if panda == 4 else " ") + "Create folders on the FTP server")
                                print(("-> " if panda == 5 else " ") + "Delete folders on the FTP server")
                                print(("-> " if panda == 6 else " ") + "Delete a file on the FTP server")
                                print(("-> " if panda == 7 else " ") + "Rename a file on the FTP server")
                                print(("-> " if panda == 8 else " ") + "Download a file from the FTP server")
                                print(("-> " if panda == 9 else " ") + "Upload a single file")
                                print(("-> " if panda == 10 else " ") + "Download multiple files")
                                print(("-> " if panda == 11 else " ") + "Upload multiple files")
                                print(("-> " if panda == 12 else " ") + "Download a directory")
                                print(("-> " if panda == 13 else " ") + "Upload a directory")
                                print(("-> " if panda == 14 else " ") + "Set file transfer mode (text/binary)")
                                print(("-> " if panda == 15 else " ") + "Show current session status")
                                print(("-> " if panda == 16 else " ") + "Toggle passive FTP mode")
                                print(("-> " if panda == 17 else " ") + "Connect to the FTP server")
                                print(("-> " if panda == 18 else " ") + "Disconnect from the FTP server")
                                print(("-> " if panda == 19 else " ") + "Exit the FTP client")
                                print(("-> " if panda == 0 else " ") + "Back to Session Management")

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
                                        print(side_function.help_for_ls())
                                        os.system("pause")
                                    elif panda == 2:
                                        print(side_function.help_for_cd())
                                        os.system("pause")
                                    elif panda == 3:
                                        print(side_function.help_for_pwd())
                                        os.system("pause")
                                    elif panda == 4:
                                        print(side_function.help_for_mkdir())
                                        os.system("pause")
                                    elif panda == 5:
                                        print(side_function.help_for_rmdir())
                                        os.system("pause")
                                    elif panda == 6:
                                        print(side_function.help_for_delete())
                                        os.system("pause")
                                    elif panda == 7:
                                        print(side_function.help_for_rename())
                                        os.system("pause")
                                    elif panda == 8:
                                        print(side_function.help_for_get())
                                        os.system("pause")
                                    elif panda == 9:
                                        print(side_function.help_for_put())
                                        os.system("pause")
                                    elif panda == 10:
                                        print(side_function.help_for_mget())
                                        os.system("pause")
                                    elif panda == 11:
                                        print(side_function.help_for_mput())
                                        os.system("pause")
                                    elif panda == 12:
                                        print(side_function.help_for_dget())
                                        os.system("pause")
                                    elif panda == 13:
                                        print(side_function.help_for_dput())
                                        os.system("pause")
                                    elif panda == 14:
                                        print(side_function.help_for_transfer_mode())
                                        os.system("pause")
                                    elif panda == 15:
                                        print(side_function.help_for_status())
                                        os.system("pause")
                                    elif panda == 16:
                                        print(side_function.help_for_passive())
                                        os.system("pause")
                                    elif panda == 17:
                                        print(side_function.help_for_connect())
                                        os.system("pause")
                                    elif panda == 18:
                                        print(side_function.help_for_disconnect())
                                        os.system("pause")
                                    elif panda == 19:
                                        print(side_function.help_for_quit())
                                        os.system("pause")
            elif choice == 0:   
                print("Thank you!")
                break
            
if __name__ == "__main__":
    main()