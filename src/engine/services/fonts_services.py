import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}
        pass
    
    def get(self, path:str, size:int) -> pygame.font:
        if path not in self._fonts or size != self._fonts:
            self._fonts[path] = pygame.font.Font(path, size)
        return self._fonts[path]
    