from pathlib import Path
from os import path, sep
from typing import Union, NamedTuple
from collections import namedtuple
import yaml


class ConfigurationParser:
    repo_name = 'home-automation-framework'

    def get_config(self) -> dict:
        conf_file_path = self._get_path_to_conf_file()
        return self._yml_to_dict(file_path=conf_file_path)

    def as_named_tuple(self) -> NamedTuple:
        a = self.get_config()
        print(a)

    def _get_path_to_conf_file(self) -> Path:
        dir_structure = path.normpath(Path.cwd()).split(sep)
        if dir_structure[0] == 'C:' or dir_structure[0] == 'D:' or dir_structure[0] == 'E:':  # Solve Windows path
            dir_structure[0] += '\\'
        elif dir_structure[0] == '':  # Solve Github actions location error
            dir_structure[0] = '/'
        index_repo_name = [i for i, x in enumerate(dir_structure) if x == self.repo_name][-1]
        project_home = Path(*dir_structure[:index_repo_name + 1])
        return Path.joinpath(project_home, 'configuration.yml')

    @staticmethod
    def _yml_to_dict(file_path: Path) -> Union[dict, list, None]:
        with open(file_path) as yml_file:
            return yaml.safe_load(yml_file)
