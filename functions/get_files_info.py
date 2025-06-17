import os

def get_files_info(working_directory, directory=None):
    if directory == ".":
        directory = None
    if directory:
        dir = os.path.join(working_directory, directory)
        if not os.path.isdir(dir):
            return f'Error: "{directory}" is not a directory'
        abs_working = os.path.abspath(working_directory)
        abs_dir = os.path.abspath(dir)
        if not abs_dir.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        dir = working_directory
    files = []
    try:
        file_list = os.listdir(dir)
    except:
        return f'Error getting file list from "{dir}"'
    for file in file_list:
        path = os.path.join(dir, file)
        try:
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
        except Exception as e:
            return f'Error: {e}"'
        files.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
    return "\n".join(files)