import yaml  # type: ignore
from .global_vars import get_var, set_var  # type: ignore
from typing import Dict, List


class GetConfig:
    def __init__(self) -> None:
        self.config_file = "config/config.yaml"
        self.white_file_level = ['HighLevelFiles', 'MiddleLevelFiles',
                                 'LowLevelFiles']

    def load_yaml(self) -> None:
        '''
        laod yaml file
        '''
        with open(self.config_file, 'r', encoding="utf-8") as f:
            set_var('config', yaml.load(f.read(), Loader=yaml.FullLoader))

    def get_level_files_config(self) -> Dict[str, List[str]]:
        '''
        Get all level files from config.yaml
        return: Dict[str, List[str]], it contains all level files
        '''
        self.load_yaml()
        all_level_dict: Dict[str, List[str]] = {
            'high': [],
            'mid': [],
            'low': []
        }
        # 获取LowLevel
        # 仅当LowLevelFiles有设置时才读取
        if get_var('config')['LowLevelFiles']:
            for FileDict in get_var('config')['LowLevelFiles']:
                for value in FileDict.values():
                    all_level_dict['low'].append(value)

        # get MidLevel
        if get_var('config')['MidLevelFiles']:
            for FileDict in get_var('config')['MidLevelFiles'][1:]:
                for value in FileDict.values():
                    all_level_dict['mid'].append(value)

        # 获取HighLevel
        if get_var('config')['MidLevelFiles']:
            high_dict: list[dict] = get_var('config')['MidLevelFiles'][0].values()  # noqa
            for DictList in high_dict:
                for dic in DictList:
                    for value in dic.values():
                        # mid contains high
                        all_level_dict['mid'].append(value)
                        all_level_dict['high'].append(value)

        return all_level_dict
