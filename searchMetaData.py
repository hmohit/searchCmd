from collections import defaultdict
import editdistance


class SearchMetaData:
    def __init__(self):
        self.command_list = []
        self.command_dict = defaultdict(list)

    def load_new_commands(self, filename):
        with open(name=filename) as file_handle:
            self.command_list = file_handle.readlines()

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
        cmd_edit_dist = []
        for cmd in self.command_list:
            cmd_edit_dist.append((cmd, editdistance.eval(cmd, search_str) / max(len(cmd), len(search_str))))

        cmd_edit_dist.sort(key=lambda x: x[1])
        try:
            zip(*cmd_edit_dist)[0][:5]
        except (ValueError, IndexError):
            return []
