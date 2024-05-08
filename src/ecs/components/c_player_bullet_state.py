from enum import Enum

class CPLayerBulletState():
    def __init__(self) -> None:
        self.state = PlayerBulletState.NOT_FIRED


class PlayerBulletState(Enum):
    NOT_FIRED = 0
    FIRED = 1
    COLLISIONED = 2