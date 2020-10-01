from pathlib import Path
from os import path, sep


class ConfigurationParser:
    repo_name = 'home-automation-framework'
    # todo: let each init call this class
    # todo: return a dict with the configuration

    def __init__(self):
        conf_file_path = self.get_path_to_conf_file()
        conf_dict = self.conf_to_dict(file_path=conf_file_path)

    def get_path_to_conf_file(self):
        dir_structure = path.normpath(Path.cwd()).split(sep)
        index_repo_name = dir_structure.index(self.repo_name)
        project_home = Path(*dir_structure[:index_repo_name + 1])
        return Path.joinpath(project_home, 'configuration.yml')

    def conf_to_dict(self, file_path):
        return dict
