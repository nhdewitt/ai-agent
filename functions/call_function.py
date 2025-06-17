import os
from . import run_python_file, get_files_info, get_file_content, write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    working_directory = os.path.abspath("./calculator")
    valid_functions = {
        "get_files_info": get_files_info.get_files_info,
        "get_file_content": get_file_content.get_file_content,
        "run_python_file": run_python_file.run_python_file,
        "write_file": write_file.write_file,
    }
    kwdict = {
        "working_directory": working_directory,
    }

    for k, v in function_call_part.args.items():
        kwdict[k] = v

    if function_call_part.name not in valid_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    function_name = function_call_part.name
    
    function_result = valid_functions[function_name](**kwdict)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )