import os
import shutil
from concurrent.futures import ThreadPoolExecutor

def sort_files_by_extension(source_folder, destination_folder):
    def move_file(file_path):
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1]
        destination_dir = os.path.join(destination_folder, file_extension[1:])

        os.makedirs(destination_dir, exist_ok=True)
        shutil.move(file_path, os.path.join(destination_dir, filename))

    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(move_file, file_path)

source_folder = "Bałagan"
destination_folder = "Sorted_Files"
sort_files_by_extension(source_folder, destination_folder)
