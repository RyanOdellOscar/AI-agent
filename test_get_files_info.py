# it should run these function calls and print their results:

#get_files_info("calculator", ".")
#get_files_info("calculator", "/bin")
#get_files_info("calculator", "../")
#get_files_info("calculator", "main.py")

import os
import functions.get_files_info
directories_to_test = [".", "pkg", "/bin", "../"]
for directory in directories_to_test:
    print(f"Result for {directory} directory: ")
    result = functions.get_files_info.get_files_info("calculator", directory)
    if result:
        print(result)

#print("Result for current directory: ")
#functions.get_files_info.get_files_info("calculator", ".")
#print("Result for pkg directory: ")
#functions.get_files_info.get_files_info("calculator", "pkg")
#print("Result for /bin directory: ")
#functions.get_files_info.get_files_info("calculator", "/bin")
#print("Result for ../ directory: ")
#functions.get_files_info.get_files_info("calculator", "../")