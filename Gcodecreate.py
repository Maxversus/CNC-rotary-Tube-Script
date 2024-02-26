import re
import math
from gcodeparser import GcodeParser
class GCode:
    
    def arc_find(gcode):
        arc = []
        gcode = GcodeParser(gcode)
        
        
        # arc.append(start_point, end_point, center, clockwise=True)
        return arc

    @staticmethod
  
    def arc_to_lines(start_point, end_point, I = 0, J = 0, clockwise=True, num_segments=20):
        """Преобразует дугу в линейные интерполяции"""
        lines = []
        center = (start_point[0] + I, start_point[1] + J)
        radius = math.sqrt((J**2) + (I**2))
        start_angle = math.atan2(start_point[1] - center[1], start_point[0] - center[0])
        end_angle = math.atan2(end_point[1] - center[1] ,end_point[0] - center[0])
        
        # Проверяем направление обхода дуги и корректируем углы
        if clockwise:
            if start_angle > end_angle:
                end_angle += 2 * math.pi
        else:
            if start_angle < end_angle:
                start_angle += 2 * math.pi

        # Определяем угловой шаг между сегментами
        if end_angle - start_angle != 0:
            angle_step = (end_angle - start_angle) / num_segments
        else:
            angle_step = 2 * math.pi / num_segments

        # Создаем сегменты прямых линий
        for i in range(num_segments + 1):
            angle = start_angle + angle_step * i
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            lines.append((float(f"{x:.4f}"), float(f"{y:.4f}")))
        
        return lines
    
    @staticmethod
    def load_from_file( file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

    @staticmethod
    def save_to_file(file_path, commands):
        with open(file_path, 'w') as file:
            file.writelines(commands)

    @staticmethod
    def add_command(commands, command):
        commands.append(command + '\n')

    @staticmethod
    def remove_command(commands, index):
        del commands[index]

    @staticmethod
    def clear_commands(commands):
        commands.clear()

    @staticmethod
    def find_x(x1, y1, x2, y2, y):
        if x1 == x2:
            return f"{x1} Прямая линия"
        else:
            # Находим наклон прямой
            m = (y2 - y1) / (x2 - x1)
            # Находим точку пересечения с осью y (y-перехват)
            b = y1 - m * x1
            # Находим x по известному y
            x = (y - b) / m
            return x