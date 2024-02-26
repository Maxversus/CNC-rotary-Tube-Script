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
    if line.command == ('G', 2) or line.command == ('G', 3):
        print(f'Найдена команда {line.params["X"], line.params["Y"], line.params["I"], line.params["J"]} в позиции {(prev_x, prev_y)}')
        arc_lines = (GCode.arc_to_lines((prev_x, prev_y), (line.params["X"], line.params["Y"]), line.params["I"], line.params["J"], clockwise=True, num_segments=20))
        for l in arc_lines:
            new_line = ('G1 X{} Y{}'.format(l[0], l[1]))
            new_gcode.append(new_line)
    else:
        new_gcode.append(line.gcode_str)
    
        
    if 'X' in line.params:
        prev_x = line.params['X']
    if 'Y' in line.params:
        prev_y = line.params['Y']

# сохранить новый gcode в файл
with open('my_new_gcode.gcode', 'w') as f:
    for line in new_gcode:
        f.write(str(line) + '\n')
