import pygame

class CSteering:
    def __init__(self):
        self.follow_vector:pygame.Vector2 = pygame.Vector2(0,0)
        self.avoid_vector:pygame.Vector2 = pygame.Vector2(0,0)