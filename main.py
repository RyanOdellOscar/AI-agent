import os
import sys
from dotenv import load_dotenv
import argparse
from google.genai import types
from system_prompt import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from collections.abc import Callable


#Check the .name property of the function_call argument. In theory it could be None, so I recommend copying it to a variable, e.g. function_name, in a way that guarantees you get a string:

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "write_file": write_file,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
}


def call_function(
    function_call: types.FunctionCall, verbose: bool = False,

) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                    types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
                ],
        )
    
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


if api_key == None:
    raise RuntimeError("API key not found")

from google import genai

client = genai.Client(api_key=api_key)


#Wrap the entirety of your model-calling logic in a loop, so the agent can iterate on a task until it's done working and has a final response for the user.

def main():
    print("Hello from aiagent!")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for iteration in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash', contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if args.verbose:
            print(f"Iteration {iteration + 1}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if not response.function_calls == None:
            result_list = []
            for call in response.function_calls:
                function_call_result = call_function(call, verbose=args.verbose)
                if function_call_result.parts == None:
                    raise Exception("function_call_result.parts is None")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("function_call_result.parts[0].function_response is None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("function_call_result.parts[0].function_response.response is None")
                result_list.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                print(f"Calling function: {call.name}({call.args})")

        else:
            print(response.text)
            return

        messages.append(types.Content(role="user", parts=result_list))

        if iteration == 19:
            print("something went wrong")
            system_exit(1)


if __name__ == "__main__":
    main()
