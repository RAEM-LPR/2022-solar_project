# coding: utf-8
# license: GPLv3

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from solar_vis import *
from solar_model import *
from solar_input import *

input_data_file = "solar_system.txt"
"""Файл со входными данными"""

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

pgRunning = True

start_button = None
of_button = None
if_button = None
clock = None
tstep = 0
time_mult = 1000.0

space = []

FPS = 30

gscreen  = None

def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    global clock
    global space
    global gscreen
    global space_objects

    if perform_execution:
        recalculate_space_objects_positions(space_objects, time_mult*tstep)
        write_stat_step(space_objects)
        physical_time += tstep
        space=[]
        for body in space_objects:
            update_object_position(space,body)
        for body in space:
            pygame.draw.circle(gscreen, body[3], (body[0], body[1]), body[2])


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global start_button
    global perform_execution
    perform_execution = True
    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global start_button
    global perform_execution
    perform_execution = False
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global space
    global perform_execution
    perform_execution = False
    #for obj in space_objects:
    #    space.delete(obj.image)  # удаление старых изображений планет
    #in_filename = filedialog.askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(input_data_file)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    space = []

    for obj in space_objects:
        if obj.type == 'star':
            create_star_image(space, obj)
        elif obj.type == 'planet':
            create_planet_image(space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    #out_filename = filedialog.asksaveasfilename(filetypes=(("Text file", ".txt"),))
    #write_space_objects_data_to_file(out_filename, space_objects)
    write_stats_to_file("modelstat.txt")

def mainloop():

    global pgRunning
    global tstep 
    global start_button
    global perform_execution
    global gscreen

    while pgRunning:
        tstep = clock.tick(FPS)
        
        gscreen.fill((0, 0, 0))

        execution()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                pgRunning = False
                quit()

        pygame_widgets.update(events)
        start_button.listen(events)

        if perform_execution:
            start_button = Button(
            gscreen, 70,window_height -50,70, 40, text='Pause',
            fontSize=24, margin=20,
            inactiveColour=(255, 255, 255),
            pressedColour=(180, 180, 180), radius=7,
            onClick=stop_execution
            )
        else:
             
            start_button = Button(
            gscreen, 70,window_height -50,70, 40, text='Start',
            fontSize=24, margin=20,
            inactiveColour=(255, 255, 255),
            pressedColour=(180, 180, 180), radius=7,
            onClick=start_execution
            ) 
        
        start_button.draw()

        pygame.display.update()

def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global if_button
    global of_button

    global pgRunning
    global clock

    global start_button

    global gscreen

    print('Modelling started!')
    physical_time = 0

    pygame.init()
    gscreen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()

    start_button = Button(
        gscreen, 70,window_height -50,70, 40, text='Start',
        fontSize=24, margin=20,
        inactiveColour=(255, 255, 255),
        pressedColour=(180, 180, 180), radius=7,
        onClick=start_execution
    )  
    if_button = Button(
        gscreen, 270,window_height -50,110, 40, text="Open file...",
        fontSize=24, margin=20,
        inactiveColour=(255, 255, 255),
        pressedColour=(180, 180, 180), radius=7,
        onClick=open_file_dialog
    )  
    of_button = Button(
        gscreen, 400,window_height -50,140, 40, text="Save to file...",
        fontSize=24, margin=20,
        inactiveColour=(255, 255, 255),
        pressedColour=(180, 180, 180), radius=7,
        onClick=save_file_dialog
    )  
  
    mainloop()

    print('Modelling finished!')

if __name__ == "__main__":
    main()
