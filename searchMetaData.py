class SearchMetaData:
    def __init__(self):
        self.command_list = []

    def load_new_commands(self, filename):
        with open(name=filename) as file_handle:
            self.command_list = file_handle.readlines()
