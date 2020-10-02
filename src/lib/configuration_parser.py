from pathlib import Path
from os import path, sep
import yaml


class ConfigurationParser:
    repo_name = 'home-automation-framework'

    def get_config(self):
        conf_file_path = self.get_path_to_conf_file()
        return self.yml_to_dict(file_path=conf_file_path)

    def get_path_to_conf_file(self):
        dir_structure = path.normpath(Path.cwd()).split(sep)
        print(dir_structure)
        if dir_structure[0] == 'C:' or dir_structure[0] == 'D:' or dir_structure[0] == 'E:':
            dir_structure[0] += f'\\'
        index_repo_name = dir_structure.index(self.repo_name)
        project_home = Path(*dir_structure[:index_repo_name + 1])
        return Path.joinpath(project_home, 'configuration.yml')

    @staticmethod
    def yml_to_dict(file_path):
        with open(file_path) as yml_file:
            return yaml.load(yml_file, Loader=yaml.FullLoader)
