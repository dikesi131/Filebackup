from pathlib import Path
import shutil
from typing import Optional, List, Dict
from .global_vars import get_var
from .decorators import incremental_backup_decorator
from .db import DatabaseExec
from .get_file_size import GetFileSize


class IncrementalBackup():
    def __init__(self) -> None:
        self.g_logger = get_var('g_logger')
        self.db_exec = DatabaseExec()

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

    @incremental_backup_decorator
    def incremental_backups_files(self, source_dic: Dict[str, List[str]],
                                  dest_path: str) -> None:
        '''
        Perform incremental backup for mid level files
        param source_dic: Dict[str, List[str]], it contains all source directories
        param dest_path: str, the destination path for backup
        return: None
        '''  # noqa

        # 读取已备份好的文件列表
        db_exec = self.db_exec
        # 获取数据库中所有的备份文件路径
        backup_files = db_exec.get_all_mid_file_paths()
        # 用来存储新增备份文件的信息
        new_file_list: list[Dict] = []
        # 用来存储新增备份文件的大小
        new_file_sizes: list[str] = []
        # 存储新增备份文件的个数
        new_files_num = 0

        dst_path = Path(dest_path)
        # 检查目标备份目录是否存在，如果不存在就创建
        if not dst_path.exists():
            dst_path.mkdir(parents=True)
        # mid才需要增量备份
        for source in source_dic['mid']:
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
                        # 通过切片操作把盘符去掉
                        if (backup_files is not None) and (file.as_posix() not in backup_files):  # noqa
                            try:
                                # 执行复制操作
                                # copy2函数必须要路径存在，否则会报错
                                shutil.copy2(file, dest_file_path)
                                # update数据库
                                new_file_dic = {
                                    'file_name': file.name,
                                    'file_path': file.as_posix(),
                                    'file_size': GetFileSize().get_file_size(file.as_posix()),  # noqa
                                    'is_new_add': True
                                }
                                new_file_list.append(new_file_dic)
                                new_file_sizes.append(new_file_dic['file_size'])  # noqa
                                new_files_num += 1
                                self.g_logger.info(f"[+] {file.name} backup successfully")  # noqa
                            except IOError as e:
                                self.g_logger.error(f"[-] {file.name} backup error: {e}")  # noqa
                        else:
                            self.g_logger.info(f"[-]{file.name} 已在备份文件列表中")  # noqa

        # update database
        db_exec.add_mid_level_files(new_file_list)
        new_backup_size = self.__cal_all_files_size(new_file_sizes)
        self.g_logger.info(f"[+] 新增备份文件的个数为: {new_files_num}")
        self.g_logger.info(f"[+] 新增备份文件的大小为: {new_backup_size}")
        self.g_logger.info("[+] 备份目录下所有文件名已更新完成")
