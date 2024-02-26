import re
D = 40 # Pipe diameter
filename = "my_new_gcode.gcode" # Add the name of the file you want to open. "NameFile.CNC"

divisor = (D*3.1415926535)/360

with open(f"{filename}", "r+") as file:
    content = file.read()

def replace_y_values(code, divisor):
    
    def replacer(match):
        original_value = float(match.group()[1:])
        new_value = '{:.2f}'.format(original_value / divisor)
        return f'A{new_value}'

    return re.sub(r'Y-?\d+\.\d+', replacer, code)

content = replace_y_values(content, divisor)

print(content)
with open(f"{filename}", "w") as file:
    file.write(content)
