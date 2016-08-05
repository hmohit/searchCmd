class SearchMetaData:
    def __init__(self):
        self.command_list = []

    def load_new_commands(self, filename):
        with open(name=filename) as file_handle:
            self.command_list = file_handle.readlines()

    def search(self, search_str):
        result = []
        for cmd in self.command_list:
            if search_str in cmd:
                result.append(cmd)

        return result
