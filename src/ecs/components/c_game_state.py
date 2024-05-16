from enum import Enum

class GameState(Enum):
    READY = 1
    PLAY = 2
    PAUSED = 3
    WIN = 4
    DEAD = 5
    GAME_OVER = 6

class CGameState():
    def __init__(self):
        self.state = GameState.READY
        self.current_time = 0
        self.current_enemyes = 0


