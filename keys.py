import sys, tty, termios, time


class _Getch:
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
    def __int__(self):
        lines = []
        row = 0
        col = 0

    def delete_key_handler(self):
        pass

    def up_key_handler(self):
        pass

    def down_key_handler(self):
        pass

    def left_key_handler(self):
        pass

    def right_key_handler(self):
        pass

    def return_key_handler(self):
        pass

    def exclude_key_handler(self):
        pass

    def execute_key_handler(self, char_input):
        self.refresh_output()
        pass

    def refresh_output(self):
        pass


def main():
    getch = _Getch()
    display_buffer = DisplayBuffer()
    while True:
        # ip_char = getch()
        # # print ip_char.encode('string-escape')
        # if ip_char == '\x03':
        #     break
        #
        # display_buffer.execute_key_handler(ip_char)
        display_buffer()


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
