# coding: utf-8
# license: GPLv3

from solar_objects import Planet, Star


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов
    Параметры:
    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star":  # FIXME: do the same for planet
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):
    """Изображение планеты"""
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4
    Параметры:
    **line** — строка с описание звезды.
    **star** — объект звезды.
    Planet 2 orange 3.302E23 57.909E9 0 0 47.87E3
    """
    
    if line.split()[0] != 'Star':
        TypeError()
    splitted = line.split()
    star.m = float(splitted[3])
    star.x = float(splitted[4])
    star.y = float(splitted[5])
    star.Vx = float(splitted[6])
    star.Vy = float(splitted[7])
    star.r = float(splitted[1])
    star.color = splitted[2]


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4
    Параметры:
    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    if line.split()[0] != 'Planet':
        TypeError()
    splitted = line.split()
    planet.m = float(splitted[3])
    planet.x = float(splitted[4])
    planet.y = float(splitted[5])
    planet.Vx = float(splitted[6])
    planet.Vy = float(splitted[7])
    planet.r = float(splitted[1])
    planet.color = splitted[2]


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Параметры:
    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as output_file:
        for obj in space_objects:
            fstr = f"planet {obj.r} {obj.color} {obj.m} \
                {obj.x} {obj.y} {obj.Vx} {obj.Vy}"
            output_file.write(fstr)
        output_file.close()

stats_array = []

def write_stat_step(space_objects):
    global stats_array
    for obj in space_objects:
            fstr = f"planet {obj.r} {obj.color} {obj.m} \
                {obj.x} {obj.y} {obj.Vx} {obj.Vy}"
            stats_array.append(fstr)

def write_stats_to_file(stats_filename):
    global stats_array
    with open(stats_filename, 'a') as stats_file:
        for fstr in stats_array:
            stats_file.write(fstr)
        stats_file.close()

if __name__ == "__main__":
    print("This module is not for direct call!")