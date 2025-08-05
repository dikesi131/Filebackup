from .global_vars import _init, set_var, get_var  # type: ignore
import time
import logging


class Logger:
    def __init__(self) -> None:
        self.log_format = '%(asctime)s:%(msecs)d %(name)s \
            %(levelname)s %(message)s'
        self.log_datefmt = '%Y-%m-%d %H:%M:%S'
        # init global vars
        _init()

    # 日志初始化
    def init_logger(self) -> None:
        '''
        init logger
        '''
        # 设置文件日志处理程序
        file_handler = logging.FileHandler('access.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 设置日志记录器
        logging.basicConfig(level=logging.DEBUG,
                            filemode='w',
                            format=self.log_format,
                            datefmt=self.log_datefmt)
        # 创建日志记录器
        set_var('g_logger', logging.getLogger(__name__))

        get_var('g_logger').setLevel(logging.INFO)
        # g_logger.addHandler(console_handler)
        get_var('g_logger').addHandler(file_handler)

    # 预处理
    def pretreatment(self) -> None:
        self.init_logger()
        # 添加工具开头标志加入日志
        starting_banner = ('\n' + '-' * 70 + '\n' +
                           f"\n\tStarted At {time.ctime()}  @Athouer:d1k3si"
                           + '\n\temail: d1k3siy@gmail.com'
                           + '\n\n' + '-' * 70 + '\n')
        get_var('g_logger').info(f"{starting_banner}")
