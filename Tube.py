import re

D = 40 # Pipe diameter
filename = "" # Add the name of the file you want to open. "NameFile.CNC"



divisor = (D*3.1415926535)/360
number = ["Y", "J"]

with open(f"{filename}", "r+") as file:
    content = file.read()

def replace_y_values(number, code, divisor):
    
    def replacer(match):
        original_value = float(match.group()[1:])
        new_value = '{:.2f}'.format(original_value / divisor)
        return f'{number}{new_value}'

    return re.sub(fr'{number}-?\d+\.\d+', replacer, code)

for i in number:
    content = replace_y_values(i, content, divisor)

print(content)
with open(f"{filename}_mode", "w") as file:
    file.write(content)
