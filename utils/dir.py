import os


def create_directory_and_file(target_path):
    # Create the parent directory if it doesn't exist
    parent_dir, _ = os.path.split(target_path)
    os.makedirs(parent_dir, exist_ok=True)

    # Create the target file if it doesn't exist
    if not os.path.exists(target_path):
        with open(target_path, 'w') as file:
            pass

    return target_path
