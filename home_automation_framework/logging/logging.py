from datetime import datetime
import sys
from dataclasses import dataclass, asdict
from ntpath import split, basename
from pathlib import Path

from lib.configuration_parser import ConfigurationParser
from home_automation_framework.logging.persistent_logging import DbLogging


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

    def __init__(self, owner, log_mode='test', min_log_lvl=LogLevels.debug, config=False):
        self.config = ConfigurationParser().get_config()
        self.owner = self._path_leaf(path=owner)
        self.log_mode = log_mode
        self.min_log_lvl = min_log_lvl

        if config:
            self.log_mode = self.config['general']['logging_mode']
            self.min_log_lvl = self._get_log_lvl_from_config()

        if self.log_mode == 'db':
            self.db = DbLogging()
            self.db.connect()

        if self.log_mode == 'file':
            self.filename = self._get_filename()

    def _log(self, msg, log_lvl):
        if log_lvl < self.min_log_lvl:
            return None

        log_msg = self._format_log_msg(msg, log_lvl, current_time=self._get_time(), source=self.owner)
        if self.log_mode == 'terminal':
            self._write_to_terminal(log_msg, log_lvl)
        elif self.log_mode == 'file':
            self._write_to_file(log_msg)
        elif self.log_mode == 'db' and self.db:
            self.db.log(source=self.owner, time=self._get_time(), log_lvl=self._get_key_from_dict(log_lvl), msg=msg)
        elif self.log_mode == 'test':
            return log_msg
        else:
            pass
        return None

    def _write_to_file(self, log_msg):
        with open(self.filename, "a") as file:
            file.write(log_msg + '\n')
        file.close()

    def _write_to_terminal(self, log_msg, log_lvl):
        output_format = self._get_output_format(log_lvl)
        sys.stdout.write(output_format)
        print(log_msg)
        sys.stdout.write(self.Colours.reset)

    def _get_output_format(self, log_lvl):
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
    def _get_time():
        return datetime.now()

    @staticmethod
    def _get_key_from_dict(val):
        log_levels = asdict(LogLevels())
        return list(log_levels.keys())[list(log_levels.values()).index(val)]

    def _format_log_msg(self, msg, log_lvl, current_time, source):
        log_lvl_key = self._get_key_from_dict(log_lvl)
        return f'{current_time} - {source} | {log_lvl_key} : {msg}'

    def _get_filename(self):
        log_folder = self.config['logging']['file_log_folder']
        dt = datetime.now().strftime('%Y%m%d%H%M')
        filename = f'logs-{dt}'
        return Path(log_folder, filename)

    def _set_log_lvl(self, log_lvl):
        self.min_log_lvl = log_lvl

    def critical(self, msg):
        self._log(msg, log_lvl=LogLevels.critical)

    def error(self, msg):
        self._log(msg, log_lvl=LogLevels.error)

    def warning(self, msg):
        self._log(msg, log_lvl=LogLevels.warning)

    def success(self, msg):
        self._log(msg, log_lvl=LogLevels.success)

    def info(self, msg):
        self._log(msg, log_lvl=LogLevels.info)

    def debug(self, msg):
        self._log(msg, log_lvl=LogLevels.debug)

    def not_set(self, msg):
        self._log(msg, log_lvl=LogLevels.not_set)

    @staticmethod
    def _path_leaf(path):
        head, tail = split(path)
        file_name = tail or basename(head)
        return file_name.split('.')[0]

    def _get_log_lvl_from_config(self):
        conf_lvl = self.config['logging']['min_log_level']
        return LogLevels.__dict__.get(conf_lvl)


def run_loglvls():
    log = Logging(owner=__file__, config=True)
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
