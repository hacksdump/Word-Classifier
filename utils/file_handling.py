class FileUtil:
    def readlines(self):
        with open(self.filepath) as file_read_line:
            for line in file_read_line:
                line = line.replace('\n', '')
                yield line

    def __init__(self, filepath):
        self.filepath = filepath
