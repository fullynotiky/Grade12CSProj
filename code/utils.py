from json import load

from os import walk
from csv import reader
from pygame import image, display, init
from pygame.draw import rect
from pygame.font import Font

init()

font = Font(None, 23)
padX = padY = 10


def debug(info, y=10, x=10):
    displaySurf = display.get_surface()
    debugSurf = font.render(str(info), True, 'White')
    debugRect = debugSurf.get_rect(topleft=(x, y))

    rect(displaySurf, 'Black', debugRect)
    displaySurf.blit(debugSurf, debugRect)


def getLayout(path: str):
    map = []
    with open(path) as file:
        layout = reader(file, delimiter=',')
        for row in layout: map.append(list(row))

    return map


def getFolder(path):
    surfs = []

    for _, __, imgFiles in walk(path):
        for img in imgFiles: surfs.append(image.load(path + f'\\{img}').convert_alpha())

    return surfs


def getJsonFile(path: str):
    with open(path, 'r') as file: return load(file)
