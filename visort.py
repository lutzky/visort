#!/usr/bin/python

import curses
import time
import sys
import fcntl
import os
import select

def blocking_read(stream):
    r = None

    while not r:
        r, w, x = select.select([sys.stdin], [], [])

    return r[0].read()

def main(stdscr, instream, make_nonblocking=True, blocking_read=blocking_read):
    if make_nonblocking:
        fcntl.fcntl(instream.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    lines = []

    try:
        height, width = stdscr.getmaxyx()

        new_line_starting = True

        while True:
            new_data = blocking_read(instream)

            if not new_data:
                return (lines, None)

            if new_line_starting:
                lines.append(new_data.rstrip())
            else:
                lines[-1] = lines[-1] + new_data.rstrip()

            new_line_starting = new_data.endswith("\n")

            lines_for_screen = sorted(lines)[0:height - 1]

            for i, line in enumerate(lines_for_screen):
                stdscr.addstr(i, 0, line[0:width - 1])
            stdscr.refresh()
    except KeyboardInterrupt, ex:
        return (lines, repr(ex))

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    result = None

    try:
        result, ex = main(stdscr, sys.stdin)
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    if ex:
        print >>sys.stderr, "WARNING: Got", ex
    if result:
        print "\n".join(sorted(result))
