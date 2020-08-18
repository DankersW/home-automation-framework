import unittest

from home_server.src.logging.logging import Logging


class TestLogging(unittest.TestCase):
    def test_different_log_levels(self):
        log = Logging(owner='a', log_mode='test')
        msg = 'a'
        time = '2020-08-14 15:56:36.678644'
        source = 'a'
        log_levels = [0, 10, 20, 30, 40, 50]
        truth_list = ['2020-08-14 15:56:36.678644 - a | not_set : a', '2020-08-14 15:56:36.678644 - a | debug : a',
                      '2020-08-14 15:56:36.678644 - a | info : a', '2020-08-14 15:56:36.678644 - a | warning : a',
                      '2020-08-14 15:56:36.678644 - a | error : a', '2020-08-14 15:56:36.678644 - a | critical : a']
        for index, log_lvl in enumerate(log_levels):
            test_result = log.format_log_msg(msg, log_lvl, time, source)
            self.assertEqual(test_result, truth_list[index])

    def test_set_log_lvl(self):
        log = Logging(owner='t', log_mode='test')
        msg = 'a'
        log_levels = [0, 20, 40, 0, 40, 50]
        min_log_lvls = [10, 10, 50, 10, 0, 40]
        truth_list = [None, 't | info : a', None, None, 't | error : a', 't | critical : a']
        for truth, log_lvl, min_log_lvl in zip(truth_list, log_levels, min_log_lvls):
            log.set_log_lvl(min_log_lvl)
            helper = str(log.log(msg, log_lvl))
            test_result = helper.split(' - ')[-1]
            self.assertEqual(test_result, str(truth))

    def test_output_format(self):
        log = Logging(owner='t', log_mode='test')
        truth_list = ['\033[1;35m', '\033[1;31m', '\033[0;33m', '\033[0;0m', '\033[;1m', '\033[0;0m']
        log_levels = [log.LogLevels.critical, log.LogLevels.error, log.LogLevels.warning, log.LogLevels.info,
                      log.LogLevels.debug, log.LogLevels.not_set]
        for truth, log_lvl in zip(truth_list, log_levels):
            test_result = log.get_output_format(log_lvl)
            self.assertEqual(test_result, truth)