from __future__ import division
from collections import defaultdict
from fuzzywuzzy import process


class SearchMetaData:
    def __init__(self):
        self.command_list = set()
        self.command_dict = defaultdict(list)

    def load_new_commands(self, filename):
        with open(name=filename) as file_handle:
            self.command_list += set(file_handle.readlines())

    def add_command(self, cmd):
        self.command_list.add(cmd)

    def create_dict(self):
        for cmd in self.command_list:
            cmd_length = len(cmd)
            for start in xrange(cmd_length):
                for end in xrange(start, cmd_length):
                    self.command_dict[cmd[start:(end + 1)]].append(cmd)

    def search(self, search_str):
        result = [cmd for cmd in self.command_list if search_str in cmd]
        if len(result) is 0:
            result = self.search_cmd_approx(search_str)

        return result

    def search_dict(self, search_str):
        if search_str in self.command_dict.keys():
            return self.command_dict[search_str]
        else:
            return self.search_cmd_approx(search_str)

    def search_cmd_approx(self, search_str):
        approx_matches = process.extract(query=search_str, choices=self.command_list, limit=5)
        return [k for k,v in approx_matches if v > 50]
