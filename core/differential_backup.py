from pathlib import Path
import shutil
from typing import Optional, List, Dict
from .global_vars import get_var
from .decorators import differential_backup_decorator
from .db import DatabaseExec
from .cal_file_hash import FileHasher
from .get_file_size import GetFileSize


class DifferentialBackupFiles():
    def __init__(self):
        self.g_logger = get_var('g_logger')

    def __cal_all_files_size(self, file_sizes: List) -> Optional[str]:
        '''
        Calculate the total size of all files
        param file_sizes: List, it contains all file sizes
        return: str: The total size of all files in a human-readable format
        '''
        file_size_dict = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4,
            'PB': 1024 ** 5
        }
        total_size_bytes = 0.0
        for size_str in file_sizes:
            size, unit = size_str.split()
            size = float(size)
            if unit == 'KB':
                size *= file_size_dict['KB']
            elif unit == 'MB':
                size *= file_size_dict['MB']
            elif unit == 'GB':
                size *= file_size_dict['GB']
            elif unit == 'TB':
                size *= file_size_dict['TB']
            elif unit == 'PB':
                size *= file_size_dict['PB']
            total_size_bytes += size

        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if total_size_bytes < 1024.0:
                return f"{total_size_bytes:.2f} {unit}"
            total_size_bytes /= 1024
        return None

    # 差异备份
    @differential_backup_decorator
    def differential_backup_files(self, source_dir: Dict[str, List[str]],
                                  dest_path: str) -> None:
        '''
        Perform differential backup for high level files
        param source_dir: Dict[str, List[str]], it contains all source directories
        param dest_path: str, the destination path for backup
        return: None
        '''  # noqa
        g_file_size = GetFileSize()
        db_exec = DatabaseExec()
        # 读取已备份好的文件列表
        backuped_file_hashs = db_exec.get_all_high_file_hashes()
        # 新增备份文件的大小
        new_file_sizes: list = []
        # 新增备份文件的数量
        new_file_count = 0

        dst_path = Path(dest_path)
        # 检查目标备份目录是否存在，如果不存在就创建
        if not dst_path.exists():
            dst_path.mkdir(parents=True)
        # high才需要差异备份
        for source in source_dir['high']:
            source_path = Path(source)

            if source_path.is_dir():
                # 取出所有文件
                for file in source_path.rglob('*'):
                    if file.is_file():
                        name = source_path.name
                        # 设置copy到的位置，保持原有目录结构不变
                        dest_file_path = dst_path / name / file.relative_to(source_path)  # noqa
                        dest_file_directory = dest_file_path.parent
                        # 检查目标文件所在的目录是否存在，如果不存在就创建
                        if not dest_file_directory.exists():
                            dest_file_directory.mkdir(parents=True)
                        file_hash = FileHasher().calculate_md5(file.as_posix())
                        if (backuped_file_hashs is not None) and (file_hash not in backuped_file_hashs):  # noqa
                            try:
                                # 执行复制操作
                                # copy2函数必须要路径存在，否则会报错
                                shutil.copy2(file, dest_file_path)
                                # update database
                                db_exec.update_high_file_hash(file.as_posix(), file_hash, True)  # noqa
                                file_size = g_file_size.get_file_size(file.as_posix())  # noqa
                                new_file_sizes.append(file_size)
                                new_file_count += 1
                                self.g_logger.info(f"[+] {file.name} backup successfully")  # noqa
                            except IOError as e:
                                self.g_logger.error(f"[-] {file.name} backup error: {e}")  # noqa
                        else:
                            self.g_logger.info(f"[-] {file.name} 文件HashCode已在数据库中")  # noqa

        self.g_logger.info(f"[+] 差异备份更新文件数量: {new_file_count}")
        total_size = self.__cal_all_files_size(new_file_sizes)
        self.g_logger.info(f"[+] 差异备份更新文件总大小: {total_size}")
        self.g_logger.info("[+] 备份目录下所有文件HashCode已更新完成")
