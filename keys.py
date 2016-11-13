#!/usr/bin/env python

# Put future imports here

# Put Python imports here
import sys
import tty
import termios
import subprocess

# Put searchCmd imports here
from searchCmdApp import write_to_clipboard


class GetCharacter:
    def __init__(self):
        pass

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = ''
            while True:
                ch += sys.stdin.read(1)
                if ch != '\x1b' and ch != '\x1b[':
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class DisplayBuffer:
    lines = []
    search_str = ''
    y = 0
    x = 0
    key_actions = {}
    invalid_keys = []

    def __init__(self):
        self.refresh_output()
        self.key_actions = {
            '\x1b[A': self.up_key_handler,
            '\x1b[B': self.down_key_handler,
            '\x1b[C': self.right_key_handler,
            '\x1b[D': self.left_key_handler,
            '\x7f': self.delete_key_handler,
            '\r': self.return_key_handler,
        }
        self.invalid_keys = [27, 127, 9, 13]

    def insert_key_handler(self, ch):
        if not self.y:
            self.search_str = self.search_str[:self.x] + ch \
                              + self.search_str[self.x:]
            self.x += 1
            self.search()

    def delete_key_handler(self):
        if not self.y and self.x:
            self.search_str = self.search_str[:self.x - 1] \
                              + self.search_str[self.x:]
            self.x -= 1
            self.search()

    def up_key_handler(self):
        if self.y:
            self.y -= 1

    def down_key_handler(self):
        if self.y < len(self.lines):
            self.y += 1

    def left_key_handler(self):
        if not self.y and self.x:
            self.x -= 1

    def right_key_handler(self):
        if not self.y and self.x < len(self.search_str):
            self.x += 1

    def return_key_handler(self):
        if self.lines:
            write_to_clipboard(self.lines[self.y - 1] if self.y else self.lines[0])
        self.clear_screen()
        exit()

    def is_insert_key(self, ch):
        if ord(ch) in self.invalid_keys:
            return False
        else:
            return True

    def execute_key_handler(self, ch):
        if ch in self.key_actions:
            self.key_actions[ch]()
        elif self.is_insert_key(ch):
            self.insert_key_handler(ch)

        self.refresh_output()

    def refresh_output(self):
        self.clear_screen()
        self.display_search_str()
        self.display_search_result()
        self.move_cur_up(len(self.lines) + 1)
        self.move_cur_right(self.x+1)

    def display_search_str(self):
        in_str = self.search_str + ' '
        pos = self.x
        out_str = '>'
        if not self.y:
            out_str += in_str[:pos] + self.highlight_str(in_str[pos]) + in_str[pos + 1:]
        else:
            out_str += in_str

        out_str += '\n'
        sys.stdout.write(out_str)

    def display_search_result(self):
        lines = self.lines
        out_lines = ''
        for idx, line in enumerate(lines):
            if idx + 1 == self.y:
                out_lines += self.highlight_str(line) + '\n'
            else:
                out_lines += line + '\n'

        sys.stdout.write(out_lines)

    def clear_screen(self):
        self.clear_line(len(self.lines)+1)

    @staticmethod
    def highlight_str(string):
        return '\033[7m' + string + '\033[0m'

    @staticmethod
    def clear_line(lines=1):
        sys.stdout.write('\033[K\n' * lines)
        DisplayBuffer.move_cur_up(lines)

    @staticmethod
    def term_reset():
        sys.stdout.write('\033[0m')

    @staticmethod
    def term_hl_on():
        sys.stdout.write('\033[7m')

    @staticmethod
    def move_cur_up(lines=1):
        sys.stdout.write('\033[{0}A'.format(lines))
        sys.stdout.flush()

    @staticmethod
    def move_cur_down(lines=1):
        sys.stdout.write('\033[{0}B'.format(lines))
        sys.stdout.flush()

    @staticmethod
    def move_cur_right(col=1):
        sys.stdout.write('\033[{0}C'.format(col))
        sys.stdout.flush()

    @staticmethod
    def move_cur_left(col=1):
        sys.stdout.write('\033[{0}D'.format(col))
        sys.stdout.flush()

    @staticmethod
    def get_col_width():
        return int(subprocess.check_output(['stty', 'size']).split()[1])

    def search(self):
        self.lines = [self.search_str] * 5


def main():
    get_character = GetCharacter()
    display_content = DisplayBuffer()
    while True:
        ip_char = get_character()
        if ip_char == '\x03':
            break
        display_content.execute_key_handler(ip_char)


if __name__ == '__main__':
    main()

