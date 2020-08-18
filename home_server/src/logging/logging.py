# Format
# 2020-08-12 15:45:23:005 | GCP-gateway | ERROR | some text here

# todo: set location of the output
# todo: set owner of the msg, aka who has requested a log
# todo: proper way of setting config
# todo: lock on file system usage


import datetime
import sys
from dataclasses import dataclass, asdict


class Logging:
    min_log_lvl = 10
    log_mode = 'terminal'
    owner = 'LoggingModule'
    file_location = ''

    @dataclass
    class LogLevels:
        critical: int = 50
        error: int = 40
        warning: int = 30
        info: int = 20
        debug: int = 10
        not_set: int = 0

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

    def __init__(self, owner, log_mode):
        self.owner = owner
        self.log_mode = log_mode

    def log(self, msg, log_lvl):
        if log_lvl < self.min_log_lvl:
            return None

        log_msg = self.format_log_msg(msg, log_lvl, current_time=self.get_time(), source=self.owner)
        if self.log_mode == 'terminal':
            self.write_to_terminal(log_msg, log_lvl)
        elif self.log_mode == 'file':
            # lock
            # write to file
            pass
        elif self.log_mode == 'test':
            return log_msg
        else:
            pass

    def write_to_terminal(self, log_msg, log_lvl):
        output_format = self.get_output_format(log_lvl)
        sys.stdout.write(output_format)
        print(log_msg)
        sys.stdout.write(self.Colours.reset)

    def get_output_format(self, log_lvl):
        if log_lvl == self.LogLevels.critical:
            return self.Colours.magenta
        elif log_lvl == self.LogLevels.error:
            return self.Colours.red
        elif log_lvl == self.LogLevels.warning:
            return self.Colours.yellow
        elif log_lvl == self.LogLevels.info:
            return self.Colours.reset
        elif log_lvl == self.LogLevels.debug:
            return self.Colours.bold
        elif log_lvl == self.LogLevels.not_set:
            return self.Colours.reset

    @staticmethod
    def get_time():
        return datetime.datetime.now()

    def format_log_msg(self, msg, log_lvl, current_time, source):
        log_levels = asdict(self.LogLevels())
        log_lvl_key = list(log_levels.keys())[list(log_levels.values()).index(log_lvl)]
        return '{} - {} | {} : {}'.format(current_time, source, log_lvl_key, msg)

    def set_log_lvl(self, log_lvl):
        self.min_log_lvl = log_lvl

    def critical(self, msg):
        self.log(msg, log_lvl=self.LogLevels.critical)

    def error(self, msg):
        self.log(msg, log_lvl=self.LogLevels.error)

    def warning(self, msg):
        self.log(msg, log_lvl=self.LogLevels.warning)

    def info(self, msg):
        self.log(msg, log_lvl=self.LogLevels.info)

    def debug(self, msg):
        self.log(msg, log_lvl=self.LogLevels.debug)

    def not_set(self, msg):
        self.log(msg, log_lvl=self.LogLevels.not_set)


if __name__ == '__main__':
    log = Logging(owner='testing', log_mode='terminal')
    log.set_log_lvl(log.LogLevels.debug)
    time = '2020-08-14 15:56:36.678644'
    source_ = 'test'
    #print(log.format_log_msg('test123', 20, time, source_))
    #print(log.format_log_msg('test123', 30, time, source_))
    log.not_set('test....')
    log.debug('test....')
    log.info('test....')
    log.warning('test....')
    log.error('test....')
    log.critical('test....')
    #print(log.construct_log_msg('a', '20', 20, time))
