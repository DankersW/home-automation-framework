# Format
# 2020-08-12 15:45:23:005 | GCP-gateway | ERROR | some text here

# todo: set location of the output
# todo: set owner of the msg, aka who has requested a log
# todo: proper way of setting config


import datetime
from dataclasses import dataclass


class Logging:

    @dataclass
    class LogLevels:
        critical: int = 50
        error: int = 40
        warning: int = 30
        info: int = 20
        debug: int = 10
        not_set: int = 0

    min_log_lvl = 10
    log_mode = ''
    owner = 'LoggingModule'
    file_location = ''

    def __init__(self):
        pass

    def log(self, msg, log_lvl):
        if log_lvl < self.min_log_lvl:
            return

        log_msg = self.construct_log_msg(msg, log_lvl, current_time=self.get_time())
        if self.log_mode == 'print':
            print(log_msg)
        elif self.log_mode == 'file':
            # write to file
            pass
        else:
            pass

    @staticmethod
    def get_time():
        return datetime.datetime.now()

    @staticmethod
    def construct_log_msg(msg, log_lvl, current_time, source):
        return '{} - {} | {} : {}'.format(current_time, source, log_lvl, msg)

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
    log = Logging()
    time = '2020-08-14 15:56:36.678644'
    print(log.construct_log_msg('test123', 20, time))
    #print(log.construct_log_msg('a', '20', 20, time))
