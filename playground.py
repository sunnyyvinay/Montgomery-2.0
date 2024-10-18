print("executing file")

# in order to execute code live, pass the code in as a string to a variable and use the python exec() function to run it

code = """
print('test 1')
"""

code2 = """
print('test 2')
"""

exec(code + code2)