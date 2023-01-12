import os


def create_folder(folder_dir):
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
