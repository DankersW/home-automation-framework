# Format
# 2020-08-12 15:45:23:005 | GCP-gateway | ERROR | some text here

# todo: set owner of the msg, aka who has requested a log


class Logging:
    def __init__(self):
        pass

    def construct_log_msg(self, msg, log_lvl):
        pass

    def critical(self, msg):
        self.construct_log_msg(msg, log_lvl=50)

    def error(self, msg):
        self.construct_log_msg(msg, log_lvl=40)

    def warning(self, msg):
        self.construct_log_msg(msg, log_lvl=30)

    def info(self, msg):
        self.construct_log_msg(msg, log_lvl=20)

    def debug(self, msg):
        self.construct_log_msg(msg, log_lvl=10)

    def not_set(self, msg):
        self.construct_log_msg(msg, log_lvl=0)
