from functions.get_file_content import get_file_content


result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")
result = get_file_content("calculator", "main.py")
print(f"main.py length: {len(result)}")
print(f"main.py truncated: {'truncated' in result}")
print(result[:150])  # Print the first 100 characters to verify content
result = get_file_content("calculator", "pkg/calculator.py")
print(f"calculator.py length: {len(result)}")
print(f"calculator.py truncated: {'truncated' in result}")
print(result[1200:1500])  # Print the first 100 characters to verify content
#lorem = get_file_content("calculator", "lorem.txt")
#is_truncated = "[...File \"lorem.txt\" truncated at 10000 characters]" in lorem
#length = len(lorem)
#print(f"lorem.txt: {length} characters, truncated: {is_truncated}")
#main = get_file_content("calculator", "main.py")
#is_truncated = "[...File \"main.py\" truncated at 10000 characters]" in main
#print(f"main.py: {len(main)} characters, truncated: {is_truncated}")
#calculator = get_file_content("calculator", "pkg/calculator.py")
#is_truncated = "[...File \"calculator.py\" truncated at 10000 characters]" in calculator
#print(f"calculator.py: {len(calculator)} characters, truncated: {is_truncated}")
print(get_file_content("calculator", "/bin/cat")) #this should return an error string
print(get_file_content("calculator", "pkg/does_not_exist.py")) #this should return an error string