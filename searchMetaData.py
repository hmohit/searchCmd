from __future__ import division
from fuzzywuzzy import process


class SearchMetaData:
    def __init__(self):
        self.command_list = {}

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
        del self.command_list[delete_str]

    def search(self, search_str):
        approx_matches = []
        for cmd in self.command_list:
            matches = process.extract(query=search_str, choices=(self.command_list[cmd] | {cmd}), limit=1)
            if matches and matches[0][1] > 50:
                approx_matches.append((cmd, matches[0][1]))

        approx_matches.sort(key=lambda x: x[1], reverse=True)
        if approx_matches:
            return zip(*approx_matches)[0][:5]
        else:
            return approx_matches[:5]
