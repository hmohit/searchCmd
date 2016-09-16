from __future__ import division
from fuzzywuzzy import process


class CommandMetaData:
    def __init__(self, command_str=None, command_tags=set()):
        self.command_str = command_str
        self.command_tags = command_tags

    def is_search_str_in_tags(self, search_str):
        result = False
        for tag in self.command_tags:
            result = result or search_str in tag
            if result is True:
                break

        return result


class SearchMetaData:
    def __init__(self):
        self.command_list = set()

    def load_new_commands(self, filename):
        with open(name=filename) as file_handle:
            for cmd in set(file_handle.readlines()):
                cmd = cmd.rstrip()
                self.command_list.add(CommandMetaData(command_str=cmd, command_tags={cmd}))

    def add_command(self, cmd, tags):
        self.command_list.add(CommandMetaData(command_str=cmd, command_tags=tags))

    def list_all(self):
        for num, cmd in enumerate(self.command_list):
            print str(num) + ' ==>> ' + cmd.command_str + ' => [' + ','.join(cmd.command_tags) + ']'

    def search(self, search_str):
        #result = [cmd.command_str for cmd in self.command_list if cmd.is_search_str_in_tags(search_str)]
        #if len(result) is 0:
        result = self.search_cmd_approx(search_str)

        return result[:5]

    def delete(self, delete_str):
        for cmd in self.command_list:
            if cmd.command_str == delete_str:
                self.command_list.discard(cmd)
                break

    def search_cmd_approx(self, search_str):
        approx_matches = []
        for cmd in self.command_list:
            matches = process.extract(query=search_str, choices=cmd.command_tags, limit=1)
            if matches and matches[0][1] > 50:
                approx_matches.append((cmd.command_str, matches[0][1]))

        approx_matches.sort(key=lambda x: x[1], reverse=True)
        if approx_matches:
            return zip(*approx_matches)[0]
        else:
            return approx_matches
