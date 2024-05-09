import pygame

class CLevel:
    def __init__(self, high_score:int, enemies_count:int) -> None:
        self.high_score = high_score
        self.enemies_count = enemies_count
        self.points = 0
        self.enemy_destroyed = None

