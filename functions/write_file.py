import os

def write_file(working_directory, file_path, content):
    working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_dir.startswith(working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_dir):
        try:
            os.makedirs(os.path.dirname(abs_dir), exist_ok=True)

        except Exception as e:
            return f'Error creating directory "{file_path}": {e}'
    try:
        with open(abs_dir, 'w') as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'