#!/usr/bin/python

import unittest
import mock
import visort

class TestVisort(unittest.TestCase):
    def testSimply(self):
        mock_stdscr = mock.Mock()
        mock_blocking_read = mock.Mock(side_effect = [
            'hello\n',
            'world\n',
            'hello\n',
            'world\n',
            ''
            ])

        mock_stdscr.getmaxyx = mock.Mock(return_value = (3, 5))
        mock_stdscr.addstr = mock.Mock()

        result, ex = visort.main(mock_stdscr, None, make_nonblocking = False,
            blocking_read = mock_blocking_read)

        mock_stdscr.addstr.assert_has_calls([
                mock.call(0, 0, 'hell'),
                mock.call(1, 0, 'worl'),
                mock.call(0, 0, 'hell'),
                mock.call(1, 0, 'hell'),
                mock.call(0, 0, 'hell'),
                mock.call(1, 0, 'hell')
                ])

        self.assertEquals(None, ex)
        self.assertEquals(['hello','hello','world','world'], sorted(result))
