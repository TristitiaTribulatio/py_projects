from argparse import ArgumentParser
from os import walk, path, remove
from hashlib import md5


class DuplicateFileHandler:
    def __init__(self):
        self.dir, self.sorting_option, self.format = '', '', ''
        self.files, self.files_by_size, self.duplicates = [], {}, {}

    def init_dir(self):
        parser = ArgumentParser()
        parser.add_argument('dir', type=str, default=False)
        try:
            args = parser.parse_args()
            self.dir = args.dir
        except:
            print('Directory is not specified')
        self.get_options()

    def get_options(self):
        self.format = input('Enter file format:\n')
        print('\nSize sorting options:\n1. Descending\n2. Ascending\n')
        while True:
            sorting_option = input('Enter a sorting option:\n')
            if sorting_option in ['1', '2']:
                if sorting_option == '1':
                    self.sorting_option = 'descending'
                elif sorting_option == '2':
                    self.sorting_option = 'ascending'
                break
            else:
                print('\nWrong option\n')
        self.walker()

    def walker(self):
        for root, dirs, files in walk(self.dir):
            for name in files:
                file = path.join(root, name)
                if file.endswith(self.format):
                    self.files.append(file)
        self.size_sorting()

    def size_sorting(self):
        if self.sorting_option == 'ascending':
            self.files.sort(key=path.getsize)
        else:
            self.files.sort(key=path.getsize, reverse=True)
        self.group_by_size()

    def group_by_size(self):
        for file in self.files:
            file_size = path.getsize(file)
            with open(file, 'rb') as f:
                file_hash = md5(b''.join(f.readlines())).hexdigest()
            if file_size in self.files_by_size and file_hash in self.files_by_size[file_size]:
                self.files_by_size[file_size][file_hash].append(file)
            elif file_size in self.files_by_size and file_hash not in self.files_by_size[file_size]:
                self.files_by_size[file_size][file_hash] = [file]
            else:
                self.files_by_size[file_size] = {}
                self.files_by_size[file_size][file_hash] = [file]
        self.collection_duplicates()

    def collection_duplicates(self):
        duplicate_num = 0
        for size in self.files_by_size:
            for file_hash in self.files_by_size[size]:
                if len(self.files_by_size[size][file_hash]) > 1:
                    for file in self.files_by_size[size][file_hash]:
                        duplicate_num += 1
                        self.duplicates[duplicate_num] = (file, size, file_hash)
        self.display_files()

    def display_files(self):
        for size in self.files_by_size.keys():
            print(f'{size} bytes')
            for hash_value in self.files_by_size[size].keys():
                [print(file) for file in self.files_by_size[size][hash_value]]
        self.check_for_duplicate()

    def check_for_duplicate(self):
        while True:
            choice = input('Check for duplicates?')
            if choice in ['yes', 'no']:
                break
            print('Wrong option')
        if choice == 'yes':
            duplicate_num = 0
            for size in self.files_by_size:
                print(f'{size} bytes')
                for file_hash in self.files_by_size[size]:
                    if len(self.files_by_size[size][file_hash]) > 1:
                        print(f'Hash: {file_hash}')
                        for file in self.files_by_size[size][file_hash]:
                            duplicate_num += 1
                            print(f"{duplicate_num}. {file}")
        self.delete_menu()

    def delete_menu(self):
        while True:
            check = input('Delete files?\n')
            if check == 'yes':
                while True:
                    f_nums = input("Enter file numbers to delete:\n").split()
                    if f_nums and all(i.isdigit() for i in f_nums) and all(int(i) in self.duplicates for i in f_nums):
                        self.do_delete([int(i) for i in f_nums])
                    else:
                        print('Wrong format')
            elif check == 'no':
                break
            else:
                print("Wrong option")

    def do_delete(self, files_to_delete):
        freed_space = 0
        for num in files_to_delete:
            print(self.duplicates[num])
            remove(self.duplicates[num][0])
            freed_space += self.duplicates[num][1]
        print(f'Total freed up space: {freed_space} bytes')


if __name__ == '__main__':
    DuplicateFileHandler().init_dir()
