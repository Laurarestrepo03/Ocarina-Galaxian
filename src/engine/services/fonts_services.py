

import pygame

class FontsServices:
    def __init__(self) -> None:
        self._text = {}

    def get_font(self, path:str, size: int):
        key = (path, size)
        if key not in self._text:
            self._text[key] = pygame.font.Font(path,size)
        return self._text[key]
