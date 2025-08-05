from pathlib import Path
from .global_vars import get_var  # type: ignore
from .db import DatabaseExec
import sys


class CheckIsBackup:
    def __init__(self) -> None:
        pass

    # 用于检测是否已经有过备份
    def is_backuped_path(self, dst_path: str) -> bool:
        '''
        check if the backup file exists
        param dst_path: str: The path to the backup file
        return: bool: True if the backup file exists, False otherwise
        '''
        db_exec = DatabaseExec()
        path = Path(dst_path)
        if not path.exists():
            get_var('g_logger').error("[ERROR] 备份文件路径不存在")
            sys.exit(1)

        if dst_path in db_exec.get_all_backuped_dir_paths():  # type: ignore
            return True
        else:
            return False
