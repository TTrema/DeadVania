import os

# Get the path of the directory where the script is located
script_path = os.path.dirname(os.path.realpath(__file__))

# Initialize a counter variable for numbering the files
counter = 1

# Recursively loop through all files and directories in the current directory
for root, dirs, files in os.walk(script_path):
    # Loop through each file in the current directory
    for file_name in files:
        # Split the file name into its components
        file_parts = os.path.splitext(file_name)
        # Check if the file is a .png file
        if file_parts[1] == '.png':
            # Construct the new file name using the counter variable
            new_file_name = '{:02d}.png'.format(counter)
            # Construct the full paths to the old and new files
            old_file_path = os.path.join(root, file_name)
            new_file_path = os.path.join(root, new_file_name)
            # Rename the file
            os.rename(old_file_path, new_file_path)
            # Increment the counter
            counter += 1
