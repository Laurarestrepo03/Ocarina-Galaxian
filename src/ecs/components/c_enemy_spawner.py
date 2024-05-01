import pygame

class CEnemySpawner:
    def __init__(self, level:dict) -> None:
        self.ahora:float = 0
        self.lines:list[Line] = []       
        for line in level["lines"]:
            self.lines.append(Line(line))
                    
class Line:
    def __init__(self, line:dict) -> None:
        self.enemy_type = line["enemy_type"]
        self.position = line["position"]
        self.number_enemies = line["number_enemies"]
        self.gap = line["gap"]
