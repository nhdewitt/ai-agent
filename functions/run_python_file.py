import os
import subprocess
import sys

def run_python_file(working_directory, file_path):
    working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_dir.startswith(working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_dir):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        python_path = sys.executable
        result = subprocess.run([python_path, abs_dir], capture_output=True, timeout=30, cwd=working)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    stdout = result.stdout.decode('utf-8')
    stderr = result.stderr.decode('utf-8')
    if stdout == "" and stderr == "":
        return f"No output produced."
    return_code = result.returncode

    output = []
    output.append(f"STDOUT: {stdout}")
    output.append(f"STDERR: {stderr}")
    if return_code != 0:
        output.append(f"Process exited with code {return_code}")
    return "\n".join(output)