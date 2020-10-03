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
        print(dir_structure)
        print(f'from lib {system("ls -lS")}')
        print(system("pwd"))
        if dir_structure[0] == 'C:' or dir_structure[0] == 'D:' or dir_structure[0] == 'E:':
            dir_structure[0] += f'\\'
        elif dir_structure[0] == '':
            dir_structure[0] = '/'
        index_repo_name = [i for i, x in enumerate(dir_structure) if x == self.repo_name][-1]
        #index_repo_name = dir_structure.index(self.repo_name)
        print(index_repo_name)
        project_home = Path(*dir_structure[:index_repo_name + 1])
        print(f'project home {project_home}')
        print(f'home location {system(f"ls -lS /{project_home}/")}')
        pat = Path.joinpath(project_home, 'configuration.yml')
        print(f'Path to file : {pat}')
        return pat

    @staticmethod
    def yml_to_dict(file_path):
        dir_structure = path.normpath(Path.cwd()).split(sep)
        print(f'Dir sturct: {dir_structure}')
        with open(file_path) as yml_file:
            return yaml.load(yml_file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    conf = ConfigurationParser()
    conf.get_path_to_conf_file()