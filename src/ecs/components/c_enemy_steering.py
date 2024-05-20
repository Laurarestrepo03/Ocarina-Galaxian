import pygame
from enum import Enum

class CEnemySteering:
    def __init__(self, entity:int, initial_position:pygame.Vector2):
        self.entity = entity
        self.return_position = initial_position
        self.state = EnemySteeringState.JUMPING
        self.jumping_counter = 0
        
class EnemySteeringState(Enum):
    HUNTING = 0
    RETURNING = 1
    JUMPING = 2