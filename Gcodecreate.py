import re
import math
from gcodeparser import GcodeParser
class GCode:
    sdf
    @staticmethod
    def replace_y_values(code_lines, divisor):
    # Функция replacer заменяет каждое совпадение с шаблоном на новое значение, деленное на divisor
        def replacer(match):
            original_value = float(match.group()[1:])  # Извлекаем исходное значение из совпадения
            new_value = '{:.2f}'.format(original_value / divisor)  # Вычисляем новое значение
            return f'A{new_value}'  # Возвращаем новое значение с добавлением префикса 'A'

        # Используем регулярное выражение для поиска и замены всех значений Y в каждой строке кода
        new_code_lines = []
        for line in code_lines:
            new_line = re.sub(r'Y-?\d+\.\d+', replacer, line)
            new_code_lines.append(new_line)
        
        return new_code_lines

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
        elif clockwise:
            angle_step = -2 * math.pi / num_segments
        else:
            angle_step = 2 * math.pi / num_segments

        # Создаем сегменты прямых линий
        for i in range(num_segments + 1):
            angle = start_angle + angle_step * i
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            lines.append(f"G1 X{float(x):.4f} Y{float(y):.4f}")
        
        return lines

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