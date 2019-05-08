import parser as pars
import sys

files = []
for i in sys.argv:

    if i == 'JackCompiler.py':
        continue

    if i.split('.')[1] == 'jack':
        files.append(i)
    else:
        print("Error, the file inputted is not a .jack file")
        exit(1)
compiled = pars.Parser(files)

print("\nPARSER TEST PASSED\n")

# compiled = pars.Parser("Main_arrayTest.jack")
# compiled = pars.Parser("Main_memory.jack")
# compiled = pars.Parser("Main_string.jack")
