# Copyright (C) 2018 Alpha Griffin
# @%@~LICENSE~@%@
"""Alpha Griffin Python Printing Utilities

Printing utilities for Python.

.. module:: ag.printing
   :platform: Unix
   :synopsis: Python Starter Project for Alpha Griffin
.. moduleauthor:: Eric Petersen <ruckusist@alphagriffin.com>
"""
import os, subprocess, shlex, platform, datetime

from .__version__ import __version__

# print ("Alpha Griffin Python Printing Utilities version %s detected" % (__version__))

#import ag.logging as log
#log.set(log.INFO)


class Color(object):
    """Console colors that work."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    MAGENTA = '\u001b[35m'
    YELLOW = '\u001b[33m'
    BRIGHT_YELLOW = '\u001b[33;1m'
    BRIGHT_WHITE = '\u001b[37;1m'
    BRIGHT_GREEN = '\u001b[32;1m'
    CYAN = '\u001b[36m'
    # CURSOR
    # all cursor movements require a .format(num of places to move)
    UP          = '\u001b[{n}A'
    DOWN        = '\u001b[{n}B'
    LEFT        = '\u001b[{n}C'
    RIGHT       = '\u001b[{n}D'
    ROW_DOWN    = '\u001b[{n}E'
    ROW_UP      = '\u001b[{n}F'
    CLEARSCREEN = '\u001b[{n}J'.format(n=2)
    # shapes
    SQUARE = '█'  # '\033[219m'
    SQR = u'\u2588'


class Printer(object):
    """
    AG unified print formatter.
    """
    def __init__(self, options=None):
        self.color = Color

        self.working_res = False
        self.res_x, self.res_y = (0,0)

        if options:
            self.options = options
            self.get_resolution()
        else:
            class optionz(object): pass
            self.options = optionz
            self.options.border = '{}'.format(self.color.SQR)
            # self.options.border = self.color.SQR
            self.options.filler = ' '
            self.options.spacer = ' |#|'
            self.options.blocker = '\t'
            self.options.verbose = True
            self.get_resolution(True)
        # END SETUP

    def __call__(self, msg=None):
        if self.working_res:
            self.printt(msg)
        else:
            print(msg)

    def printt(self, data=None, ret=False, time=False, color='magenta'):
        if data is None:
            data = ' '
        else:
            data = ' {}'.format(str(data))

        # fix message size adjusted for borders.
        scr_size = self.res_x - (len(self.options.border) * 2)-1
        # set msg size.
        if time:
            color_time = '[{color}{date:%m-%d-%y|%H:%M:%S}{end}]'.format(
                color=self.color.OKBLUE,
                date=datetime.datetime.now(),
                end=self.color.ENDC
            )
            time_len = len(color_time)
            scr_size = scr_size - time_len + 9
            ender = color_time
        else:
            ender = ''

        if color:
            scr_size += 11
            if 'white' in color:
                COLOR = self.color.BRIGHT_WHITE
            elif 'yellow' in color:
                COLOR = self.color.BRIGHT_YELLOW
            elif 'red' in color:
                COLOR = self.color.FAIL
                scr_size -= 2
            elif 'green' in color:
                COLOR = self.color.BRIGHT_GREEN
            elif 'cyan' in color:
                COLOR = self.color.CYAN
                scr_size -= 2
            elif 'magenta' in color:
                COLOR = self.color.MAGENTA
                scr_size -= 2

            data = '{color}{message}{end}'.format(
                message=data,
                color=COLOR,
                end=self.color.ENDC
            )

        # finish building message
        msg = '{msg:{filler}{align}{size}}'.format(
            msg = data,
            filler = self.options.filler,
            align = '<', # RIGHT align
            size = scr_size
        )
        msg = '{border}{msg}{ender}{border}'.format(
            msg = msg,
            border = self.options.border,
            ender = ender
        )
        if ret:
            return(msg)
        else:
            print(msg)

    def get_resolution(self, OUTPUT=False):
        self.platform = platform.system()
        if OUTPUT: print('Printing to a {} Platform, Getting resolution...'.format(self.platform))
        if 'Linux' in self.platform:
            try:
                self.res_x, self.res_y = self.getTerminalSize()
                self.working_res = True
            except:
                print('failing to get {} resolution.'.format(self.platform))
        elif 'Windows' in self.platform:
            try:
                self.res_x, self.res_y = self._get_terminal_size_windows()
                self.working_res = True
            except:
                print('failing to get {} resolution.'.format(self.platform))
        else:
            print('you have a {} platform... seriously??'.format(self.platform))
            try:
                self.res_x, self.res_y = self.getTerminalSize()
                self.working_res = True
            except:
                print('failing to get {} resolution.'.format(self.platform))
        if self.res_x > 0:
            if OUTPUT: print('Found Terminal Resolution.')
            if OUTPUT: print('*' * self.res_x)
            return True
        else:
            print('No Terminal Resolution found, Using Jupyter settings.')
            return False

    def _get_terminal_size_windows(self):
        """Source: https://gist.github.com/jtriley/1108174"""
        try:
            '''This generally Fails.'''
            from ctypes import windll, create_string_buffer
            # stdin handle is -10
            # stdout handle is -11
            # stderr handle is -12
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom,
                 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex -1, sizey
        except:
            # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
            try:
                '''This generally Works.'''
                # check_call is DEPRICATED. switching to check_output.
                cols = int(subprocess.check_output(shlex.split('tput cols')))
                rows = int(subprocess.check_output(shlex.split('tput lines')))
                return (cols, rows)
            except:
                print('EPIC WINDOWS SYSTEM FAIL.')
                pass
            pass

    def getTerminalSize(self):
        """Source: https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python"""
        # print('checking UNIX terminal size.')
        env = os.environ
        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            except:
                print('cant import stuff')
                return None
            return cr

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
            ### Use get(key[, default]) instead of a try/catch
            #try:
            #    cr = (env['LINES'], env['COLUMNS'])
            #except:
            #    cr = (25, 80)
        return int(cr[1]), int(cr[0])

    def self_test_1(self):
        scr_size = self.res_x - (len(self.options.border) * 2)+5
        self.printt('Working Resolution X:{}, Y: {}'.format(
            self.res_x,
            self.res_y
        ))
