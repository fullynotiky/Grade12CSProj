from csv import reader
from os import walk

from pygame import image


def getLayout(path: str):
    map = []

    with open(path) as file:
        layout = reader(file, delimiter=',')

        for row in layout:
            map.append(list(row))

    return map


def getFolder(path):
    surfs = []

    for _, __, imgFiles in walk(path):
        for img in imgFiles:
            fullPath = path + f'\\{img}'
            surf = image.load(fullPath).convert_alpha()
            surfs.append(surf)

    return surfs
