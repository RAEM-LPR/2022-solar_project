# coding: utf-8
# license: GPLv3

#import tkinter
import pygame
import pygame_widgets
from pygame_widgets.button import Button
#from tkinter import filedialog
from solar_vis import *
from solar_model import *
from solar_input import *

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
        physical_time += tstep
        space=[]
        for body in space_objects:
            drawbuf = update_object_position(body)
            pygame.draw.circle(gscreen, drawbuf[3], (drawbuf[0], drawbuf[1]), drawbuf[2])
            #space.append()
        
        #displayed_time.set("%.1f" % physical_time + " seconds gone")
        #for body_image in space:
            #print(body_image[0], body_image[1])
            #pygame.draw.circle(gscreen, body_image[3], (body_image[0], body_image[1]), body_image[2]) #star.image = [x,y,r,star.color]
            
            #space.after(101 - int(time_speed.get()), execution) pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global start_button
    global perform_execution
    perform_execution = True
    #start_button.text = "Pause"
    #start_button.setOnClick(stop_execution)
    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global start_button
    global perform_execution
    perform_execution = False
    #start_button.setText("Start")
    #start_button.setOnClick(start_execution)
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
    space_objects = read_space_objects_data_from_file("one_satellite.txt") # to do
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
    wrire_stats_to_file("modelstat.txt", space_objects)

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
    #global time_speed
    #global space
    #global start_start_button
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

    """
    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_start_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_start_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_start_button.pack(side=tkinter.LEFT)
    save_file_start_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_start_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)
    """
    mainloop()#screen)

    print('Modelling finished!')

if __name__ == "__main__":
    main()
