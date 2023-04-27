import os


def get_filename_without_path_and_extension(filename):
    return os.path.splitext(os.path.split(filename)[-1])[0]


def create_folder(folder_dir):
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
