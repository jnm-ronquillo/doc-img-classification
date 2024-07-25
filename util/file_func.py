import os


def get_subfolder_names(folder_path):
    subfolder_names = []

    # Iterate over the contents of the folder
    for item in os.listdir(folder_path):
        # Check if the item is a directory (subfolder)
        if os.path.isdir(os.path.join(folder_path, item)):
            subfolder_names.append(item)

    return subfolder_names