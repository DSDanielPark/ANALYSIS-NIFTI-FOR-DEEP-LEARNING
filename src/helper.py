import os

def recursive_find_all_files(top_folder_path:str, file_format:str) -> list:
    gathered_file_pathes = []

    for (root, directories, files) in os.walk(top_folder_path):
        for file in files:
            if file_format in file:
                file_path = os.path.join(root, file)
                gathered_file_pathes.append(file_path)

    return gathered_file_pathes