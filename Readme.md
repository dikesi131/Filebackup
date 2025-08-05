# FilebackUp – File Backup Tool

## Project Overview  
FilebackUp is a powerful file-backup utility that supports **full**, **incremental**, and **differential** backup strategies.  
The tool classifies files into **High**, **Medium**, and **Low** priority levels according to their importance, and applies different backup policies to each level to improve backup efficiency and reduce storage consumption.

## Features  
- **Multi-level Backup Policy**: Files are split into High / Medium / Low priorities for differentiated treatment  
- **Full Backup**: Back up everything at once—ideal for first-time backups  
- **Incremental Backup**: Only new files are backed up—perfect for periodic backups of medium-priority data  
- **Differential Backup**: Back up files that have changed since the last full backup—great for real-time protection of high-priority data  
- **SQLite Database**: Stores backup history and file metadata  
- **File-Hash Verification**: Detects file changes via MD5 hash values  
- **Email Notification**: Automatically sends a summary e-mail after every backup  
- **Comprehensive Logging**: Records every step and every error in detail  

## Requirements  
- Python 3.6+  
- SQLAlchemy  
- PyYAML  

## Installation  

1. Clone the repository:  
```sh
git clone https://github.com/yourusername/FilebackUp.git
cd FilebackUp
```

2. Install dependencies:  
```sh
pip install -r requirements.txt
```

## Configuration  
Before first use, edit `config/config.yaml`:

```yaml
# Email settings
email: your-email@qq.com
# Authorization code (NOT your login password)
PassCode: your-email-auth-code
port: 587
SendTo: recipient-email@example.com

# File-level mapping
HighLevelFiles:
  - high_priority_dir: "/path/to/important/files"

MidLevelFiles:
  - HighInMid:
    - high_dir1: "/path/to/important/files/in/mid"
  - mid_dir1: "/path/to/mid/priority/files"
  - mid_dir2: "/path/to/another/mid/files"

LowLevelFiles:
  - low_dir1: "/path/to/low/priority/files"
```

## Usage  

Basic backup:  
```sh
python file_backup.py -o /path/to/backup/destination
```

Force a full backup:  
```sh
python file_backup.py -o /path/to/backup/destination -f
```

Parameters:  
- `-o, --output`: Target directory for backup files  
- `-f, --force`: Force a full backup regardless of previous state  

## How It Works  

1. **Full Backup**  
   - Runs the first time you back up or whenever `-f` is supplied  
   - Backs up files of **all** priority levels  
   - Records file hashes and paths in the database  

2. **Incremental Backup**  
   - Applied to **Medium-level** files  
   - Only new files not yet recorded in the database are copied  
   - Database is updated accordingly  

3. **Differential Backup**  
   - Applied to **High-level** files  
   - Compares current MD5 hashes with stored hashes to detect changes  
   - Only modified files are copied; database is updated  

## Project Structure  

```
FilebackUp/
├── config/
│   └── config.yaml          # configuration file
├── core/
│   ├── cal_file_hash.py     # compute file hashes
│   ├── check_is_backuped.py # check backup status
│   ├── db.py                # database operations
│   ├── decorators.py        # decorators
│   ├── differential_backup.py
│   ├── full_backup.py
│   ├── get_config.py        # load YAML config
│   ├── get_file_size.py
│   ├── get_parm.py          # parse CLI arguments
│   ├── global_vars.py
│   ├── incremental_backup.py
│   ├── logger.py
│   ├── send_message.py      # send e-mail notifications
│   └── setting.py           # DB settings
├── file_backup.py           # main entry point
├── Readme-zh.md             # Chinese documentation
└── Readme.md                # English documentation
```

## Database Schema  

The tool uses an SQLite database with the following tables:

1. **HIGH_LEVEL_FILES**  
   - filename, path, size, hash, is_new, is_changed  

2. **MID_LEVEL_FILES**  
   - filename, path, size, is_new  

3. **LOW_LEVEL_FILES**  
   - filename, path, size  

4. **IS_BACKUPED**  
   - target path information  

## Performance Optimizations  

- Multi-level strategies reduce redundant backups  
- Hash comparisons quickly identify changed files  
- Decorators add runtime statistics without cluttering core logic  

## FAQ  

1. **Backup fails**  
   - Check destination permissions  
   - Verify `config.yaml`  
   - Inspect the log file for details  

2. **E-mail not sent**  
   - Confirm the authorization code is correct  
   - Ensure network connectivity  

3. **Database errors**  
   - Check file permissions on the SQLite file  
   - Database is created automatically on first run  

## Contributing  

We welcome contributions!  
1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Open a Pull Request  

## License

Apache-2.0 License
