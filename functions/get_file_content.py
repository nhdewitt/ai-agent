import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working = os.path.abspath(working_directory)
    dir = os.path.join(working_directory, file_path)
    abs_dir = os.path.abspath(dir)
    if not abs_dir.startswith(working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(dir):
        return 'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(dir, 'r') as f:
            file_content = f.read(MAX_CHARS)
        
            if len(file_content) == MAX_CHARS:
                file_content += f'\n[...File "{file_path}" truncated at 10000 characters]'
        
            return file_content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'