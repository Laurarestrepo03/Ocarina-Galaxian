class CLevel:
    def __init__(self, interface_info:dict) -> None:
        self.high_score = interface_info["high_score_value"]["text"]
        self.score = 0
        self.enemy_destroyed = None
        
        self.current_attack_interval = 0
        
        self.direction = 1
        self.x_relative_position = 0
        self.vel = 0