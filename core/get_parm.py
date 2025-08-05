import argparse


# 获取参数
def get_parameters() -> argparse.ArgumentParser:
    '''
    获取参数
    '''
    parser = argparse.ArgumentParser(description="用于进行文件的备份")
    parser.add_argument('-o', '--output', type=str, help="请输入要备份到的目录")
    parser.add_argument('-f', '--force', action='store_true', help='强制备份')
    return parser
