import os
import re

# get the directory of the current Python file
script_dir = os.path.dirname(os.path.abspath(__file__))

# define the pattern to match
pattern = r'(\d+).png'

# recursively scan the directory and its subdirectories
for root, dirs, files in os.walk(script_dir):
    # initialize the starting number for this folder
    start_num = 1
    for file in files:
        # check if the file matches the pattern
        match = re.match(pattern, file)
        if match:
            # extract the number from the filename
            num = int(match.group(1))
            # generate the new filename
            new_file = f'{start_num}.png'
            # construct the full path for the old and new files
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, new_file)
            # rename the file
            os.rename(old_path, new_path)
            # increment the starting number for the next file in this folder
            start_num += 1
