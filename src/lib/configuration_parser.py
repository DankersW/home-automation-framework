from pathlib import Path
from os import path, sep, system
import yaml


class ConfigurationParser:
    repo_name = 'home-automation-framework'

    def get_config(self):
        conf_file_path = self.get_path_to_conf_file()
        return self.yml_to_dict(file_path=conf_file_path)

    def get_path_to_conf_file(self):
        dir_structure = path.normpath(Path.cwd()).split(sep)
        if dir_structure[0] == 'C:' or dir_structure[0] == 'D:' or dir_structure[0] == 'E:':  # Solve Windows path
            dir_structure[0] += f'\\'
        elif dir_structure[0] == '':  # Solve Github actions location error
            dir_structure[0] = '/'
        index_repo_name = [i for i, x in enumerate(dir_structure) if x == self.repo_name][-1]
        project_home = Path(*dir_structure[:index_repo_name + 1])
        return Path.joinpath(project_home, 'configuration.yml')

    @staticmethod
    def yml_to_dict(file_path):
        with open(file_path) as yml_file:
            return yaml.load(yml_file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    conf = ConfigurationParser()
    conf.get_path_to_conf_file()