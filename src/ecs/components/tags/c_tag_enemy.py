from enum import Enum

class CTagEnemy:
    def __init__(self, type:str) -> None:
        self.type = type
        self.bullets_fired = 0
        self.firing_state = FiringState.NOT_FIRED
        self.timer = 0

class FiringState(Enum):
    NOT_FIRED = 0
    FIRING = 1
    FIRED = 2

