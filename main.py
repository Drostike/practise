import random
import sys

import cv2
import pygame

from Button import Button
from Client import Client
from Dogovor import Dogovor
from InputBox import InputBox
from UsloviyaStrahovki import UsloviyaStrahovki

pygame.mixer.init()
pygame.font.init()

PYGBUTTON_FONT = pygame.font.Font('Comfortaa-Medium.ttf', 60)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (64, 64, 64)
GRAY = (128, 128, 128)
LIGHTGRAY = (62, 65, 73)
YELLOW = (209, 190, 0)
GREEN = (114, 192, 83)
RED = (218, 87, 102)
COLOR_INACTIVE = pygame.color.Color(126, 126, 126)
COLOR_ACTIVE = DARKGRAY
FONT_enter = pygame.font.Font("Comfortaa-Medium.ttf", 25)

tablet_sound = pygame.mixer.Sound("tablet.mp3")
tablet_sound.set_volume(1)
paper_sound = pygame.mixer.Sound("paper.mp3")
paper_sound.set_volume(0.05)
click_sound = pygame.mixer.Sound("click.mp3")
click_sound.set_volume(0.1)

_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(0, 0, 0), opx=5):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


pygame.init()

pygame.mixer_music.load("music.mp3")
pygame.mixer_music.set_volume(0.05)
pygame.mixer_music.play()

balance = 150000
screen = pygame.display.set_mode((1600, 1000))
buttons = []

money = Button(rect=(1270, 40, 280, 80), caption=str(balance), fg_color=(209, 190, 0), surface=screen,
               displacement_fg_x=0, displacement_fg_y=9, bg_color=DARKGRAY, only_fg=False, border_color=BLACK,
               hover_color_fg=(219, 200, 10), hover_color_bg=(74, 74, 74), clicked_color_bg=(54, 54, 54),
               clicked_color_fg=(199, 180, 0))

clients_button = Button(rect=(1410, 415, 150, 200), only_fg=True, surface=screen)
buttons.append(money)
buttons.append(clients_button)
clock = pygame.time.Clock()
pygame.display.set_caption("Моя игра")
running = True
video = cv2.VideoCapture("fonovoe.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)
screen = pygame.display.set_mode(video_image.shape[1::-1])
tablet = False
notebook = False

surf = pygame.Surface((450, 400))
surf1 = pygame.Surface((450, 400))
surf2 = pygame.Surface((450, 400))
surf3 = pygame.Surface((450, 400))

rect = pygame.rect.Rect(0, 0, 150, 200)
rect1 = pygame.rect.Rect(0, 0, 200, 174)
rect2 = pygame.rect.Rect(0, 0, 180, 170)
rect3 = pygame.rect.Rect(0, 0, 280, 135)

surf.set_alpha(130)
surf1.set_alpha(130)
surf2.set_alpha(130)
surf3.set_alpha(130)

surf.set_colorkey((255, 255, 255))
surf1.set_colorkey((255, 255, 255))
surf2.set_colorkey((255, 255, 255))
surf3.set_colorkey((255, 255, 255))

notebook_image = pygame.image.load("notebook.png")
house = pygame.image.load("house.png")
health = pygame.image.load("health.png")
car = pygame.image.load("car.png")

house_button = Button(rect=(1010, 823, 200, 174), surface=screen, only_fg=True)
health_button = Button(rect=(708, 825, 180, 170), surface=screen, only_fg=True)
car_button = Button(rect=(300, 850, 280, 135), surface=screen, only_fg=True)

buttons.append(health_button)
buttons.append(house_button)
buttons.append(car_button)

house_demand = 50
health_demand = 50
car_demand = 50

small_house = pygame.transform.scale(house, (house.get_width() // 2, house.get_height() // 2))
small_health = pygame.transform.scale(health, (health.get_width() // 2, health.get_height() // 2))
small_car = pygame.transform.scale(car, (car.get_width() // 2, car.get_height() // 2))

text = pygame.font.Font("Comfortaa-Medium.ttf", 40)
text2 = pygame.font.Font("Comfortaa-Medium.ttf", 50)

date_block = Button(screen, (50, 40, 840, 80), DARKGRAY, border_rounding=12, border_color=BLACK)
date_fon = Button(screen, (170, 40, 600, 80), border_rounding=0, border_color=BLACK, bg_color=(33, 33, 33))
pause_button = Button(screen, (50, 40, 120, 80), border_rounding=12, only_fg=True)
speed_button = Button(screen, (770, 40, 120, 80), border_rounding=12, only_fg=True)

buttons.append(pause_button)
buttons.append(speed_button)

pause = False
speed = 1

color_inactive = (33, 33, 33)
color_active = (68, 137, 211)

tablet_image = pygame.image.load("tablet.png")
tablet_image = pygame.transform.scale(tablet_image, (tablet_image.get_width() // 1.6, tablet_image.get_height() // 1.8))

count = 0
day = 1
mounth = 1
year = 2023

close_tablet = False
open_tablet = False

tablet_image_lines = pygame.image.load("tablet_lines.png")
tablet_image_lines = pygame.transform.scale(tablet_image_lines, (
    tablet_image_lines.get_width() // 1.6, tablet_image_lines.get_height() // 1.8))

close_notebook = False
open_notebook = False

notebook_close_image = pygame.image.load("note_close.png")
notebook_open_image = pygame.image.load("note_open.png")

notebook_close_image = pygame.transform.scale(notebook_close_image, (
    notebook_close_image.get_width() // 1.23, notebook_close_image.get_height() // 1.23))
notebook_open_image = pygame.transform.scale(notebook_open_image, (
    notebook_open_image.get_width() // 1.23, notebook_open_image.get_height() // 1.23))

default_usloviya_house = UsloviyaStrahovki(3000, 9999, 50000, 5000, 0)
default_usloviya_health = UsloviyaStrahovki(3000, 9999, 50000, 5000, 0)
default_usloviya_car = UsloviyaStrahovki(3000, 9999, 50000, 5000, 0)

mounth_count = 0
clients_list_car = []
clients_list_health = []
clients_list_house = []

names = ("Александр", "Михаил", "Марк", "Лев", "Максим", "Артём", "Дмитрий", "Иван", "Матвей", "Даниил")
fams = ("Иванов", "Кузнецов", "Попов", "Соколов", "Новиков", "Смирнов", "Петров", "Ковалёв", "Васильев", "Пономарёв")
balance_hist = {"Ежемесячные расходы": 0, "Доход со страховки здоровья": 0, "Доход со страховки автомобилей": 0,
                "Доход со страховки недвижимости": 0, "Выплаты по страховке недвижимости": 0,
                "Выплаты по страховке здоровья": 0, "Выплаты по страховке автомобилей": 0}

text_tablet = pygame.font.Font("Comfortaa-Medium.ttf", 33)
text_tablet_small = pygame.font.Font("Comfortaa-Medium.ttf", 25)

input_boxes = []
input1 = InputBox(710, 336, 200, 33)
input_boxes.append(input1)
input2 = InputBox(1088, 427, 200, 33)
input_boxes.append(input2)
input3 = InputBox(595, 517, 200, 33)
input_boxes.append(input3)
input4 = InputBox(810, 609, 200, 33)
input_boxes.append(input4)

enter = Button(screen, (690, 676, 350, 80), DARKGRAY, WHITE, caption="Сохранить", font=text2, visible=False,
               displacement_fg_y=10, displacement_fg_x=17, hover_color_fg=WHITE, hover_color_bg=(74, 74, 74))
buttons.append(enter)

text_notebook = pygame.font.Font("Comfortaa-Medium.ttf", 18)

game_over = False

text_big = pygame.font.Font("Comfortaa-Medium.ttf", 70)

while running:

    if balance < 0:
        game_over = True

    if "usloviya_house" not in locals():
        usloviya_house = default_usloviya_house

    if "usloviya_health" not in locals():
        usloviya_health = default_usloviya_health

    if "usloviya_car" not in locals():
        usloviya_car = default_usloviya_car

    if not pause:
        count += 1

    if not game_over:
        car_demand = round((
                                       usloviya_car.return_max() - usloviya_car.return_franshiza()) / usloviya_car.return_vznos() * 3) - mounth_count
        health_demand = round((
                                          usloviya_health.return_max() - usloviya_health.return_franshiza()) / usloviya_health.return_vznos() * 3) - mounth_count
        house_demand = round((
                                         usloviya_house.return_max() - usloviya_house.return_franshiza()) / usloviya_house.return_vznos() * 3) - mounth_count

    if not game_over:
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(),
                video_image.shape[1::-1],
                "BGR")
        else:
            run = False
        screen.blit(video_surf, (0, 0))
    else:
        pygame.mixer_music.stop()
        pause = True
        game_over = Button(screen, (400, 250, 800, 500), bg_color=LIGHTGRAY, hover_effect=False, click_effect=False,
                           active=False, border_rounding=20, border_width=5, border_color=BLACK)
        game_over.draw()
        label1 = render("Вы проиграли,", text_big, gfcolor=YELLOW, opx=3)
        screen.blit(label1, (520, 320))
        label2 = render(f"Но выдержали целых {mounth_count} месяцев!", text, gfcolor=YELLOW, opx=2)
        screen.blit(label2, (453, 480))
        label3 = render("Нажмите ESC для выхода", text_tablet_small, gfcolor=YELLOW, opx=2)
        screen.blit(label3, (620, 700))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    """if not game_over:
        balance -= 10000"""

    if house_demand > 100:
        house_demand = 100
    elif house_demand < 0:
        house_demand = 0

    if health_demand > 100:
        health_demand = 100
    elif health_demand < 0:
        health_demand = 0

    if car_demand > 100:
        car_demand = 100
    elif car_demand < 0:
        car_demand = 0

    if car_demand < 40:
        color = RED
    elif car_demand < 70:
        color = YELLOW
    else:
        color = GREEN
    text_car = render("-  " + str(car_demand) + "%", text, color, BLACK, 1)
    screen.blit(text_car, (175, 258))

    if health_demand < 40:
        color = RED
    elif health_demand < 70:
        color = YELLOW
    else:
        color = GREEN
    text_health = render("-    " + str(health_demand) + "%", text, color, BLACK, 1)
    screen.blit(text_health, (155, 410))

    if house_demand < 40:
        color = RED
    elif house_demand < 70:
        color = YELLOW
    else:
        color = GREEN
    text_house = render("-    " + str(house_demand) + "%", text, color, BLACK, 1)
    screen.blit(text_house, (155, 580))

    money.set_caption(str(balance) + "₽")
    money.set_displacement_fg_x((7 - len(str(balance))) * money.get_font().size("0")[0] * 0.55)
    money.draw()

    surf.fill((255, 255, 255))
    surf1.fill((255, 255, 255))
    surf2.fill((255, 255, 255))
    surf3.fill((255, 255, 255))

    pygame.draw.rect(rect=rect, border_radius=15, color=DARKGRAY, surface=surf)
    pygame.draw.rect(rect=rect1, border_radius=15, color=DARKGRAY, surface=surf1)
    pygame.draw.rect(rect=rect2, border_radius=15, color=DARKGRAY, surface=surf2)
    pygame.draw.rect(rect=rect3, border_radius=15, color=DARKGRAY, surface=surf3)

    house_button.draw()
    clients_button.draw()
    health_button.draw()
    car_button.draw()

    surf.set_alpha(0)
    surf1.set_alpha(0)
    surf2.set_alpha(0)
    surf3.set_alpha(0)

    pause_button.draw()
    speed_button.draw()
    date_block.draw()
    date_fon.draw()

    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            for box in input_boxes:
                box.handle_event(event)

            for button in buttons:
                button.events(event)
                if button == money:
                    if button.get_click():
                        paper_sound.play()
                        if notebook:
                            close_notebook = True
                            close_notebook_count = 24
                            notebook = False
                        else:
                            if tablet:
                                close_tablet = True
                                close_tablet_count = 24
                                tablet = False
                                input1.set_text("")
                                input2.set_text("")
                                input3.set_text("")
                                input4.set_text("")
                                enter.set_visible(False)
                            notebook_type = "money"
                            open_notebook = True
                            open_notebook_count = 0

                elif button == clients_button:
                    if button.get_click():
                        paper_sound.play()
                        if notebook:
                            close_notebook = True
                            close_notebook_count = 24
                            notebook = False
                        else:
                            if tablet:
                                close_tablet = True
                                close_tablet_count = 24
                                tablet = False
                                input1.set_text("")
                                input2.set_text("")
                                input3.set_text("")
                                input4.set_text("")
                                enter.set_visible(False)
                            notebook_type = "clients"
                            open_notebook = True
                            open_notebook_count = 0

                elif button == house_button:
                    if button.get_click():
                        tablet_sound.play()
                        if tablet:
                            close_tablet = True
                            close_tablet_count = 24
                            tablet = False
                            input1.set_text("")
                            input2.set_text("")
                            input3.set_text("")
                            input4.set_text("")
                            enter.set_visible(False)
                        else:
                            if notebook:
                                close_notebook = True
                                close_notebook_count = 24
                                notebook = False
                            tablet_type = "house"
                            open_tablet = True
                            open_tablet_count = 0

                elif button == health_button:
                    if button.get_click():
                        tablet_sound.play()
                        if tablet:
                            close_tablet = True
                            close_tablet_count = 24
                            tablet = False
                            input1.set_text("")
                            input2.set_text("")
                            input3.set_text("")
                            input4.set_text("")
                            enter.set_visible(False)
                        else:
                            if notebook:
                                close_notebook = True
                                close_notebook_count = 24
                                notebook = False
                            tablet_type = "health"
                            open_tablet = True
                            open_tablet_count = 0

                elif button == car_button:
                    if button.get_click():
                        tablet_sound.play()
                        if tablet:
                            close_tablet = True
                            close_tablet_count = 24
                            tablet = False
                            input1.set_text("")
                            input2.set_text("")
                            input3.set_text("")
                            input4.set_text("")
                            enter.set_visible(False)
                        else:
                            if notebook:
                                close_notebook = True
                                close_notebook_count = 24
                                notebook = False
                            tablet_type = "car"
                            open_tablet = True
                            open_tablet_count = 0

                elif button == pause_button:
                    if button.get_click():
                        click_sound.play()
                        if pause:
                            pause = False
                        else:
                            pause = True

                elif button == speed_button:
                    if button.get_click():
                        click_sound.play()
                        if speed == 1:
                            speed = 2
                        elif speed == 2:
                            speed = 3
                        else:
                            speed = 1

                if button == enter:
                    if button.get_click():
                        click_sound.play()

    for box in input_boxes:
        box.update()

    if pause:
        pygame.draw.polygon(screen, color_active, ((87, 53), (127, 80), (87, 107)))

    if not pause:
        pygame.draw.rect(screen, color_active, (85, 55, 15, 50))
        pygame.draw.rect(screen, color_active, (110, 55, 15, 50))

    if clients_button.button_down():
        surf.set_alpha(180)
    elif clients_button.get_state_hover():
        surf.set_alpha(130)

    if house_button.button_down():
        surf1.set_alpha(180)
    elif house_button.get_state_hover():
        surf1.set_alpha(130)

    if health_button.button_down():
        surf2.set_alpha(180)
    elif health_button.get_state_hover():
        surf2.set_alpha(130)

    if car_button.button_down():
        surf3.set_alpha(180)
    elif car_button.get_state_hover():
        surf3.set_alpha(130)

    if speed == 1:
        pygame.draw.polygon(screen, color_active, ((790, 60), (815, 80), (790, 100)))
        pygame.draw.polygon(screen, color_inactive, ((820, 60), (845, 80), (820, 100)))
        pygame.draw.polygon(screen, color_inactive, ((850, 60), (875, 80), (850, 100)))
    elif speed == 2:
        pygame.draw.polygon(screen, color_active, ((790, 60), (815, 80), (790, 100)))
        pygame.draw.polygon(screen, color_active, ((820, 60), (845, 80), (820, 100)))
        pygame.draw.polygon(screen, color_inactive, ((850, 60), (875, 80), (850, 100)))
    elif speed == 3:
        pygame.draw.polygon(screen, color_active, ((790, 60), (815, 80), (790, 100)))
        pygame.draw.polygon(screen, color_active, ((820, 60), (845, 80), (820, 100)))
        pygame.draw.polygon(screen, color_active, ((850, 60), (875, 80), (850, 100)))

    if count % 90 == 0:
        day += 1
        if random.randint(1, 200 - car_demand) < 8:
            client = Client(random.choice(names), random.choice(fams), random.randint(18, 90),
                            random.randint(10000000, 100000000))
            dogovor = Dogovor(client, random.randint(10000000, 100000000), usloviya_car, "car", mounth_count,
                              random.randint(3, 18))
            clients_list_car.append(dogovor)
            balance_hist["Доход со страховки автомобилей"] += dogovor.usloviya.return_vznos()
            balance += dogovor.usloviya.return_vznos()

        if random.randint(1, 200 - car_demand) < 8:
            client = Client(random.choice(names), random.choice(fams), random.randint(18, 90),
                            random.randint(10000000, 100000000))
            dogovor = Dogovor(client, random.randint(10000000, 100000000), usloviya_health, "health", mounth_count,
                              random.randint(3, 18))
            clients_list_health.append(dogovor)
            balance_hist["Доход со страховки здоровья"] += dogovor.usloviya.return_vznos()
            balance += dogovor.usloviya.return_vznos()

        if random.randint(1, 200 - car_demand) < 8:
            client = Client(random.choice(names), random.choice(fams), random.randint(18, 90),
                            random.randint(10000000, 100000000))
            dogovor = Dogovor(client, random.randint(10000000, 100000000), usloviya_house, "house", mounth_count,
                              random.randint(3, 18))
            clients_list_house.append(dogovor)
            balance_hist["Доход со страховки недвижимости"] += dogovor.usloviya.return_vznos()
            balance += dogovor.usloviya.return_vznos()

        for dogovor in clients_list_car:
            if random.randint(1, 372) == 1:
                viplata = random.randint(1, dogovor.usloviya.return_max() * 1.4)
                if viplata > dogovor.usloviya.return_max():
                    viplata = dogovor.usloviya.return_max()
                elif viplata < dogovor.usloviya.return_franshiza():
                    viplata = 0
                balance_hist["Выплаты по страховке автомобилей"] += viplata
                balance -= viplata

        for dogovor in clients_list_health:
            if random.randint(1, 372) == 1:
                viplata = random.randint(1, dogovor.usloviya.return_max() * 1.4)
                if viplata > dogovor.usloviya.return_max():
                    viplata = dogovor.usloviya.return_max()
                elif viplata < dogovor.usloviya.return_franshiza():
                    viplata = 0
                balance_hist["Выплаты по страховке здоровья"] += viplata
                balance -= viplata

        for dogovor in clients_list_house:
            if random.randint(1, 372) == 1:
                viplata = random.randint(1, dogovor.usloviya.return_max() * 1.4)
                if viplata > dogovor.usloviya.return_max():
                    viplata = dogovor.usloviya.return_max()
                elif viplata < dogovor.usloviya.return_franshiza():
                    viplata = 0
                balance_hist["Выплаты по страховке недвижимости"] += viplata
                balance -= viplata

    pygame.draw.rect(screen, GREEN, (170, 40, round(600 / 90 * (count % 90)), 80))

    if day == 32:
        day = 1
        mounth += 1
        mounth_count += 1
        balance -= 40000
        balance_hist = {"Ежемесячные расходы": 40000, "Доход со страховки здоровья": 0,
                        "Доход со страховки автомобилей": 0, "Доход со страховки недвижимости": 0,
                        "Выплаты по страховке недвижимости": 0, "Выплаты по страховке здоровья": 0,
                        "Выплаты по страховке автомобилей": 0}
        for dogovor in clients_list_health:
            if mounth_count - dogovor.return_date() > dogovor.return_time():
                clients_list_health.remove(dogovor)
            else:
                balance_hist["Доход со страховки здоровья"] += dogovor.usloviya.return_vznos()
                balance += dogovor.usloviya.return_vznos()

        for dogovor in clients_list_car:
            if mounth_count - dogovor.return_date() > dogovor.return_time():
                clients_list_car.remove(dogovor)
            else:
                balance_hist["Доход со страховки автомобилей"] += dogovor.usloviya.return_vznos()
                balance += dogovor.usloviya.return_vznos()

        for dogovor in clients_list_house:
            if mounth_count - dogovor.return_date() > dogovor.return_time():
                clients_list_house.remove(dogovor)
            else:
                balance_hist["Доход со страховки недвижимости"] += dogovor.usloviya.return_vznos()
                balance += dogovor.usloviya.return_vznos()

        if mounth_count - usloviya_house.return_date() > usloviya_house.return_period():
            usloviya_house = default_usloviya_house

        if mounth_count - usloviya_health.return_date() > usloviya_health.return_period():
            usloviya_health = default_usloviya_health

        if mounth_count - usloviya_car.return_date() > usloviya_car.return_period():
            usloviya_car = default_usloviya_car

    if mounth == 13:
        mounth = 1
        year += 1

    date = render(f"{str(day)}/{str(mounth)}/{str(year)}", text2, opx=2, ocolor=BLACK, gfcolor=YELLOW)

    screen.blit(surf, (1410, 415))
    screen.blit(surf1, (1010, 823))
    screen.blit(surf2, (708, 825))
    screen.blit(surf3, (300, 850))
    screen.blit(notebook_image, (1400, 430))
    screen.blit(house, (1000, 800))
    screen.blit(health, (729, 840))
    screen.blit(car, (300, 853))
    screen.blit(small_house, (15, 550))
    screen.blit(small_health, (40, 400))
    screen.blit(small_car, (15, 250))
    screen.blit(date, (350, 50))

    if not game_over:
        if open_tablet:
            if open_tablet_count < 24:
                if open_tablet_count < 12:
                    screen.blit(tablet_image, (open_tablet_count * 100 - 1000, 150))
                elif open_tablet_count < 18:
                    screen.blit(tablet_image, (200 + (open_tablet_count - 12) * 20, 150))
                else:
                    screen.blit(tablet_image, (255 + (open_tablet_count * 5 - 18), 150))
                open_tablet_count += 1
            else:
                open_tablet = False
                tablet = True

        if close_tablet:
            if close_tablet_count > 0:
                if close_tablet_count < 12:
                    screen.blit(tablet_image, (close_tablet_count * 100 - 1000, 150))
                elif close_tablet_count < 18:
                    screen.blit(tablet_image, (200 + (close_tablet_count - 12) * 20, 150))
                else:
                    screen.blit(tablet_image, (255 + (close_tablet_count * 5 - 18), 150))
                close_tablet_count -= 1
            else:
                close_tablet = False

        if tablet:
            screen.blit(tablet_image_lines, (350, 150))

        if open_notebook:
            if open_notebook_count < 24:
                if open_notebook_count < 10:
                    screen.blit(notebook_close_image, (600, 1000 - (open_notebook_count * 70)))
                elif open_notebook_count < 17:
                    screen.blit(notebook_close_image, (600, 300 - (open_notebook_count - 7) * 15))
                else:
                    screen.blit(notebook_close_image, (600, 170 - (open_notebook_count - 15) * 3))
                open_notebook_count += 1
            else:
                open_notebook = False
                notebook = True

        if close_notebook:
            if close_notebook_count > 0:
                if close_notebook_count < 10:
                    screen.blit(notebook_close_image, (600, 1100 - (close_notebook_count * 70)))
                elif close_notebook_count < 17:
                    screen.blit(notebook_close_image, (600, 300 - (close_notebook_count - 7) * 15))
                else:
                    screen.blit(notebook_close_image, (600, 170 - (close_notebook_count - 15) * 3))
                close_notebook_count -= 1
            else:
                close_notebook = False

        if notebook:
            screen.blit(notebook_open_image, (400, 140))

    if tablet and not game_over:
        if tablet_type == "car":
            label = render("Новые условия страхования автомобилей", text_tablet, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label1 = render("Ежемесячный взнос - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label2 = render("Максимальная сумма страхового возмещения - ", text_tablet_small, gfcolor=WHITE,
                            ocolor=BLACK, opx=2)
            label3 = render("Франшиза - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label4 = render("Срок действия (в месяцах) - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)

            screen.blit(label, (450, 212))
            screen.blit(label1, (415, 339))
            screen.blit(label2, (415, 430))
            screen.blit(label3, (415, 520))
            screen.blit(label4, (415, 611))
            enter.set_visible(True)

            for box in input_boxes:
                box.draw(screen)

            if enter.get_click():
                close_tablet = True
                close_tablet_count = 24
                tablet = False
                enter.set_visible(False)
                usloviya_car = UsloviyaStrahovki(int(input1.get_text()), int(input4.get_text()), int(input2.get_text()),
                                                 int(input3.get_text()), date=mounth_count)
                input1.set_text("")
                input2.set_text("")
                input3.set_text("")
                input4.set_text("")

        elif tablet_type == "health":
            label = render("Новые условия страхования здоровья", text_tablet, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label1 = render("Ежемесячный взнос - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label2 = render("Максимальная сумма страхового возмещения - ", text_tablet_small, gfcolor=WHITE,
                            ocolor=BLACK, opx=2)
            label3 = render("Франшиза - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label4 = render("Срок действия (в месяцах) - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)

            screen.blit(label, (490, 212))
            screen.blit(label1, (415, 339))
            screen.blit(label2, (415, 430))
            screen.blit(label3, (415, 520))
            screen.blit(label4, (415, 611))
            enter.set_visible(True)

            for box in input_boxes:
                box.draw(screen)

            if enter.get_click():
                close_tablet = True
                close_tablet_count = 24
                tablet = False
                usloviya_health = UsloviyaStrahovki(int(input1.get_text()), int(input4.get_text()),
                                                    int(input2.get_text()),
                                                    int(input3.get_text()), date=mounth_count)
                input1.set_text("")
                input2.set_text("")
                input3.set_text("")
                input4.set_text("")
                enter.set_visible(False)

        elif tablet_type == "house":
            label = render("Новые условия страхования недвижимости", text_tablet, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label1 = render("Ежемесячный взнос - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label2 = render("Максимальная сумма страхового возмещения - ", text_tablet_small, gfcolor=WHITE,
                            ocolor=BLACK, opx=2)
            label3 = render("Франшиза - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)
            label4 = render("Срок действия (в месяцах) - ", text_tablet_small, gfcolor=WHITE, ocolor=BLACK, opx=2)

            screen.blit(label, (450, 212))
            screen.blit(label1, (415, 339))
            screen.blit(label2, (415, 430))
            screen.blit(label3, (415, 520))
            screen.blit(label4, (415, 611))
            enter.set_visible(True)

            for box in input_boxes:
                box.draw(screen)

            if enter.get_click():
                close_tablet = True
                close_tablet_count = 24
                tablet = False
                usloviya_house = UsloviyaStrahovki(int(input1.get_text()), int(input4.get_text()),
                                                   int(input2.get_text()),
                                                   int(input3.get_text()), date=mounth_count)
                input1.set_text("")
                input2.set_text("")
                input3.set_text("")
                input4.set_text("")
                enter.set_visible(False)

    if notebook and not game_over:
        if notebook_type == "money":
            label = render("Расходы и доходы           за текущий месяц", text_tablet, gfcolor=YELLOW, ocolor=BLACK,
                           opx=2)
            label2 = render("Выплаты по страховке недвижимости", text_notebook, gfcolor=RED, ocolor=BLACK, opx=2)
            label3 = render("Выплаты по страховке здоровья", text_notebook, gfcolor=RED, ocolor=BLACK, opx=2)
            label4 = render("Выплаты по страховке автомобилей", text_notebook, gfcolor=RED, ocolor=BLACK, opx=2)
            label5 = render("Доход по страховке недвижимости", text_notebook, gfcolor=GREEN, ocolor=BLACK, opx=2)
            label6 = render("Доход по страховке здоровья", text_notebook, gfcolor=GREEN, ocolor=BLACK, opx=2)
            label7 = render("Доход по страховке автомобилей", text_notebook, gfcolor=GREEN, ocolor=BLACK, opx=2)
            label8 = render("Ежемесячные расходы", text_notebook, gfcolor=RED, ocolor=BLACK, opx=2)
            label9 = render("Итого", text_tablet, gfcolor=YELLOW, ocolor=BLACK, opx=2)

            screen.blit(label, (458, 168))
            screen.blit(label5, (428, 233))
            screen.blit(label6, (428, 305))
            screen.blit(label7, (428, 380))
            screen.blit(label2, (428, 455))
            screen.blit(label3, (428, 529))
            screen.blit(label4, (428, 602))
            screen.blit(label8, (428, 676))
            screen.blit(label9, (428, 735))

            label20 = render(str(balance_hist["Выплаты по страховке недвижимости"]) + "₽", text_tablet_small,
                             gfcolor=RED, ocolor=BLACK, opx=2)
            label30 = render(str(balance_hist["Выплаты по страховке здоровья"]) + "₽", text_tablet_small, gfcolor=RED,
                             ocolor=BLACK, opx=2)
            label40 = render(str(balance_hist["Выплаты по страховке автомобилей"]) + "₽", text_tablet_small,
                             gfcolor=RED,
                             ocolor=BLACK, opx=2)
            label50 = render(str(balance_hist["Доход со страховки недвижимости"]) + "₽", text_tablet_small,
                             gfcolor=GREEN,
                             ocolor=BLACK, opx=2)
            label60 = render(str(balance_hist["Доход со страховки здоровья"]) + "₽", text_tablet_small, gfcolor=GREEN,
                             ocolor=BLACK, opx=2)
            label70 = render(str(balance_hist["Доход со страховки автомобилей"]) + "₽", text_tablet_small,
                             gfcolor=GREEN,
                             ocolor=BLACK, opx=2)
            label80 = render("40000₽", text_tablet_small, gfcolor=RED,
                             ocolor=BLACK, opx=2)
            color = RED if -balance_hist["Выплаты по страховке недвижимости"] - balance_hist[
                "Выплаты по страховке здоровья"] - balance_hist["Выплаты по страховке автомобилей"] + balance_hist[
                               "Доход со страховки недвижимости"] + balance_hist["Доход со страховки здоровья"] + \
                           balance_hist["Доход со страховки автомобилей"] - 40000 < 0 else GREEN
            label90 = render(str(
                -balance_hist["Выплаты по страховке недвижимости"] - balance_hist["Выплаты по страховке здоровья"] +
                -balance_hist["Выплаты по страховке автомобилей"] + balance_hist["Доход со страховки недвижимости"] +
                balance_hist["Доход со страховки здоровья"] + balance_hist[
                    "Доход со страховки автомобилей"] - 40000) + "₽", text_tablet, gfcolor=color,
                             ocolor=BLACK, opx=2)

            screen.blit(label50, (1030 - len(str(balance_hist["Доход со страховки недвижимости"]) + "₽") / 2 * 10, 227))
            screen.blit(label60, (1030 - len(str(balance_hist["Доход со страховки здоровья"]) + "₽") / 2 * 10, 300))
            screen.blit(label70, (1030 - len(str(balance_hist["Доход со страховки автомобилей"]) + "₽") / 2 * 10, 375))
            screen.blit(label20,
                        (1030 - len(str(balance_hist["Выплаты по страховке недвижимости"]) + "₽") / 2 * 10, 450))
            screen.blit(label30, (1030 - len(str(balance_hist["Выплаты по страховке здоровья"]) + "₽") / 2 * 10, 524))
            screen.blit(label40,
                        (1030 - len(str(balance_hist["Выплаты по страховке автомобилей"]) + "₽") / 2 * 10, 598))
            screen.blit(label80, (1030 - len(str("40000₽")) / 2 * 10, 671))
            screen.blit(label90, (1030 - len(str(
                -balance_hist["Выплаты по страховке недвижимости"] - balance_hist["Выплаты по страховке здоровья"] +
                -balance_hist["Выплаты по страховке автомобилей"] + balance_hist["Доход со страховки недвижимости"] +
                balance_hist["Доход со страховки здоровья"] + balance_hist[
                    "Доход со страховки автомобилей"] - 40000) + "₽") / 2 * 15, 735))

        elif notebook_type == "clients":
            label = render("Список                             клиентов", text_tablet, gfcolor=YELLOW, ocolor=BLACK,
                           opx=2)

            screen.blit(label, (540, 170))

            clients = clients_list_car + clients_list_house + clients_list_health
            if len(clients) > 0:
                label1 = render(
                    f"Имя: {clients[0].return_client().return_name()}   Фамилия: {clients[0].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[0].return_thing() == 'car':
                    type = "авто"
                elif clients[0].return_thing() == "health":
                    type = "здоровье"
                else:
                    type = "недвижимость"

                mes = clients[0].return_date() + clients[0].return_time()
                years = 2023
                while mes > 12:
                    years += 1
                    mes -= 12

                label2 = render(f"Тип: {type}   Срок: до 1/{mes}/{years}", text_notebook, gfcolor=YELLOW, ocolor=BLACK,
                                opx=2)
                label3 = render(
                    f"Взнос: {clients[0].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[0].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label1, (430, 233 + 25))
                screen.blit(label2, (430, 259 + 25))
                screen.blit(label3, (430, 285 + 25))

            if len(clients) > 1:
                label11 = render(
                    f"Имя: {clients[1].return_client().return_name()}   Фамилия: {clients[1].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[1].return_thing() == 'car':
                    type1 = "авто"
                elif clients[1].return_thing() == "health":
                    type1 = "здоровье"
                else:
                    type1 = "недвижимость"

                mes1 = clients[1].return_date() + clients[1].return_time()
                years1 = 2023
                while mes1 > 12:
                    years1 += 1
                    mes1 -= 12

                label12 = render(f"Тип: {type1}   Срок: до 1/{mes1}/{years1}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label13 = render(
                    f"Взнос: {clients[1].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[1].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label11, (853, 233 + 25))
                screen.blit(label12, (853, 259 + 25))
                screen.blit(label13, (853, 285 + 25))

            if len(clients) > 2:
                label21 = render(
                    f"Имя: {clients[2].return_client().return_name()}   Фамилия: {clients[2].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[2].return_thing() == 'car':
                    type2 = "авто"
                elif clients[2].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[2].return_date() + clients[2].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[2].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[2].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (430, 330 + 25))
                screen.blit(label22, (430, 356 + 25))
                screen.blit(label23, (430, 382 + 25))

            if len(clients) > 3:
                label21 = render(
                    f"Имя: {clients[3].return_client().return_name()}   Фамилия: {clients[3].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[3].return_thing() == 'car':
                    type2 = "авто"
                elif clients[3].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[3].return_date() + clients[3].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[3].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[3].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (853, 330 + 25))
                screen.blit(label22, (853, 356 + 25))
                screen.blit(label23, (853, 382 + 25))

            if len(clients) > 4:
                label21 = render(
                    f"Имя: {clients[4].return_client().return_name()}   Фамилия: {clients[4].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[4].return_thing() == 'car':
                    type2 = "авто"
                elif clients[4].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[4].return_date() + clients[4].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[4].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[4].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (430, 430 + 25))
                screen.blit(label22, (430, 456 + 25))
                screen.blit(label23, (430, 482 + 25))

            if len(clients) > 5:
                label21 = render(
                    f"Имя: {clients[5].return_client().return_name()}   Фамилия: {clients[5].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[5].return_thing() == 'car':
                    type2 = "авто"
                elif clients[5].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[5].return_date() + clients[5].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[5].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[5].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (853, 430 + 25))
                screen.blit(label22, (853, 456 + 25))
                screen.blit(label23, (853, 482 + 25))

            if len(clients) > 6:
                label21 = render(
                    f"Имя: {clients[6].return_client().return_name()}   Фамилия: {clients[6].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[6].return_thing() == 'car':
                    type2 = "авто"
                elif clients[6].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[6].return_date() + clients[6].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[6].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[6].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (430, 529 + 25))
                screen.blit(label22, (430, 555 + 25))
                screen.blit(label23, (430, 581 + 25))

            if len(clients) > 7:
                label21 = render(
                    f"Имя: {clients[7].return_client().return_name()}   Фамилия: {clients[7].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[7].return_thing() == 'car':
                    type2 = "авто"
                elif clients[7].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[7].return_date() + clients[7].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[7].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[7].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (853, 529 + 25))
                screen.blit(label22, (853, 555 + 25))
                screen.blit(label23, (853, 581 + 25))

            if len(clients) > 8:
                label21 = render(
                    f"Имя: {clients[8].return_client().return_name()}   Фамилия: {clients[8].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[8].return_thing() == 'car':
                    type2 = "авто"
                elif clients[8].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[8].return_date() + clients[8].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[8].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[8].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (430, 627 + 25))
                screen.blit(label22, (430, 653 + 25))
                screen.blit(label23, (430, 679 + 25))

            if len(clients) > 9:
                label21 = render(
                    f"Имя: {clients[9].return_client().return_name()}   Фамилия: {clients[9].return_client().return_fam()}",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                if clients[9].return_thing() == 'car':
                    type2 = "авто"
                elif clients[9].return_thing() == "health":
                    type2 = "здоровье"
                else:
                    type2 = "недвижимость"

                mes2 = clients[9].return_date() + clients[9].return_time()
                years2 = 2023
                while mes2 > 12:
                    years2 += 1
                    mes2 -= 12

                label22 = render(f"Тип: {type2}   Срок: до 1/{mes2}/{years2}", text_notebook, gfcolor=YELLOW,
                                 ocolor=BLACK,
                                 opx=2)
                label23 = render(
                    f"Взнос: {clients[9].return_usloviya().return_vznos()}₽   Макс. выплата: {clients[9].return_usloviya().return_max()}₽",
                    text_notebook, gfcolor=YELLOW, ocolor=BLACK, opx=2)

                screen.blit(label21, (853, 627 + 25))
                screen.blit(label22, (853, 653 + 25))
                screen.blit(label23, (853, 679 + 25))

    enter.draw()
    clock.tick(24 if speed == 1 else 24 * speed * 1.3)
    pygame.display.flip()
