def progress_bar(current: int, total: int, length: int = 50) -> None:
    if total <= 0:
        current = total = 1
    percent = current / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r|{bar}| {percent:.2%}', end='\r')
    if current == total:
        print()

def format_size(size_in_bytes: int) -> str:
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024**2:
        return f"{size_in_bytes/1024:.1f} KB"
    elif size_in_bytes < 1024**3:
        return f"{size_in_bytes/1024**2:.1f} MB"
    else:
        return f"{size_in_bytes/1024**3:.1f} GB"

def print_formatted_list(list_file: str):
    print(f"{'Type':<6} {'Name':<20} {'Last Modified':<16} {'Size':>10}")
    print("─" * 55)
    lines = list_file.splitlines()
    for line in lines:
        parts = line.split()
        size_str = parts[4]
        month = parts[5]
        day = parts[6]
        time_or_year = parts[7]
        name = parts[8]

        if line.startswith('d'):
            item_type = "<DIR>"
            formatted_size = ""
        else:
            item_type = ""
            formatted_size = format_size(int(size_str))

        date_str = f"{month} {day} {time_or_year}"
        print(f"{item_type:<6} {name:<20} {date_str:<16} {formatted_size:>10}")
    print("─" * 55)


def help_for_ls() -> str:
    return """
DIRECTORY LISTING COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: ls [directory_path]

DESCRIPTION:
    Lists files and directories in the specified remote directory.
    If no path is provided, lists contents of the current remote directory.

SYNTAX:
    ls                          # List current directory
    ls /path/to/directory       # List specific directory
    ls ..                       # List parent directory
    ls /                        # List root directory

EXAMPLES:
    ls                          # Show files in current directory
    ls /home/user/documents     # List contents of documents folder
    ls ../downloads             # List parent directory's downloads folder

OUTPUT FORMAT:
    Type    Name                Last Modified       Size
    ────────────────────────────────────────────────────
    <DIR>   folder_name         Jan 15 2024         
            document.txt        Jan 15 14:30        1.2KB
            image.jpg           Jan 14 09:15        245.7KB

NOTES:
    • <DIR> indicates a directory
    • File sizes are shown in human-readable format (B, KB, MB, GB)
    • Shows total count of files and directories
    • Automatically handles filenames with spaces
    • Works with both absolute and relative paths

SEE ALSO: cd, pwd, mkdir, rmdir
    """

def help_for_cd() -> str:
    return """
CHANGE DIRECTORY COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: cd <directory_path>

DESCRIPTION:
    Changes the current working directory on the remote FTP server.
    This affects where other commands (like ls, put, get) operate.

SYNTAX:
    cd <path>                   # Change to specified directory
    cd /                        # Change to root directory
    cd ..                       # Move up one directory level
    cd ~                        # Change to home directory (if supported)

EXAMPLES:
    cd /home/user              # Change to user's home directory
    cd documents               # Change to 'documents' subdirectory
    cd ../downloads            # Go up one level, then into downloads
    cd /var/www/html           # Change to web server directory

SPECIAL PATHS:
    /                          # Root directory
    ..                         # Parent directory
    .                          # Current directory (no change)
    ~                          # Home directory (server dependent)

TIPS:
    • Use 'pwd' to see current directory before changing
    • Use 'ls' to see available directories
    • Path can be absolute (/full/path) or relative (subfolder)
    • Some servers are case-sensitive for directory names

ERROR HANDLING:
    • Returns error if directory doesn't exist
    • Returns error if insufficient permissions
    • Automatically validates path format

SEE ALSO: pwd, ls, mkdir
    """

def help_for_pwd() -> str:
    return """
PRINT WORKING DIRECTORY COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: pwd

DESCRIPTION:
    Displays the current working directory path on the remote FTP server.
    This shows exactly where you are in the server's file system.

SYNTAX:
    pwd                        # Show current directory path

EXAMPLES:
    pwd                        # Output: /home/user/documents

OUTPUT:
    Displays the full absolute path of your current location on the server.
    Example outputs:
    • /home/username
    • /var/www/html
    • /uploads/2024/january

USAGE SCENARIOS:
    • Check your location before uploading files
    • Verify you're in the correct directory
    • Get full path for reference in scripts
    • Confirm directory changes were successful

TIPS:
    • Always use pwd after cd to confirm directory change
    • Useful for troubleshooting navigation issues
    • Shows exactly where uploaded files will be placed
    • Helps understand the server's directory structure

NO PARAMETERS:
    This command takes no arguments and always shows the current directory.

SEE ALSO: cd, ls
    """

def help_for_mkdir() -> str:
    return """
CREATE DIRECTORY COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: mkdir <directory_name>

DESCRIPTION:
    Creates a new directory on the remote FTP server.
    The directory is created in the current working directory unless
    a full path is specified.

SYNTAX:
    mkdir <name>               # Create directory in current location
    mkdir <path/name>          # Create directory with full path
    mkdir "../name"            # Create in parent directory

EXAMPLES:
    mkdir uploads              # Create 'uploads' folder here
    mkdir /home/user/backup    # Create backup folder with full path
    mkdir "my documents"       # Create folder with spaces (use quotes)
    mkdir projects/2024        # Create nested path (if projects exists)

NAMING RULES:
    • Directory names are case-sensitive on most servers
    • Avoid special characters: < > : " | ? * \\ /
    • Use quotes for names containing spaces
    • Maximum length varies by server (usually 255 characters)

PERMISSIONS:
    • Requires write permission in the target directory
    • Some servers restrict directory creation
    • May fail if directory already exists

ERROR CONDITIONS:
    • Directory already exists
    • Insufficient permissions
    • Invalid directory name
    • Parent directory doesn't exist (for nested paths)

TIPS:
    • Use 'ls' to verify the directory was created
    • Check permissions if creation fails
    • Some servers auto-create intermediate directories
    • Consider using 'cd' to navigate into new directory

SEE ALSO: rmdir, cd, ls
    """

def help_for_rmdir() -> str:
    return """
REMOVE DIRECTORY COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: rmdir <directory_name>

DESCRIPTION:
    Removes a directory from the remote FTP server.
    This operation recursively deletes the directory and ALL its contents,
    including subdirectories and files.

SYNTAX:
    rmdir <name>               # Remove directory in current location
    rmdir <path/name>          # Remove directory with full path

EXAMPLES:
    rmdir old_backup           # Remove 'old_backup' directory
    rmdir /tmp/temp_files      # Remove temp_files with full path
    rmdir "old documents"      # Remove directory with spaces

WARNING - DESTRUCTIVE OPERATION:
    • This command PERMANENTLY deletes directories and ALL contents
    • There is NO undo operation
    • All files and subdirectories are removed recursively
    • Always double-check the directory name before executing

RECURSIVE BEHAVIOR:
    The command automatically:
    1. Enters the target directory
    2. Deletes all files within it
    3. Recursively removes all subdirectories
    4. Finally removes the main directory

SAFETY FEATURES:
    • Validates directory exists before deletion
    • Properly handles nested directory structures
    • Returns to original directory after operation
    • Provides progress feedback for large directories

ERROR CONDITIONS:
    • Directory doesn't exist
    • Insufficient permissions
    • Directory is not empty (on some servers)
    • Directory is currently in use
    • Network interruption during operation

TIPS:
    • Use 'ls' to verify contents before deletion
    • Consider downloading important data first
    • Some servers may have directory protection
    • Operation may take time for large directories

ALTERNATIVES:
    • Use file manager for selective deletion
    • Download directory first as backup
    • Delete files individually with 'delete' command

SEE ALSO: mkdir, delete, ls
    """

def help_for_delete() -> str:
    return """
DELETE FILE COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: delete <filename>

DESCRIPTION:
    Permanently deletes a file from the remote FTP server.
    This operation cannot be undone.

SYNTAX:
    delete <filename>          # Delete file in current directory
    delete <path/filename>     # Delete file with full path

EXAMPLES:
    delete document.txt        # Delete document.txt in current directory
    delete /uploads/old.pdf    # Delete file with full path
    delete "my file.doc"       # Delete file with spaces (use quotes)
    delete *.tmp               # Delete files matching pattern (if supported)

WARNING - PERMANENT DELETION:
    • This operation PERMANENTLY removes the file
    • There is NO undo or recovery option
    • Always verify the filename before executing
    • Consider downloading important files first

FILE SPECIFICATIONS:
    • File must exist on the remote server
    • Case-sensitive on most servers
    • Use quotes for filenames with spaces
    • Full path can be specified

SAFETY FEATURES:
    • Validates file exists before deletion
    • Provides confirmation of successful deletion
    • Error reporting for failed operations

ERROR CONDITIONS:
    • File doesn't exist
    • Insufficient permissions
    • File is currently locked or in use
    • Invalid filename format
    • Network interruption

TIPS:
    • Use 'ls' to verify file exists and get exact name
    • Check file permissions if deletion fails
    • Some servers log all file deletions
    • Consider using 'get' to download before deleting

PERMISSIONS:
    • Requires delete permission on the file
    • May require write permission in the directory
    • Some servers restrict file deletion by user

BEST PRACTICES:
    • Always double-check the filename
    • Download important files before deletion
    • Use 'ls' to confirm file is gone after deletion
    • Keep track of deleted files for audit purposes

SEE ALSO: rmdir, get, ls, rename
    """

def help_for_rename() -> str:
    return """
RENAME FILE COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: rename <old_name> <new_name>

DESCRIPTION:
    Renames a file or directory on the remote FTP server.
    Can also be used to move files between directories.

SYNTAX:
    rename <old_name> <new_name>        # Rename in current directory
    rename <old_path> <new_path>        # Move and/or rename with paths

EXAMPLES:
    rename old.txt new.txt              # Simple rename
    rename "old file.doc" "new file.doc" # Rename with spaces
    rename temp.log /backup/archive.log  # Move and rename
    rename report.pdf final_report.pdf   # Add prefix/suffix

RENAMING RULES:
    • Both old and new names must be specified
    • New name cannot already exist (will overwrite on some servers)
    • Case changes are supported (old.txt → OLD.TXT)
    • Can change file extension (doc → pdf)

MOVING FILES:
    • Specify different paths to move files between directories
    • Source: /folder1/file.txt → Target: /folder2/file.txt
    • Creates move effect by renaming with new path
    • Target directory must exist

SPECIAL CONSIDERATIONS:
    • File/directory must exist and be accessible
    • Requires appropriate permissions
    • Some servers may not support cross-directory moves
    • Operation is atomic (all-or-nothing)

ERROR CONDITIONS:
    • Source file/directory doesn't exist
    • Target name already exists
    • Insufficient permissions
    • Invalid characters in new name
    • Cross-filesystem moves not supported

SAFETY FEATURES:
    • Validates source exists before operation
    • Reports success/failure clearly
    • Maintains file permissions and attributes
    • Preserves timestamps (on most servers)

TIPS:
    • Use 'ls' to verify current names and check results
    • Test permissions with small files first
    • Some servers log rename operations
    • Consider case sensitivity of target system

COMMON USE CASES:
    • Organizing files with descriptive names
    • Adding timestamps: report.pdf → report_2024-01-15.pdf
    • Moving files to different directories
    • Correcting filename typos
    • Changing file extensions

SEE ALSO: move, copy, ls
    """

def help_for_get() -> str:
    return """
DOWNLOAD FILE COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: get <remote_file> [local_path]

DESCRIPTION:
    Downloads a file from the remote FTP server to your local computer.
    Includes virus scanning, progress tracking, and error recovery.

SYNTAX:
    get <filename>                    # Download to default location
    get <filename> <local_path>       # Download to specific location
    get <path/filename>               # Download with remote path

EXAMPLES:
    get document.pdf                  # Download to downloads_from_server/
    get report.doc ./local_report.doc # Download to current directory
    get /uploads/image.jpg            # Download from specific server path
    get "file with spaces.txt"        # Handle filenames with spaces

DOWNLOAD BEHAVIOR:
    • Default location: downloads_from_server/ directory
    • Automatically creates download directory if needed
    • Preserves original filename unless local path specified
    • Shows real-time progress with speed and ETA

PROGRESS DISPLAY:
    |████████████████████████| 75.3%

SECURITY FEATURES:
    • Automatic virus scanning of downloaded files
    • Infected files are automatically deleted
    • File size validation before download
    • Secure transfer with optional SSL/TLS

FILE SIZE HANDLING:
    • Displays file size before download starts
    • Supports files from bytes to gigabytes
    • Automatic retry for network interruptions
    • Resume capability for large files (server dependent)

ERROR RECOVERY:
    • Automatic retry on network errors
    • Validates file integrity after download
    • Reports specific error conditions
    • Cleans up partial downloads on failure

COMMON ERRORS:
    • File not found on server
    • Insufficient local disk space
    • Permission denied (server or local)
    • File is infected with virus
    • Network timeout during transfer

TIPS:
    • Use 'ls' to verify file exists and check size
    • Ensure sufficient local disk space
    • Check local directory permissions
    • Large files may take time - be patient
    • Virus scanning adds slight delay but ensures safety

PERFORMANCE:
    • Optimized buffer sizes for fast transfers
    • Automatic connection mode selection
    • Efficient memory usage for large files
    • Progress updates every 100ms

SEE ALSO: put, mget, ls, status
    """

def help_for_put() -> str:
    return """
UPLOAD FILE COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: put <local_file> [remote_name]

DESCRIPTION:
    Uploads a file from your local computer to the remote FTP server.
    Includes virus scanning, progress tracking, and error recovery.

SYNTAX:
    put <local_file>                  # Upload with same name
    put <local_file> <remote_name>    # Upload with different name
    put "./documents/file.pdf"        # Upload from specific local path

EXAMPLES:
    put document.pdf                  # Upload document.pdf to server
    put ./report.doc server_report.doc # Upload with new name
    put "C:/Users/Me/file.txt"        # Upload from Windows path
    put "/home/user/image.jpg"        # Upload from Unix path

UPLOAD BEHAVIOR:
    • File uploaded to current remote directory
    • Preserves original filename unless remote name specified
    • Shows real-time progress with speed and ETA
    • Automatic virus scanning before upload

SECURITY FEATURES:
    • Pre-upload virus scanning of local files
    • Infected files are rejected and not uploaded
    • Secure transfer with optional SSL/TLS encryption
    • File integrity validation during transfer

PROGRESS DISPLAY:
    |████████████████████████| 82.7%

PRE-UPLOAD CHECKS:
    • Verifies local file exists and is readable
    • Checks file isn't currently locked/in use
    • Validates remote directory permissions
    • Ensures sufficient server disk space (if supported)

ERROR RECOVERY:
    • Automatic retry on network errors
    • Validates upload completion
    • Reports specific error conditions
    • Cleans up partial uploads on failure

COMMON ERRORS:
    • Local file not found or not readable
    • File is infected with virus
    • Insufficient server disk space
    • Permission denied on remote server
    • Network timeout during transfer
    • Remote filename conflicts

FILE TYPES:
    • Supports all file types and sizes
    • Automatic binary/text mode detection
    • Handles special characters in filenames
    • Preserves file timestamps when possible

TIPS:
    • Use 'pwd' to verify upload destination
    • Check remote permissions with 'status'
    • Large files may take time - be patient
    • Virus scanning ensures server security
    • Use quotes for filenames with spaces

PERFORMANCE:
    • Optimized for fast transfers
    • Efficient memory usage
    • Automatic compression (if server supports)
    • Progress updates every 100ms

SEE ALSO: get, mput, ls, pwd, status
    """

def help_for_mget() -> str:
    return """
MULTIPLE FILE DOWNLOAD COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: mget <file_pattern> or mget <file1> <file2> ...

DESCRIPTION:
    Downloads multiple files from the remote FTP server in a single operation.
    Supports wildcards, file lists, and batch processing with progress tracking.

SYNTAX:
    mget <file1> <file2> <file3>      # Download specific files
    mget *.txt                        # Download all .txt files
    mget *.pdf *.doc                  # Download multiple file types
    mget /path/*.jpg                  # Download from specific directory

WILDCARD PATTERNS:
    *.txt                             # All files ending with .txt
    *.{pdf,doc,docx}                  # Multiple extensions
    report_*                          # Files starting with 'report_'
    *_2024.*                          # Files containing '_2024'

EXAMPLES:
    mget *.pdf                        # Download all PDF files
    mget file1.txt file2.txt          # Download specific files
    mget /uploads/*.jpg               # Download images from uploads folder
    mget "*.txt" "*.doc"              # Download text and document files

BATCH PROCESSING:
    • Processes files sequentially for reliability
    • Shows progress for each individual file
    • Displays overall batch progress
    • Continues on errors (skips failed files)

PROGRESS DISPLAY:
    [Client] Downloading 5 file(s)...
    [Client] (1/5) Downloading report.pdf
    |████████████████████████| 100%
    [Client] (2/5) Downloading data.txt
    |██████████              | 45%

SMART FEATURES:
    • Automatic duplicate detection
    • Virus scanning for each downloaded file
    • Creates download directory structure
    • Preserves file timestamps
    • Handles filenames with spaces

ERROR HANDLING:
    • Continues downloading remaining files if one fails
    • Reports success/failure count at end
    • Detailed error messages for each failure
    • Automatic cleanup of partial downloads

CONFIRMATION PROMPT:
    Before starting download, displays:
    • List of matched files
    • Total number of files
    • Estimated total size (if available)
    • Option to proceed or cancel

DOWNLOAD LOCATION:
    • Default: downloads_from_server/ directory
    • Maintains directory structure for remote paths
    • Creates subdirectories as needed

TIPS:
    • Use 'ls' to preview files before downloading
    • Check available disk space for large batches
    • Wildcards are case-sensitive on some servers
    • Use quotes around patterns with special characters
    • Consider network speed for large file sets

PERFORMANCE:
    • Optimized for batch operations
    • Reuses connections for efficiency
    • Parallel processing where safe
    • Intelligent retry mechanisms

SEE ALSO: get, mput, ls
    """

def help_for_mput() -> str:
    return """
MULTIPLE FILE UPLOAD COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: mput <file_pattern> or mput <file1> <file2> ...

DESCRIPTION:
    Uploads multiple files from your local computer to the remote FTP server
    in a single operation. Supports wildcards, file lists, and batch processing.

SYNTAX:
    mput <file1> <file2> <file3>      # Upload specific files
    mput *.txt                        # Upload all .txt files
    mput *.pdf *.doc                  # Upload multiple file types
    mput ./documents/*.jpg            # Upload from specific directory

WILDCARD PATTERNS:
    *.txt                             # All .txt files in current directory
    ./docs/*.pdf                      # All PDFs in docs folder
    **/*.jpg                          # All JPGs in all subdirectories
    report_*                          # Files starting with 'report_'

EXAMPLES:
    mput *.pdf                        # Upload all PDF files
    mput file1.txt file2.txt          # Upload specific files
    mput ./uploads/*.jpg              # Upload images from uploads folder
    mput "C:/Documents/*.doc"         # Upload from Windows path

BATCH PROCESSING:
    • Processes files sequentially for reliability
    • Shows progress for each individual file
    • Displays overall batch progress
    • Continues on errors (skips failed files)

PROGRESS DISPLAY:
    [Client] Uploading 3 file(s)...
    [Client] (1/3) Uploading report.pdf
    |████████████████████████| 100%
    [Client] (2/3) Uploading data.txt
    |██████████              | 45%

SECURITY FEATURES:
    • Virus scanning before each upload
    • Infected files are skipped automatically
    • Validates file integrity during transfer
    • Secure transfer with SSL/TLS support

PRE-UPLOAD VALIDATION:
    • Checks all files exist and are readable
    • Validates filenames for remote compatibility
    • Estimates total upload size and time
    • Confirms sufficient remote disk space

CONFIRMATION PROMPT:
    Before starting upload, displays:
    • List of matched local files
    • Total number of files
    • Total size to upload
    • Estimated transfer time
    • Option to proceed or cancel

ERROR HANDLING:
    • Continues uploading remaining files if one fails
    • Reports success/failure count at end
    • Detailed error messages for each failure
    • Automatic cleanup of partial uploads

SMART FEATURES:
    • Automatic duplicate detection
    • Preserves local directory structure
    • Handles filenames with spaces
    • Maintains file timestamps when possible

UPLOAD DESTINATION:
    • Files uploaded to current remote directory
    • Use 'cd' to change destination before upload
    • Check destination with 'pwd' command

TIPS:
    • Use 'pwd' to verify upload destination
    • Check remote permissions before large uploads
    • Wildcards work with local file system
    • Use quotes for paths with spaces
    • Consider file sizes and network speed

PERFORMANCE:
    • Optimized for batch operations
    • Efficient connection reuse
    • Automatic buffer size optimization
    • Progress updates for user feedback

SEE ALSO: put, mget, cd, pwd, ls
    """

def help_for_dput() -> str:
    return """
DIRECTORY UPLOAD COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: dput <local_directory> [remote_directory]

DESCRIPTION:
    Recursively uploads an entire directory and all its contents from your
    local computer to the remote FTP server, preserving directory structure.

SYNTAX:
    dput <local_dir>                  # Upload to same name on server
    dput <local_dir> <remote_name>    # Upload with different remote name
    dput "./my_folder"                # Upload from relative path
    dput "C:/Users/Me/Documents"      # Upload from absolute path

EXAMPLES:
    dput ./projects                   # Upload projects folder
    dput ./backup server_backup       # Upload backup as server_backup
    dput "C:/My Documents" docs       # Upload with spaces in name
    dput /home/user/photos            # Upload photos directory

RECURSIVE BEHAVIOR:
    • Uploads ALL files and subdirectories
    • Preserves complete directory structure
    • Creates remote directories as needed
    • Maintains relative paths and hierarchy

DIRECTORY STRUCTURE EXAMPLE:
    Local:  ./projects/2024/reports/file.pdf
    Remote: /current_dir/projects/2024/reports/file.pdf

UPLOAD PROCESS:
    1. Validates local directory exists and is readable
    2. Creates remote directory structure
    3. Uploads files systematically
    4. Shows progress for each file and directory
    5. Reports final statistics

PROGRESS DISPLAY:
    [Client] Uploading directory ./projects (127 items)
    [Client] (1/127) Uploading file: readme.txt
    [Client] (15/127) Uploading directory: images
    [Client] (89/127) Uploading file: data/report.pdf

SECURITY FEATURES:
    • Virus scans every file before upload
    • Skips infected files automatically
    • Validates directory permissions
    • Secure transfer with SSL/TLS

SMART FEATURES:
    • Automatically creates remote directories
    • Handles nested directory structures
    • Preserves file timestamps when possible
    • Skips system files (., .., .DS_Store, etc.)

ERROR HANDLING:
    • Continues on individual file failures
    • Reports detailed error information
    • Maintains operation log
    • Returns to original directory on completion

SIZE CONSIDERATIONS:
    • Calculates total size before starting
    • Shows estimated transfer time
    • Monitors available disk space
    • Handles large directory trees efficiently

EXCLUSION PATTERNS:
    Automatically skips:
    • Hidden system files (.*) 
    • Temporary files (*.tmp, *.temp)
    • Backup files (*.bak, *.backup)
    • OS-specific files (.DS_Store, Thumbs.db)

TIPS:
    • Use 'pwd' to verify upload destination
    • Consider network speed for large directories
    • Check remote disk space availability
    • Test with small directories first
    • Monitor progress for very large uploads

PERFORMANCE:
    • Optimized for recursive operations
    • Efficient directory traversal
    • Batch processing where possible
    • Memory-conscious for large trees

LIMITATIONS:
    • Requires sufficient remote disk space
    • May be slow for directories with many small files
    • Some servers limit directory depth
    • Network timeouts possible for very large directories

SEE ALSO: dget, mput, mkdir, cd, pwd
    """

def help_for_dget() -> str:
    return """
DIRECTORY DOWNLOAD COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: dget <remote_directory> [local_directory]

DESCRIPTION:
    Recursively downloads an entire directory and all its contents from the
    remote FTP server to your local computer, preserving directory structure.

SYNTAX:
    dget <remote_dir>                 # Download to downloads_from_server/
    dget <remote_dir> <local_path>    # Download to specific local path
    dget "/uploads/backup"            # Download from specific remote path

EXAMPLES:
    dget projects                     # Download projects directory
    dget /uploads/docs ./documents    # Download to local documents folder
    dget server_backup ./backup       # Download backup directory
    dget "/home/user/photos"          # Download photos from server

RECURSIVE BEHAVIOR:
    • Downloads ALL files and subdirectories
    • Preserves complete directory structure
    • Creates local directories as needed
    • Maintains relative paths and hierarchy

DIRECTORY STRUCTURE EXAMPLE:
    Remote: /server/projects/2024/reports/file.pdf
    Local:  ./downloads_from_server/projects/2024/reports/file.pdf

DOWNLOAD PROCESS:
    1. Validates remote directory exists and is accessible
    2. Creates local directory structure
    3. Downloads files systematically
    4. Shows progress for each file and directory
    5. Reports final statistics

PROGRESS DISPLAY:
    [Client] Downloading directory /uploads/projects (95 items)
    [Client] (1/95) Downloading file: readme.txt
    [Client] (12/95) Downloading directory: images
    [Client] (67/95) Downloading file: data/report.pdf

DEFAULT LOCATION:
    If no local path specified, downloads to:
    ./downloads_from_server/<directory_name>/

SECURITY FEATURES:
    • Virus scans every downloaded file
    • Deletes infected files automatically
    • Validates file integrity during transfer
    • Secure transfer with SSL/TLS

SMART FEATURES:
    • Automatically creates local directories
    • Handles nested directory structures
    • Preserves file timestamps when possible
    • Handles filenames with spaces and special characters

ERROR HANDLING:
    • Continues on individual file failures
    • Reports detailed error information
    • Maintains operation log
    • Returns to original remote directory on completion

SIZE CONSIDERATIONS:
    • Shows total files/directories count
    • Monitors available local disk space
    • Handles large directory trees efficiently
    • Progress tracking for user awareness

FILE FILTERING:
    • Downloads all file types by default
    • Maintains original file extensions
    • Preserves file permissions where possible
    • Handles binary and text files correctly

DISK SPACE MANAGEMENT:
    • Checks available local disk space
    • Warns if space might be insufficient
    • Efficient streaming for large files
    • Cleanup on cancellation or errors

TIPS:
    • Check available local disk space first
    • Use 'ls' to preview directory contents
    • Consider network speed for large directories
    • Test with small directories first
    • Monitor download progress

COMMON USE CASES:
    • Backing up server directories
    • Synchronizing remote folders
    • Downloading project archives
    • Retrieving log file collections
    • Mirroring server content

PERFORMANCE:
    • Optimized for recursive operations
    • Efficient directory traversal
    • Memory-conscious for large trees
    • Parallel processing where safe

LIMITATIONS:
    • Requires sufficient local disk space
    • May be slow for many small files
    • Network timeouts possible for large directories
    • Some servers limit concurrent connections

SEE ALSO: dput, mget, get, cd, ls
    """

def help_for_transfer_mode() -> str:
    return """
TRANSFER MODE CONFIGURATION
═══════════════════════════════════════════════════════════════════

COMMANDS: ascii | binary

DESCRIPTION:
    Sets the file transfer mode between ASCII (text) and BINARY modes.
    This affects how files are transferred and is crucial for file integrity.

SYNTAX:
    ascii                            # Set ASCII/text mode
    binary                           # Set binary mode

TRANSFER MODES EXPLAINED:

ASCII MODE (Text Mode):
    • For text files only (.txt, .html, .csv, .xml, etc.)
    • Converts line endings between systems
    • Windows (CRLF) ↔ Unix (LF) ↔ Mac (CR)
    • Suitable for configuration files, logs, code

BINARY MODE (Image Mode):
    • For ALL non-text files
    • No data conversion - exact byte copy
    • Required for: images, videos, executables, archives
    • Preserves file integrity completely
    • DEFAULT and RECOMMENDED mode

WHEN TO USE ASCII:
    Plain text files (.txt, .log)
    Source code (.py, .js, .html, .css)
    Configuration files (.ini, .conf)
    CSV and data files
    Documentation (.md, .rst)

WHEN TO USE BINARY:
    Images (.jpg, .png, .gif, .bmp)
    Videos (.mp4, .avi, .mov)
    Audio (.mp3, .wav, .flac)
    Archives (.zip, .tar, .rar)
    Executables (.exe, .app, .deb)
    Office documents (.pdf, .docx, .xlsx)
    Databases (.db, .sqlite)

CRITICAL WARNING:
    Using ASCII mode for binary files will CORRUPT them!
    • Images will be damaged and unviewable
    • Executables will not run
    • Archives will be unextractable
    • Data will be permanently lost

CURRENT MODE DISPLAY:
    Check current mode with 'status' command:
    Transfer Mode: BINARY (recommended)
    Transfer Mode: ASCII (text files only)

AUTO-DETECTION:
    The client attempts to detect file types automatically:
    • Binary mode for unknown extensions
    • Warns when ASCII mode might be inappropriate
    • Provides recommendations based on file extension

EXAMPLES:
    binary                           # Set binary mode (recommended default)
    ascii                            # Set ASCII mode for text files
    
    # Typical workflow:
    binary                           # Set safe default
    put image.jpg                    # Upload binary file
    ascii                            # Switch for text files
    put config.txt                   # Upload text file
    binary                           # Return to safe default

BEST PRACTICES:
    • Use BINARY mode as default (safer)
    • Only switch to ASCII for known text files
    • Always return to BINARY after ASCII transfers
    • When in doubt, use BINARY mode

PLATFORM DIFFERENCES:
    • Windows: CRLF (\\r\\n)
    • Unix/Linux: LF (\\n)
    • Classic Mac: CR (\\r)
    • ASCII mode handles these conversions automatically

TECHNICAL DETAILS:
    • ASCII mode processes each byte
    • Binary mode transfers raw byte streams
    • MODE command sent to FTP server
    • Server acknowledges mode change

TROUBLESHOOTING:
    File corrupted after transfer?
        → Probably used ASCII mode for binary file
        → Re-transfer in BINARY mode
    
    Text file has wrong line endings?
        → Use ASCII mode for cross-platform text files
        → Or use text editor to fix line endings

SEE ALSO: status, put, get
    """

def help_for_status() -> str:
    return """
CONNECTION STATUS COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: status

DESCRIPTION:
    Displays comprehensive information about your current FTP connection,
    session settings, and server status. Essential for troubleshooting
    and monitoring your FTP session.

SYNTAX:
    status                           # Show complete status information

INFORMATION DISPLAYED:

CONNECTION DETAILS:
    • Server IP address and port
    • Connection status (connected/disconnected)
    • SSL/TLS encryption status
    • Connection uptime
    • Network latency information

DIRECTORY INFORMATION:
    • Current remote directory (server)
    • Current local directory (your computer)
    • Directory permissions
    • Available disk space (if supported)

SESSION CONFIGURATION:
    • Transfer mode (ASCII/BINARY)
    • Connection mode (ACTIVE/PASSIVE)
    • Buffer size settings
    • Timeout configurations
    • Keep-alive status

SECURITY STATUS:
    • SSL/TLS encryption: Enabled/Disabled
    • Certificate information
    • Authentication method used
    • Virus scanning status

PERFORMANCE METRICS:
    • Data transfer statistics
    • Connection speed
    • Files transferred this session
    • Total bytes transferred

EXAMPLE OUTPUT:
    === Session Status ===
    Connected to: 192.168.1.100:21
    Transfer Mode: BINARY
    Connection Mode: PASSIVE
    SSL/TLS: Enabled
    Remote Directory: /home/user/uploads
    Local Directory: C:\\Users\\Me\\Downloads
    Buffer Size: 8192 bytes
    === Server Response ===
    211-Server status information...

SERVER RESPONSE SECTION:
    Displays raw server status information including:
    • Server software and version
    • Server capabilities
    • Current session statistics
    • Server-specific status messages

TROUBLESHOOTING USES:
    Connection Issues:
        • Verify you're connected to correct server
        • Check SSL/TLS configuration
        • Confirm network connectivity

    Transfer Problems:
        • Check transfer mode (binary vs ASCII)
        • Verify connection mode (active vs passive)
        • Review buffer size settings

    Permission Errors:
        • Check current directories
        • Verify authentication status
        • Review server capabilities

    Performance Issues:
        • Monitor buffer sizes
        • Check connection statistics
        • Review network latency

WHEN TO USE STATUS:
    • Before important file transfers
    • After changing directories
    • When troubleshooting connection issues
    • To verify security settings
    • For session monitoring

SECURITY CHECKS:
    • Confirms SSL/TLS is active
    • Shows authentication method
    • Displays certificate status
    • Verifies virus scanning is enabled

TIPS:
    • Run status after connecting to verify settings
    • Use before large transfers to check configuration
    • Helpful for documenting connection settings
    • Essential for troubleshooting problems

NO PARAMETERS:
    This command requires no additional parameters and shows
    all available status information.

SEE ALSO: connect, transfer_mode, pwd
    """

def help_for_passive() -> str:
    return """
CONNECTION MODE TOGGLE
═══════════════════════════════════════════════════════════════════

COMMAND: passive

DESCRIPTION:
    Toggles between ACTIVE and PASSIVE FTP connection modes.
    This affects how data connections are established and can resolve
    firewall and NAT traversal issues.

SYNTAX:
    passive                          # Toggle between active/passive modes

CONNECTION MODES EXPLAINED:

PASSIVE MODE (Recommended):
    • Client initiates ALL connections
    • Server provides IP and port for data connection
    • Client connects to server's data port
    • Works through most firewalls and NAT
    • Default mode for modern FTP clients

ACTIVE MODE (Traditional):
    • Server initiates data connections back to client
    • Client provides IP and port to server
    • Server connects to client's data port
    • May be blocked by firewalls/NAT
    • Required by some older servers

WHEN TO USE PASSIVE MODE:
    Behind firewalls (most common scenario)
    Using NAT/router (home/office networks)
    Corporate networks with security policies
    When active mode connections fail
    Default choice for most situations

WHEN TO USE ACTIVE MODE:
    Direct server connection (no NAT/firewall)
    Some older FTP servers require it
    When passive mode is not supported
    Troubleshooting passive mode issues

FIREWALL CONSIDERATIONS:

Passive Mode:
    • Outbound connections only
    • Works with stateful firewalls
    • No special firewall configuration needed
    • Compatible with most network setups

Active Mode:
    • Requires inbound connections
    • May need firewall port ranges opened
    • Can be blocked by restrictive policies
    • Needs special NAT configuration

TROUBLESHOOTING:

If data transfers fail:
    1. Try toggling mode: passive
    2. Check firewall settings
    3. Verify network connectivity
    4. Contact network administrator

"Can't open data connection" errors:
    • Usually indicates mode incompatibility
    • Try switching modes
    • Check if server supports both modes

CURRENT MODE CHECKING:
    Use 'status' command to see current mode:
    Connection Mode: PASSIVE (firewall-friendly)
    Connection Mode: ACTIVE (may need firewall config)

AUTOMATIC DETECTION:
    • Client attempts passive mode first
    • Falls back to active if passive fails
    • Some servers only support one mode
    • Mode preference saved per session

EXAMPLES:
    passive                          # Toggle to opposite mode
    status                           # Check current mode
    ls                              # Test data connection with new mode

NETWORK COMPATIBILITY:

    Home Networks: Passive recommended
    Corporate: Passive usually required
    Public WiFi: Passive only option
    Direct Connection: Either mode works
    Server-to-Server: Often requires active

TECHNICAL DETAILS:
    • PASV command for passive mode
    • PORT command for active mode
    • Data ports: 20 (active) or random (passive)
    • Control port: Always 21

BEST PRACTICES:
    • Start with passive mode
    • Only change if transfers fail
    • Document working mode for future reference
    • Test with 'ls' command after changing

SEE ALSO: status, connect, transfer_mode
    """

def help_for_connect() -> str:
    return """
SERVER CONNECTION COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: connect [hostname] [port]

DESCRIPTION:
    Establishes a connection to an FTP server with authentication,
    SSL/TLS support, and automatic configuration detection.

SYNTAX:
    connect                          # Use default server settings
    connect <hostname>               # Connect to hostname, default port
    connect <hostname> <port>        # Connect with specific port
    connect <ip_address> <port>      # Connect using IP address

EXAMPLES:
    connect                          # Connect to 127.0.0.1:21 (default)
    connect ftp.example.com          # Connect to server on port 21
    connect 192.168.1.100 2121      # Connect to IP with custom port
    connect files.company.com 21     # Connect to company FTP server

CONNECTION PROCESS:

SERVER CONNECTION:
    • Establishes TCP connection to server
    • Waits for server welcome message
    • Validates FTP server response
    • Sets connection timeout (30 seconds)

SSL/TLS NEGOTIATION (if enabled):
    • Sends AUTH TLS command
    • Negotiates encryption parameters
    • Establishes secure control channel
    • Configures data channel protection

AUTHENTICATION:
    • Prompts for username (or uses default)
    • Prompts for password (or uses default)
    • Validates credentials with server
    • Establishes authenticated session

CONFIGURATION:
    • Sets optimal transfer modes
    • Configures connection parameters
    • Tests basic functionality
    • Ready for file operations

INPUT PROMPTS:
    If credentials not in config:
    
    Enter FTP server IP: [127.0.0.1]
    Enter FTP server port: [21]
    Enter username: [mduy]
    Enter password: [***]
    
    Press Enter to use default values shown in brackets.

DEFAULT CONFIGURATION:
    • Server: 127.0.0.1 (localhost)
    • Port: 21 (standard FTP)
    • Username: mduy
    • Password: 142857
    • SSL/TLS: Enabled
    • Mode: Passive

SECURITY FEATURES:
    SSL/TLS encryption for control and data channels
    Password masking during input
    Certificate validation (configurable)
    Secure authentication protocols

CONNECTION VALIDATION:
    Server reachability test
    FTP service availability
    SSL/TLS capability check
    Authentication verification
    Basic command functionality

ERROR HANDLING:
    Connection timeouts (30-second limit)
    DNS resolution failures
    SSL/TLS negotiation errors
    Authentication failures
    Network connectivity issues

COMMON CONNECTION ERRORS:

"Connection timeout":
    • Server not responding
    • Incorrect hostname/IP
    • Network connectivity issues
    • Firewall blocking connection

"Authentication failed":
    • Incorrect username/password
    • Account disabled or locked
    • Server access restrictions

"SSL/TLS negotiation failed":
    • Server doesn't support encryption
    • Certificate issues
    • SSL/TLS version mismatch

FIREWALL CONSIDERATIONS:
    • Port 21 must be accessible (control)
    • Additional ports for data (passive mode)
    • Corporate firewalls may block FTP
    • Consider using passive mode

SERVER COMPATIBILITY:
    Standard FTP servers (vsftpd, ProFTPD, etc.)
    Windows IIS FTP
    FileZilla Server
    Pure-FTPd
    Most commercial FTP servers

TIPS:
    • Test connection with 'status' after connecting
    • Use 'ls' to verify basic functionality
    • Check 'pwd' to see initial directory
    • Save working connection details for future use

ENVIRONMENT VARIABLES:
    Set these to avoid prompts:
    FTP_HOST=server.example.com
    FTP_PORT=21
    FTP_USERNAME=myuser
    FTP_PASSWORD=mypass

SEE ALSO: disconnect, status, passive
    """

def help_for_disconnect() -> str:
    return """
SERVER DISCONNECTION COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: disconnect

DESCRIPTION:
    Gracefully disconnects from the current FTP server, properly closing
    all connections and cleaning up resources.

SYNTAX:
    disconnect                       # Disconnect from current server

DISCONNECTION PROCESS:

GRACEFUL SHUTDOWN:
    • Sends QUIT command to server
    • Waits for server acknowledgment
    • Closes control connection properly
    • Terminates any active data transfers

RESOURCE CLEANUP:
    • Closes all open sockets
    • Releases SSL/TLS connections
    • Clears connection state
    • Frees allocated resources

SESSION RESET:
    • Resets connection parameters
    • Clears cached directory information
    • Returns to disconnected state
    • Ready for new connection

WHEN TO DISCONNECT:
    Finished with file operations
    Switching to different server
    Troubleshooting connection issues
    Ending FTP session
    Network problems requiring reconnection

AUTOMATIC DISCONNECTION:
    The client automatically disconnects on:
    • Network timeouts
    • Server-initiated disconnections
    • Fatal errors
    • Client application exit

SAFETY FEATURES:
    Completes ongoing transfers before disconnecting
    Saves partial transfer state where possible
    Prevents data corruption
    Proper SSL/TLS session termination

CONNECTION STATE:
    After disconnection:
    • No server commands available
    • File transfers disabled
    • Must reconnect before operations
    • Local commands still function

ERROR HANDLING:
    • Handles network interruptions gracefully
    • Continues cleanup even if server unresponsive
    • Reports disconnection status
    • Cleans up even on forced disconnection

EXAMPLES:
    disconnect                       # Normal disconnection
    # After network issues:
    disconnect                       # Force cleanup
    connect server.com               # Reconnect to server

VERIFICATION:
    After disconnection, verify with:
    status                          # Should show "Not connected"

TROUBLESHOOTING SCENARIOS:

Hung connections:
    disconnect                      # Force cleanup
    connect                         # Establish new connection

Network timeouts:
    disconnect                      # Clean state
    # Check network connectivity
    connect                         # Retry connection

Authentication issues:
    disconnect                      # Reset session
    # Verify credentials
    connect                         # Try with new credentials

SERVER RESPONSE:
    Typical server responses:
    "221 Goodbye" - Normal disconnection
    "221 Service closing control connection" - Successful logout

POST-DISCONNECTION:
    • All remote commands will fail
    • Use 'connect' to establish new session
    • Local directory commands still work
    • File system operations remain available

BEST PRACTICES:
    • Always disconnect when finished
    • Don't leave idle connections open
    • Disconnect before switching servers
    • Use disconnect for troubleshooting

RESOURCE IMPACT:
    • Minimal CPU usage
    • Immediate memory cleanup
    • Network resources released
    • Server connection slot freed

AUTOMATION:
    • Can be used in scripts
    • Safe to call multiple times
    • No-op if already disconnected
    • Always succeeds

NO PARAMETERS:
    This command takes no parameters and immediately
    begins the disconnection process.

SEE ALSO: connect, quit, status
    """

def help_for_quit() -> str:
    return """
EXIT APPLICATION COMMAND
═══════════════════════════════════════════════════════════════════

COMMAND: quit

DESCRIPTION:
    Exits the FTP client application completely, performing cleanup
    and ensuring all connections are properly closed.

SYNTAX:
    quit                            # Exit the FTP client

EXIT PROCESS:

CONNECTION CLEANUP:
    • Automatically disconnects from FTP server
    • Closes all open connections gracefully
    • Sends QUIT command to server
    • Waits for server acknowledgment

RESOURCE CLEANUP:
    • Closes all file handles
    • Releases network resources
    • Clears temporary files
    • Frees allocated memory

SESSION TERMINATION:
    • Saves session statistics (if configured)
    • Clears sensitive data from memory
    • Performs security cleanup
    • Exits application cleanly

SAFETY FEATURES:
     Completes ongoing file transfers
     Prevents data corruption
     Saves important session data
     Secure memory cleanup

AUTOMATIC ACTIONS:
    When quitting, the client automatically:
    • Disconnects from current server
    • Cancels any pending operations
    • Cleans up temporary files
    • Releases system resources

CONFIRMATION:
    The application may prompt for confirmation if:
    • File transfers are in progress
    • Unsaved changes exist
    • Important operations are pending

EXAMPLES:
    quit                            # Normal application exit
    
    # Alternative exit methods:
    # Ctrl+C (interrupt signal)
    # Close window/terminal
    # System shutdown

INTERRUPTED OPERATIONS:
    If quit is called during:
    
    File transfers:
        • Attempts to complete current file
        • Cleanly cancels remaining queue
        • Reports partial transfer status

    Directory operations:
        • Completes current directory
        • Returns to original location
        • Reports completion status

GRACEFUL vs FORCED EXIT:
    
    Graceful (recommended):
        quit                        # Proper cleanup
    
    Forced (emergency only):
        Ctrl+C                      # Interrupt signal
        # May leave incomplete operations

SESSION STATISTICS:
    Before exit, may display:
    • Total files transferred
    • Total bytes transferred
    • Session duration
    • Connection statistics

RECOVERY INFORMATION:
    On abnormal exit, the client:
    • Logs current state
    • Saves recovery information
    • Enables session resume (if supported)
    • Reports incomplete operations

ALTERNATIVES TO QUIT:
    
    Disconnect only:
        disconnect                  # Stay in application
    
    Switch servers:
        disconnect                  # Close current
        connect new.server.com      # Connect to new server

SYSTEM INTEGRATION:
    • Respects system shutdown signals
    • Integrates with task managers
    • Supports scripted automation
    • Handles console interrupts

SECURITY CONSIDERATIONS:
    • Clears passwords from memory
    • Closes encrypted connections properly
    • Removes temporary files securely
    • Logs session end for audit

POST-EXIT CLEANUP:
    After quit:
    • Application process terminates
    • All network connections closed
    • Temporary files removed
    • System resources released

TROUBLESHOOTING:
    
    Application won't quit:
        • Wait for operations to complete
        • Use Ctrl+C for emergency exit
        • Check for hung network operations

    Incomplete cleanup:
        • Check for remaining temp files
        • Verify network connections closed
        • Review system resource usage

BEST PRACTICES:
    • Always use 'quit' for normal exit
    • Wait for operations to complete
    • Don't force-quit unless necessary
    • Monitor system resources after exit

NO PARAMETERS:
    This command takes no parameters and immediately
    begins the application exit process.

SEE ALSO: disconnect, status
    """