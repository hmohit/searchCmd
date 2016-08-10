from collections import defaultdict


class SearchMetaData:
    def __init__(self):
        self.command_list = []
        self.command_dict = defaultdict(list)

    def load_new_commands(self, filename):
        with open(name=filename) as file_handle:
            self.command_list = file_handle.readlines()

    def search(self, search_str):
        result = []
        for cmd in self.command_list:
            if search_str in cmd:
                result.append(cmd)

        return result

    def create_dict(self):
        for cmd in self.command_list:
            cmd_length = len(cmd)
            for start in xrange(cmd_length):
                for end in xrange(start, cmd_length):
                    self.command_dict[cmd[start:(end + 1)]].append(cmd)

    def search_dict(self, search_str):
        return self.command_dict[search_str]
