import os
import shutil
from pathlib import Path


class Recurse:

    def __init__(self, file_type, destination):
        self._file_type = file_type
        self._destination = destination

    def get_file_type(self):
        return self._file_type

    def get_destination(self):
        if self._destination=="":
            self._destination="staged_data"
        return self._destination

    def recurse_path(self, target_path, root=""):
            """"
            This function recursively prints all contents of a pathlib.Path object
            """
            #print_indented(target_path.name, level)
            for file in target_path.iterdir():
                if file.is_dir():
                    self.recurse_path(file, file)
                else:
                    if "azureml" in str(root):
                        continue
                    if str(file.name).endswith(self.get_file_type()):
                        destination = os.path.join(os.getcwd(), self.get_destination(), file.name)
                        source=os.path.join(target_path.absolute(),file.name)
                        shutil.copyfile(source, destination)

    def walk_path(directory):
        for root, dirs, files in os.walk(directory):
            path = root.split(os.sep)
            print(path)

            for dir in dirs:
                print(f"what is the directory {dir}")

            print((len(path) - 1) * '-b-', os.path.basename(root))
            for file in files:
                print(file)
                print(len(path) * '---', file)