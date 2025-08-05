import subprocess
from pathlib import Path
from .global_vars import get_var  # type: ignore
from .decorators import full_backup_decorator  # type: ignore
from .db import DatabaseExec  # type: ignore
from .get_file_size import GetFileSize  # type: ignore
from .cal_file_hash import FileHasher  # type: ignore
from typing import Optional, Dict, List


class FullBackup:
    def __init__(self) -> None:
        self.g_logger = get_var('g_logger')
        self.commands: Dict[str, Dict[str, str]] = {
            'macOS': {
                # force copy, {0} is source, {1} is dest
                # -R: copy all subdirectories, including empty ones
                # -f: if destination does not exist
                'cp_dir': 'cp -rf {0} {1}',
                'cp_file': 'cp -f {0} {1}',
            },
            'Windows': {
                # force copy, {0} is source, {1} is dest
                # /E: copy all subdirectories, including empty ones
                # /I: if destination does not exist
                # and copying more than one file
                'cp_dir': 'xcopy {0} {1} /E /I /Y',
                'cp_file': 'copy {0} {1} /Y',
            }
        }

    def __check_system(self) -> Optional[bool]:
        '''
        check system is macOS/Linux or Windows, if it is macOS or Linux,
        return True else return False
        '''
        system = subprocess.check_output('uname', shell=True).decode().strip()
        if system == 'Darwin':
            # macOS
            self.g_logger.info('System is macOS')
            return True
        elif system == 'Linux':
            # Linux
            self.g_logger.info('System is Linux')
            return True
        elif system == 'Windows':
            # Windows
            self.g_logger.info('System is Windows')
            return False
        else:
            # exit program, return None, print error message
            self.g_logger.error('Unknown system')
            return None

    def get_all_file_path(self,
                          source_dir: Dict[str, List[str]]) -> Dict[str, List[Dict]]:  # noqa
        '''
        Get all file path from source_dir
        param source_dir: Dict[str, list[str]], it contains all level files
        return: list[str], it contains all file path
        '''
        all_files: Dict[str, List[Dict]] = {
            'high': [],
            'mid': [],
            'low': []
        }
        for key in source_dir.keys():
            if key == 'high':
                for source in source_dir[key]:
                    source_path = Path(source)
                    if source_path.is_dir():
                        for file in source_path.rglob('*'):
                            if file.is_file():
                                # get file name
                                f_name = file.name
                                # get file path
                                f_path = file.as_posix()
                                # get file size
                                f_size = GetFileSize().get_file_size(f_path)
                                # get file hash
                                f_hash = FileHasher().calculate_md5(f_path)
                                high_dic = {
                                    'file_name': f_name,
                                    'file_path': f_path,
                                    'file_size': f_size,
                                    'file_hash': f_hash
                                }
                                all_files['high'].append(high_dic)
                    else:
                        # get file name
                        f_name = file.name
                        # get file path
                        f_path = file.as_posix()
                        # get file size
                        f_size = GetFileSize().get_file_size(f_path)
                        # get file hash
                        f_hash = FileHasher().calculate_md5(f_path)
                        high_dic = {
                            'file_name': f_name,
                            'file_path': f_path,
                            'file_size': f_size,
                            'file_hash': f_hash
                        }
                        all_files['high'].append(high_dic)
            elif key == 'mid':
                for source in source_dir[key]:
                    source_path = Path(source)
                    if source_path.is_dir():
                        for file in source_path.rglob('*'):
                            if file.is_file():
                                # get file name
                                f_name = file.name
                                # get file path
                                f_path = file.as_posix()
                                # get file size
                                f_size = GetFileSize().get_file_size(f_path)
                                mid_dic = {
                                    'file_name': f_name,
                                    'file_path': f_path,
                                    'file_size': f_size
                                }
                                all_files['mid'].append(mid_dic)

                    else:
                        # get file name
                        f_name = file.name
                        # get file path
                        f_path = file.as_posix()
                        # get file size
                        f_size = GetFileSize().get_file_size(f_path)
                        mid_dic = {
                            'file_name': f_name,
                            'file_path': f_path,
                            'file_size': f_size
                        }
                        all_files['mid'].append(mid_dic)
            elif key == 'low':
                for source in source_dir[key]:
                    source_path = Path(source)
                    if source_path.is_dir():
                        for file in source_path.rglob('*'):
                            if file.is_file():
                                # get file name
                                f_name = file.name
                                # get file path
                                f_path = file.as_posix()
                                # get file size
                                f_size = GetFileSize().get_file_size(f_path)
                                low_dic = {
                                    'file_name': f_name,
                                    'file_path': f_path,
                                    'file_size': f_size
                                }
                                all_files['low'].append(low_dic)

                    else:
                        # get file name
                        f_name = file.name
                        # get file path
                        f_path = file.as_posix()
                        # get file size
                        f_size = GetFileSize().get_file_size(f_path)
                        low_dic = {
                            'file_name': f_name,
                            'file_path': f_path,
                            'file_size': f_size
                        }
                        all_files['low'].append(low_dic)

        return all_files

    def insert_all_level_files_data(self, source_dir: Dict[str, List[str]],
                                    dst_path: str) -> None:  # noqa
        '''
        Insert all level files data to database
        param source_dir: Dict[str, List[str]], it contains all level files
        param dst_path: str, the destination path for backup
        return: None
        '''
        all_level_files_data = self.get_all_file_path(source_dir)
        db_exec = DatabaseExec()
        db_exec.add_high_level_files(all_level_files_data['high'])
        db_exec.add_mid_level_files(all_level_files_data['mid'])
        db_exec.add_low_level_files(all_level_files_data['low'])
        db_exec.add_is_backuped(dst_path)

    # 完全备份
    @full_backup_decorator
    def full_file_backup(self, source_dir: Dict[str, List[str]],
                         dest_path: str) -> None:
        '''
        Perform full backup for all level files
        param source_dir: Dict[str, List[str]], it contains all source directories
        param dest_path: str, the destination path for backup
        return: None
        '''  # noqa
        # check system
        system = self.__check_system()
        if system is None:
            # exit and print error info
            print('[-] Unknown system, program exit!')
            exit(1)

        dst_path = Path(dest_path)
        # get high level files
        for key in source_dir.keys():
            for source in source_dir[key]:
                source_path = Path(source)
            if source_path.is_dir():
                dest_dir = dst_path / source_path.name
                dest_dir.mkdir(parents=True, exist_ok=True)
                if self.__check_system():
                    command = self.commands['macOS']['cp_dir'].format(
                        source_path, dest_dir)
                else:
                    command = self.commands['Windows']['cp_dir'].format(
                        source_path, dest_dir)
                self.g_logger.info(f"[+] {source_path.name} backuping...")
            else:
                if self.__check_system():
                    command = self.commands['macOS']['cp_file'].format(
                        source_path, dest_dir)
                else:
                    command = self.commands['Windows']['cp_file'].format(
                        source_path, dest_dir)
                self.g_logger.info(f"[+] {source_path.name} backuping...")

            try:
                subprocess.run(command, shell=True, check=True,
                               capture_output=True, text=True)
                self.g_logger.info(f"[+] {source_path.name} backup successfully!")  # noqa
            except subprocess.CalledProcessError as e:
                self.g_logger.error(f"[-] {source_path.name} backup error: {e.stderr}")  # noqa

        # insert all level files data to database after backup
        self.insert_all_level_files_data(source_dir, dest_path)
