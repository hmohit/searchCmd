#!/usr/bin/env python

# Put Python imports here
import sys
import subprocess
import readline
import time

# Put 3rd party imports here
from fuzzywuzzy import process


class SearchMetaData:
    def __init__(self):
        self.command_list = {}
        self.cache = []
        self.cache_size = 10
        self.last_lines = 0

    def insert_in_cache(self, element):
        if not element:
            pass

        if element in self.cache:
            self.cache.remove(element)
        elif len(self.cache) == self.cache_size:
            self.cache.pop()

        self.cache.insert(0, element)

    def load_new_commands(self, filename):
        with open(name=filename) as file_handle:
            for cmd in set(file_handle.readlines()):
                cmd = cmd.rstrip().split('::')
                self.command_list[cmd[0]] = set(cmd[1:])

    def add_command(self, cmd, tags):
        self.command_list[cmd] = tags

    def __str__(self):
        data = ''
        for cmd in self.command_list:
            data += ' :: '.join([cmd] + list(self.command_list[cmd])) + '\n'

        return data

    def delete(self, delete_str):
        if delete_str in self.cache:
            self.cache.remove(delete_str)

        del self.command_list[delete_str]

    def search(self, search_str):
        approx_matches = []
        for cmd in self.command_list:
            matches = process.extract(query=search_str, choices=(self.command_list[cmd] | {cmd}), limit=1)
            if matches and matches[0][1] > 50:
                approx_matches.append((cmd, matches[0][1]))

        def doctor_results(x):
            if x[0] in self.cache:
                return x[0], x[1] + len(self.cache) - self.cache.index(x[0])
            else:
                return x[0], x[1]

        approx_matches = map(lambda x: doctor_results(x), approx_matches)
        approx_matches.sort(key=lambda x: x[1], reverse=True)

        if approx_matches:
            return zip(*approx_matches)[0][:5]
        else:
            return approx_matches[:5]

    def search_str(self, input_str, last=0):
        results = self.search(input_str)
        col = int(subprocess.check_output(['stty', 'size']).split()[1])
        lines = 0

        for index, cmd in enumerate(results):
            sys.stdout.write('\033[K')
            out_line = str(index) + ':' + cmd
            print '\r', out_line
            lines += 1 + ((len(out_line) - 1) / col)

        if not last:
            if self.last_lines > lines:
                sys.stdout.write('\033[2K')
                sys.stdout.write('\033[K\n' * (self.last_lines - lines))

            sys.stdout.write('\033[' + str(max(lines, self.last_lines) + 1) + 'A')
            self.last_lines = lines

        sys.stdout.flush()

    def dyn_search(self, done_event):
        last_str = ''

        while True:
            in_str = readline.get_line_buffer()
            time.sleep(0.0001)

            if done_event.is_set():
                print
                self.search_str(last_str, 1)
                exit()

            if last_str != in_str:
                print
                last_str = in_str
                self.search_str(in_str)
                print ' ' * (len(last_str) + 5),
                print '\r>', in_str,
                sys.stdout.flush()
