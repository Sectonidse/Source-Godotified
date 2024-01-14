import os
import fnmatch
import fileinput


def remove_comments(directory, file_pattern="*"):
    for root, _, files in os.walk(directory):
        for file_name in fnmatch.filter(files, file_pattern):
            file_path = os.path.join(root, file_name)

            with fileinput.FileInput(file_path, inplace=True) as file:
                for line in file:
                    if not line.startswith("//"):
                        print(line, end='')


# Example usage:
directory_to_search = "./materials/"
remove_comments(directory_to_search, "*.vmt")  # Specify the file pattern as needed
