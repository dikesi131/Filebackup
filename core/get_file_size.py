import os
from typing import Any, Optional
from .db import DatabaseExec


class GetFileSize():
    def __init__(self):
        self.db_exec = DatabaseExec()
        self.file_size_dict = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4,
            'PB': 1024 ** 5
        }

    def get_file_size(self, file_path: str) -> Any:
        '''
        Get the size of a file in a human-readable format (KB, MB, etc.)
        param file_path: str: The path to the file
        return: str: The size of the file in a human-readable format
        or None if the file does not exist
        '''
        try:
            size_bytes = float(os.path.getsize(file_path))
            for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.2f} {unit}"
                size_bytes /= 1024
        except OSError as e:
            print(f"Error: {e}")
            return None

    def add_all_mid_file_size(self) -> Optional[str]:
        '''
        Add all mid file sizes to the database
        '''
        mid_file_sizes = self.db_exec.get_all_mid_file_size()
        total_size_bytes = 0.0
        if mid_file_sizes is None:
            return None
        for size_str in mid_file_sizes:
            size, unit = size_str.split()
            size = float(size)
            if unit == 'KB':
                size *= self.file_size_dict['KB']
            elif unit == 'MB':
                size *= self.file_size_dict['MB']
            elif unit == 'GB':
                size *= self.file_size_dict['GB']
            elif unit == 'TB':
                size *= self.file_size_dict['TB']
            elif unit == 'PB':
                size *= self.file_size_dict['PB']
            total_size_bytes += size

        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if total_size_bytes < 1024.0:
                return f"{total_size_bytes:.2f} {unit}"
            total_size_bytes /= 1024
        return None

    def add_all_high_file_size(self) -> Optional[str]:
        '''
        Add all high file sizes to the database
        '''
        high_file_sizes = self.db_exec.get_all_high_file_size()
        total_size_bytes = 0.0
        if high_file_sizes is None:
            return None
        for size_str in high_file_sizes:
            size, unit = size_str.split()
            size = float(size)
            if unit == 'KB':
                size *= self.file_size_dict['KB']
            elif unit == 'MB':
                size *= self.file_size_dict['MB']
            elif unit == 'GB':
                size *= self.file_size_dict['GB']
            elif unit == 'TB':
                size *= self.file_size_dict['TB']
            elif unit == 'PB':
                size *= self.file_size_dict['PB']
            total_size_bytes += size

        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if total_size_bytes < 1024.0:
                return f"{total_size_bytes:.2f} {unit}"
            total_size_bytes /= 1024
        return None
