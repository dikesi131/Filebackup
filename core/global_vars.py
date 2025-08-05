from typing import Any


GLOBALS_DICT = dict()


# 注：_init()只需要在程序一开始调用的模块调用即可
# 使用set和get方法的目的是为了实现多模块共享全局变量，避免全局变量命名空间不同从而逻辑出错的问题
def _init():
    """在主模块初始化"""
    global GLOBALS_DICT
    # 设置全局变量默认值
    GLOBALS_DICT = {
        # 配置项
        "config": None,
        # 日志变量
        "g_logger": None,
        # 用于存放不同级别的文件/目录
        # 分别对应level 0 1 2
        "high_level_files": list(),
        "middle_level_files": list(),
        "low_level_files": list(),
    }


# 用于设置全局变量
def set_var(name: str, value: Any) -> bool:
    """设置Config"""
    try:
        global GLOBALS_DICT
        GLOBALS_DICT[name] = value
        return True
    except KeyError:
        return False


# 用于获取全局变量
def get_var(name: str) -> Any:
    """取值Config"""
    try:
        global GLOBALS_DICT
        return GLOBALS_DICT[name]
    except KeyError:
        return "Not Found"
