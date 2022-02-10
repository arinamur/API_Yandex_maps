import math
import os
import sys

import pygame

from geocoder import *
from classes import InputAddress, Button

lon = lat = -1
zoom = 14
map_file = "map.png"
types = ['map', 'sat', 'sat,skl']
ind_type = 0


def view_map():
    global lon, lat, zoom, map_file, types, ind_type

    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": f"{lon},{lat}",
        "z": zoom,
        "l": types[ind_type]
    }
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return

    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))


def update(event):
    global zoom, lon, lat, ind_type, Address
    STEP = 0.004
    coord_to_geo = 0.0000428
    if event.key == pygame.K_PAGEUP and zoom < 19:
        zoom += 1
    elif event.key == pygame.K_PAGEDOWN and zoom > 2:
        zoom -= 1
    elif event.key == pygame.K_LEFT:
        lon -= STEP * math.pow(2, 14 - zoom)
    elif event.key == pygame.K_RIGHT:
        lon += STEP * math.pow(2, 14 - zoom)
    elif event.key == pygame.K_UP and lat + STEP * math.pow(2, 14 - zoom) < 90:
        lat += STEP * math.pow(2, 14 - zoom)
    elif event.key == pygame.K_DOWN and lat - STEP * math.pow(2, 14 - zoom) > -90:
        lat -= STEP * math.pow(2, 14 - zoom)
    elif event.key == pygame.K_TAB:
        ind_type = (ind_type + 1) % 3
    else:
        if Address.active:
            if event.key == pygame.K_BACKSPACE:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    Address.text = ''
                else:
                    Address.text = Address.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                Address.active = False
            else:
                Address.text += event.unicode


def swap(text):
    global lon, lat
    lon, lat = get_ll_coord(text)


pygame.init()
screen = pygame.display.set_mode((600, 450))

all_sprites = pygame.sprite.Group()
Address = InputAddress('Лаврушинский пер., 10, стр. 4, Москва, Россия', 5, 5, all_sprites)
Search = Button('Искать', 5, 30, all_sprites)

swap(Address.text)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            update(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if Address.check_click(event.pos):
                Address.active = not Address.active
            else:
                Address.active = False
            if Search.check_click(event.pos):
                swap(Address.text)
    screen.fill((0, 0, 0))
    view_map()
    for obj in all_sprites:
        obj.render(screen)
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
