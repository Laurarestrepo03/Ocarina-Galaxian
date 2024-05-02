from enum import Enum

class CTagBullet():
    def __init__(self, type:int) -> None:
        self.fired = False
        self.type = type

class BulletType(Enum):
    PLAYER = 0
    ENEMY = 1