print("executing file")

# in order to execute code live, pass the code in as a string to a variable and use the python exec() function to run it

code = """
def counter(n):
    for i in range(n):
        print(i)
        
counter(5)
"""

exec(code)