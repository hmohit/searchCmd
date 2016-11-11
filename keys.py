<<<<<<< cfb5f295a319df4e4c11c2ef4843c2114d4e719f
#!/usr/bin/env python

# Put future imports here

# Put Python imports here
import sys
import tty
import termios
import subprocess

# Put searchCmd imports here
from searchCmdApp import write_to_clipboard

class _Getch:
    def __init__(self):
        pass

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
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
        self.key_actions = {
            '\x1b[A': self.up_key_handler,
            '\x1b[B': self.down_key_handler,
            '\x1b[C': self.right_key_handler,
            '\x1b[D': self.left_key_handler,
            '\x7f': self.delete_key_handler,
            '\r': self.return_key_handler,
        }
        self.invalid_keys = [27, 127, 9, 13, 65, 66, 67, 68]

    def insert_key_handler(self, ch):
        if not self.y:
            self.search_str = self.search_str[:self.x] + ch \
                              + self.search_str[self.x:]
            self.x += 1

    def delete_key_handler(self):
        if not self.y and self.x:
            self.search_str = self.search_str[:self.x - 1] \
                              + self.search_str[self.x:]
            self.x -= 1

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

        exit()

    def is_insert_key(self, ch):
        if ord(ch) in self.invalid_keys:
            return False

        else:
            return True

    @staticmethod
    def get_col_width():
        return int(subprocess.check_output(['stty', 'size']).split()[1])

    def execute_key_handler(self, ch):
        if ch.encode('string-escape') in self.key_actions:
            self.key_actions[ch.encode('string-escape')]()

        elif self.is_insert_key(ch):
            self.insert_key_handler(ch)

        self.refresh_output()

    def refresh_output(self):
        self.clear_screen()
        sys.stdout.write('>' + self.search_str + '\r')

        for line in self.lines:
            sys.stdout.write(line + ['\n'])

        self.move_cur_up(len(self.lines)+1)
        self.move_cur_right(self.x)
        self.term_hl_on()
        sys.stdout.write(self.search_str[self.x])
        self.term_reset()
        self.move_cur_left()

    def clear_screen(self):
        sys.stdout.write('\r')
        self.clear_line(len(self.lines))
        self.move_cur_up(len(self.lines)+1)


    def get_col_width(self):
        pass

    @staticmethod
    def clear_line(lines=1):
        sys.stdout.write('\033[K\n'*lines)
        DisplayBuffer.move_cur_up(lines)

    @staticmethod
    def term_reset():
        sys.stdout.write('\033[0m')

    @staticmethod
    def term_hl_on():
        sys.stdout.write('\033[7m')

    @staticmethod
    def move_cur_up(lines=1):
        sys.stdout.write('\033[{}A'.format(lines))
        sys.stdout.flush()

    @staticmethod
    def move_cur_down(lines=1):
        sys.stdout.write('\033[{}B'.format(lines))
        sys.stdout.flush()

    @staticmethod
    def move_cur_right(col=1):
        sys.stdout.write('\033[{}C'.format(col))
        sys.stdout.flush()

    @staticmethod
    def move_cur_left(col=1):
        sys.stdout.write('\033[{}D'.format(col))
        sys.stdout.flush()

def dummy(input_str):
    return [input_str]*5


def main():
    getch = _Getch()
    while True:
        ip_char = getch()
        print ip_char.encode('string-escape')
        if ip_char == '\x03':
            break


if __name__ == '__main__':
    main()


    # write_buffer = 'Hi there!\nHow \033[7ma\033[0mre you\n'
    # lines = write_buffer.split('\n')
    # # lines = filter(lambda x: len(x) > 0, lines)
    # clear_lines = map(lambda x: ' ' * len(x), lines)
    # clear_screen = '\n'.join(clear_lines)
    # sys.stdout.write(write_buffer)
    # time.sleep(2)
    # sys.stdout.write('\033[2A')
    # time.sleep(2)
    # sys.stdout.write(clear_screen)
    # sys.stdout.flush()
    # sys.stdout.write('\033[2A')
    # # print ' ' * 50 + '\r',
    # time.sleep(2)
