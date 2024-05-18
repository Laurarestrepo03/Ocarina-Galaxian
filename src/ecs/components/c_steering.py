import pygame
from enum import Enum

class CSteering:
    def __init__(self, entity:int, initial_position:pygame.Vector2):
        #self.follow_vector:pygame.Vector2 = pygame.Vector2(0,0)
        #self.avoid_vector:pygame.Vector2 = pygame.Vector2(0,0)
        self.entity = entity
        self.return_position = initial_position
        self.state = SteeringState.HUNTING
        
class SteeringState(Enum):
    HUNTING = 0
    RETURNING = 1
    GROUP = 2