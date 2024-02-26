from gcodeparser import GcodeParser

from Gcodecreate import GCode
# открыть файл gcode и сохранить содержимое в переменной
with open('Круг.tap', 'r') as f:
    gcode = f.read()
new_gcode = []
# получить разобранные строки gcode
parsed_gcode = GcodeParser(gcode, include_comments=True).lines
for line in parsed_gcode:
    # заменить команды G2 и G3
    if line.command_str not in ("G2", "G3"):
        new_gcode.append(line.gcode_str)
    else:  
        if line.command == ('G', 2):
            print(f'Найдена команда G3 {line.params["X"], line.params["Y"], line.params["I"], line.params["J"]} в позиции {(prev_x, prev_y)}')
            clockwise = False
        else:
            print(f'Найдена команда G3 {line.params["X"], line.params["Y"], line.params["I"], line.params["J"]} в позиции {(prev_x, prev_y)}')
            clockwise = True

        arc_lines = (GCode.arc_to_lines((prev_x, prev_y), (line.params["X"], line.params["Y"]),
                                            line.params["I"],
                                            line.params["J"], 
                                            clockwise,
                                            num_segments=20
                                            ))
        new_gcode.extend(arc_lines)
    if 'X' in line.params:
        prev_x = line.params['X']
    if 'Y' in line.params:
        prev_y = line.params['Y']

# сохранить новый gcode в файл
with open('my_new_gcode.gcode', 'w') as f:
    for line in new_gcode:
        f.write(str(line) + '\n')
