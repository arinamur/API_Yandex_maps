import os
import sys

import pygame
import requests

from geocoder import *
from distance import *
from business import *

api_server = "http://static-maps.yandex.ru/1.x/"

lon, lat = get_ll_coord('Лаврушинский пер., 10, стр. 4, Москва, Россия')
zoom = 17

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

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
