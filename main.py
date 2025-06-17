import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from config import system_prompt

MAX_ITERATIONS = 20


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    
    if not args:
        print('Usage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?" [--verbose]')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {prompt}\n") 

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                )
            }
        )
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Gets the content of the specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to retrieve the content from, relative to the working directory. If not provided, informs the user that they cannot read a non-existent file."
                )
            }
        )
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs the Python interpreter on the specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The Python file to run. If not provided, informs the user that they cannot run a non-existent file."
                )
            }
        )
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the desired output to the filename provided by the user, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The text that the user wishes to be output to the file."
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The filename the user would like their output saved to."
                )
            }
        )
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    generate_content(client, messages, verbose, available_functions)

def generate_content(client, messages, verbose, available_functions):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    for i in range(MAX_ITERATIONS):
        needs_tool_call = False
        function_results_to_append = []
        
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    needs_tool_call = True
                    function_call_result = call_function(part.function_call, verbose)
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    function_results_to_append.append(function_call_result)
        
        if not needs_tool_call:
            break

        messages.append(response.candidates[0].content)
        messages.extend(function_results_to_append)

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
    
    if i == MAX_ITERATIONS - 1:
        print("Unfortunately, I reached the maximum number of iterations without resolving the question.")
    else:
        print("Final Response:")
        print(response.text)

if __name__ == "__main__":
    main()