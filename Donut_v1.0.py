import os
import time
from colorama import Fore, Style, init
import numpy as np

# Инициализация Colorama
init()

# Размеры консоли
width, height = 50, 25

# Параметры пончика
donut_radius = 0.8
donut_thickness = 0.2
donut_hole_radius = 0.3
light_position = np.array([2, 2, 2])

# Функция для вычисления оттенка серого
def get_gray_shade(angle):
    gray_level = (np.sin(angle) + 1) / 2  # Нормализация значения в диапазоне [0, 1]
    gray_level = 0.5 + gray_level / 2  # Смещение и масштабирование к диапазону [0.5, 1]
    return Fore.LIGHTBLACK_EX + Style.BRIGHT + '@' + Style.RESET_ALL

# Функция для вычисления цвета пикселя
def get_pixel_color(x, y, z, angle):
    # Нормализация координат пикселя
    x = (x - width / 2) / (width / 2)
    y = (y - height / 2) / (height / 2)
    z = z / 10  # Диапазон z от -1 до 1

    # Вращение пончика
    x_rotated = x * np.cos(angle) - y * np.sin(angle)
    y_rotated = x * np.sin(angle) + y * np.cos(angle)

    # Вычисление направления луча
    ray_direction = np.array([x_rotated, y_rotated, -z])
    ray_direction = ray_direction / np.linalg.norm(ray_direction)

    # Вычисление расстояния до пончика
    distance_from_center = np.sqrt(x_rotated ** 2 + y_rotated ** 2)
    if donut_hole_radius < distance_from_center < donut_radius:
        t = np.sqrt(max(0, donut_radius ** 2 - x_rotated ** 2 - y_rotated ** 2))
        if t > 0:
            # Вычисление нормали
            normal = np.array([x_rotated, y_rotated, t])
            normal = normal / np.linalg.norm(normal)

            # Вычисление освещения
            light_direction = light_position - np.array([x_rotated, y_rotated, t])
            light_direction = light_direction / np.linalg.norm(light_direction)
            diffuse = max(np.dot(normal, light_direction), 0)

            # Вычисление градиента
            gradient = (donut_radius - distance_from_center) / donut_thickness
            gradient = max(0, min(1, gradient))

            # Вычисление цвета
            if gradient > 0.8:
                return Fore.RED + 'g' + Style.RESET_ALL
            elif gradient > 0.6:
                return Fore.YELLOW + 'h' + Style.RESET_ALL
            elif gradient > 0.4:
                return Fore.GREEN + '&' + Style.RESET_ALL
            elif gradient > 0.2:
                return get_gray_shade(angle)
            else:
                return Fore.MAGENTA + '@' + Style.RESET_ALL
    return ' '

# Анимация пончика
angle = 0
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    for z in range(-10, 11, 1):
        for y in range(height):
            row = ''
            for x in range(width):
                row += get_pixel_color(x, y, z, angle)
            print(row)
        time.sleep(0.1)
        os.system('cls' if os.name == 'nt' else 'clear')
    angle += 0.1
