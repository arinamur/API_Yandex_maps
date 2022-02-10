import math
import os
import sys

import pygame

from geocoder import *

lon, lat = get_ll_coord('Лаврушинский пер., 10, стр. 4, Москва, Россия')
zoom = 14
map_file = "map.png"


def view_map():
    global lon, lat, zoom, map_file

    api_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": f"{lon},{lat}",
        "z": zoom,
        "l": "map"
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
    global zoom, lon, lat
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
