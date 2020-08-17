import unittest

from home_server.src.logging.logging import Logging


class TestLogging(unittest.TestCase):
    log = Logging()

    def test_different_log_levels(self):
        msg = 'a'
        time = '2020-08-14 15:56:36.678644'
        source = 'a'
        log_levels = [0, 10, 20, 30, 40, 50]
        truth_list = ['2020-08-14 15:56:36.678644 - a | not_set : a', '2020-08-14 15:56:36.678644 - a | debug : a',
                      '2020-08-14 15:56:36.678644 - a | info : a', '2020-08-14 15:56:36.678644 - a | warning : a',
                      '2020-08-14 15:56:36.678644 - a | error : a', '2020-08-14 15:56:36.678644 - a | critical : a']
        for index, log_lvl in enumerate(log_levels):
            test_result = self.log.format_log_msg(msg, log_lvl, time, source)
            self.assertEqual(test_result, truth_list[index])
