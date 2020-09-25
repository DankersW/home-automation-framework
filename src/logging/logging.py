# Format
# 2020-08-12 15:45:23:005 | GCP-gateway | ERROR | some text here

# todo: set location of the output
# todo: proper way of setting config
# todo: lock on file system usage

import datetime
import sys
from dataclasses import dataclass, asdict
from ntpath import split, basename

import yaml


@dataclass
class LogLevels:
    critical: int = 60
    error: int = 50
    warning: int = 40
    success: int = 30
    info: int = 20
    debug: int = 10
    not_set: int = 0


class Logging:

    @dataclass
    class Colours:
        black: str = '\033[1;30m'
        red: str = '\033[1;31m'
        green: str = '\033[0;32m'
        yellow: str = '\033[0;33m'
        blue: str = '\033[1;34m'
        magenta: str = '\033[1;35m'
        cyan: str = '\033[1;36m'
        white: str = '\033[1;37m'
        bold: str = '\033[;1m'
        reset: str = '\033[0;0m'

    def __init__(self, owner, log_mode='test', min_log_lvl=LogLevels.debug):
        self.owner = self.path_leaf(path=owner)
        self.log_mode = log_mode
        self.min_log_lvl = min_log_lvl
        self.filename = self.get_filename_from_config()

    def log(self, msg, log_lvl):
        if log_lvl < self.min_log_lvl:
            return None

        log_msg = self.format_log_msg(msg, log_lvl, current_time=self.get_time(), source=self.owner)
        if self.log_mode == 'terminal':
            self.write_to_terminal(log_msg, log_lvl)
        elif self.log_mode == 'file':
            self.write_to_file(log_msg)
        elif self.log_mode == 'test':
            return log_msg
        else:
            pass
        return None

    def write_to_file(self, log_msg):
        with open(self.filename, "a") as file:
            file.write(log_msg + '\n')
        file.close()

    def write_to_terminal(self, log_msg, log_lvl):
        output_format = self.get_output_format(log_lvl)
        sys.stdout.write(output_format)
        print(log_msg)
        sys.stdout.write(self.Colours.reset)

    def get_output_format(self, log_lvl):
        mapper = {
            LogLevels.critical: self.Colours.magenta,
            LogLevels.error: self.Colours.red,
            LogLevels.warning: self.Colours.yellow,
            LogLevels.success: self.Colours.green,
            LogLevels.info: self.Colours.reset,
            LogLevels.debug: self.Colours.bold,
            LogLevels.not_set: self.Colours.reset
        }
        return mapper.get(log_lvl, self.Colours.reset)

    @staticmethod
    def get_time():
        return datetime.datetime.now()

    @staticmethod
    def format_log_msg(msg, log_lvl, current_time, source):
        log_levels = asdict(LogLevels())
        log_lvl_key = list(log_levels.keys())[list(log_levels.values()).index(log_lvl)]
        return f'{current_time} - {source} | {log_lvl_key} : {msg}'

    @staticmethod
    def get_filename_from_config_yml():
        with open('configuration.yml') as file:
            configuration = yaml.load(file, Loader=yaml.FullLoader)
        return configuration['logging']['filename']

    @staticmethod
    def get_filename_from_config():
        return 'log.txt'

    def set_log_lvl(self, log_lvl):
        self.min_log_lvl = log_lvl

    def critical(self, msg):
        self.log(msg, log_lvl=LogLevels.critical)

    def error(self, msg):
        self.log(msg, log_lvl=LogLevels.error)

    def warning(self, msg):
        self.log(msg, log_lvl=LogLevels.warning)

    def success(self, msg):
        self.log(msg, log_lvl=LogLevels.success)

    def info(self, msg):
        self.log(msg, log_lvl=LogLevels.info)

    def debug(self, msg):
        self.log(msg, log_lvl=LogLevels.debug)

    def not_set(self, msg):
        self.log(msg, log_lvl=LogLevels.not_set)

    @staticmethod
    def path_leaf(path):
        head, tail = split(path)
        file_name = tail or basename(head)
        return file_name.split('.')[0]


def run_loglvls():
    log = Logging(owner=__file__, log_mode='terminal', min_log_lvl=LogLevels.debug)
    log.set_log_lvl(LogLevels.debug)
    log.not_set('test....')
    log.debug('test....')
    log.info('test....')
    log1 = Logging(owner='extra', log_mode='terminal', min_log_lvl=LogLevels.debug)
    log1.warning('test....')
    log1.error('test....')
    log1.critical('test....')
    log1.success('test....')
    log.debug('test....')


if __name__ == '__main__':
    run_loglvls()
