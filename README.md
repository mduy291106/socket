# SOCKET PROGRAMMING  
## Table of Contents
1. [ClamAV installation and configuration](#clamav)  
2. [FTP Server software used and how it was set up](#ftp)
3. [Instruction to run the program](#Instruction)
4. [Sample commands and expected outputs](#sample)
   
## ClamAV Installation and Configuration (Windows)

1. **Download ClamAV**
   - Download the latest ClamAV for Windows (ZIP version) from the [official website](https://www.clamav.net/downloads).
   - Unzip it to a folder of your choice (e.g., `C:\ClamAV`).

2. **Prepare configuration files**
   - Inside the `conf_examples` folder, locate:
     - `clamd.conf.sample`
     - `freshclam.conf.sample`
   - Move both files to the main ClamAV folder (e.g., `C:\ClamAV`).
   - Remove the `.sample` extension from both file names.
   - Open each file and delete the word `Example` in any configuration lines where it appears.

3. **Update the virus database**
   - Open **Command Prompt**.
   - Navigate to the ClamAV folder:
     ```bash
     cd C:\ClamAV
     ```
   - Run:
     ```bash
     freshclam.exe
     ```
     This will download the latest virus definition database.

4. **Test scanning**
   - In Command Prompt:
     ```bash
     clamscan.exe "path\to\your\file.txt"
     ```
   - If ClamAV is working, it will display the scan result.

## FTP Server Setup (FileZilla on Windows)

### 1. Install FileZilla Server
1. Download FileZilla Server for Windows from the [official website](https://filezilla-project.org/download.php?type=server).
2. Run `FileZilla_Server.exe` to install.
3. After installation, launch FileZilla Server to start configuring.

### 2. Configure FTP Server
1. Open FileZilla Server interface.
2. Go to **Edit → Users**.
3. Click **Add** to create a new user.
4. Under **Authentication**, select **Require a password to log in**.
5. Set and confirm the password for the user.
6. (Optional) Assign a shared folder for the user in the **Shared folders** tab.
7. Save the settings.
## Instructions to Run the Program

### 1. Start the FTP Server
1. Ensure your FTP server (e.g., FileZilla Server) is running.
2. Make sure the server is listening on the correct host and port (default: 21).

### 2. Run the FTP Client
1. Open **Command Prompt**.
2. Navigate to the folder containing `ftp_client.py`:
   ```bash
    cd path/to/your/project
3. Start the client
    python ftp_client.py
4. When prompted for connection details, simply press Enter to use default settings. (host 127.0.0.1 - port 21)  
 
## Sample commands and expected outputs
### 1. List files in directory
```python
ls [path] 
```
#### Expected output
```
[Client] Current directory: /
Type   Name           Last Modified      Size
---------------------------------------------
       ad.txt         Aug 12 08:57        0 B
       as.txt         Aug 12 08:58       23 B
<DIR>  b              Aug 11 03:34
       BTCN06.docx    Aug 12 06:51        0 B
       ex1.cpp        Aug 12 08:20        0 B
       helper.py      Aug 12 06:50     1.1 KB
       new.txt        Aug 11 09:33        0 B
       old_name.txt   Aug 12 09:05    48.5 MB
       test.txt       Aug 12 07:21        0 B
       test2.txt      Aug 10 08:54        0 B
```
**2. Change directory**
```python
cd [path]
```
#### Example
```
cd downloads_from_server
```
#### Expected Output
```
[Client] Current directory: /downloads_from_server
[Client] Changed directory to /downloads_from_server
```
**3. Go to parent directory**
```python
cd .. 
```
#### Example
```
cd ...
```
#### Expected Output
```
[Client] Current directory: /
[Client] Changed directory to /
```
**4. Download file**
```python
get [file] 
```
#### Example
```
get Test.txt
```
Output
```
[Client] File b/Test.txt uploaded successfully to server as Test.txt
```
**5. Upload file**
```python
put [file] 
```
#### Example
```python
put Test.txt
```
Output
```   
[Client] File Test.txt uploaded successfully as downloads_from_server\Test.txt
```