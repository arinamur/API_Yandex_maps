import os
import sys
import math

import pygame

from geocoder import *

lon, lat = get_ll_coord('Лаврушинский пер., 10, стр. 4, Москва, Россия')
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
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


def update(event):
    global zoom, lon, lat, ind_type
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
    elif event.key == pygame.K_t:
        ind_type = (ind_type + 1) % 3


pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            update(event)
    view_map()
pygame.quit()

os.remove(map_file)
