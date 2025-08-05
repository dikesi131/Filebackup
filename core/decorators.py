from .global_vars import get_var  # type: ignore
from .db import DatabaseExec
from .get_file_size import GetFileSize  # type: ignore
import time


db_exec = DatabaseExec()
g_file_size = GetFileSize()


# 完全备份函数修饰器
def full_backup_decorator(func):
    def wrapper(*args, **kwargs):
        get_var('g_logger').info("[+] Full Backup Start")
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        time_format = '%H:%M:%S'
        high_file_size = g_file_size.add_all_high_file_size()
        mid_file_size = g_file_size.add_all_mid_file_size()
        high_file_count = db_exec.get_all_high_file_count()
        mid_file_count = db_exec.get_all_mid_file_count()
        # Ensure counts are integers, not None
        high_file_count = high_file_count if high_file_count is not None else 0
        mid_file_count = mid_file_count if mid_file_count is not None else 0
        cost_time = time.strftime(time_format,
                                  time.gmtime(end_time - start_time))
        get_var('g_logger').info("[-] Full Backup End")
        get_var('g_logger').info(f"[+] The high level files size {high_file_size}")  # noqa
        get_var('g_logger').info(f"[+] The mid level files size {mid_file_size}")  # noqa
        get_var('g_logger').info(f"[+] All Files Count Is {high_file_count + mid_file_count}")  # noqa
        get_var("g_logger").info(f"[-] The Cost Time Is {cost_time}")

    return wrapper


# 增量备份函数修饰器
def incremental_backup_decorator(func):
    def wrapper(*args, **kwargs):
        get_var('g_logger').info("[+] Incremental Backup Start")
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        time_format = '%H:%M:%S'
        cost_time = time.strftime(time_format,
                                  time.gmtime(end_time - start_time))
        get_var('g_logger').info("[-] Incremental Backup End")
        get_var("g_logger").info(f"[-] The Cost Time Is {cost_time}")

    return wrapper


# 差异备份函数修饰器
def differential_backup_decorator(func):
    def wrapper(*args, **kwargs):
        get_var("g_logger").info("[+] Differential Backup Start")
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        time_format = '%H:%M:%S'
        cost_time = time.strftime(time_format,
                                  time.gmtime(end_time - start_time))
        get_var("g_logger").info("[-] Differential Backup End")
        get_var("g_logger").info(f"[-] The Cost Time Is {cost_time}")

    return wrapper


# 计算程序运行时间的装饰器
def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_format = '%H:%M:%S'
        elapsed_time = time.strftime(time_format,
                                     time.gmtime(end_time - start_time))
        get_var('g_logger').info(f"[-] Execution time: {elapsed_time:.2f} seconds")  # noqa
        return result

    return wrapper
