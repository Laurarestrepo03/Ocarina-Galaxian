import pygame

class CEnemySpawner:
    def __init__(self, level:dict) -> None:
        self.ahora:float = 0
        self.enemies:list[Enemy] = []       
        for enemy in level["enemies"]:
            self.enemies.append(Enemy(enemy))       
            
class Enemy:
    def __init__(self, event:dict) -> None:
        self.enemy_type:str = event["enemy_type"]
        self.position:pygame.Vector2 = pygame.Vector2(event["position"]["x"], event["position"]["y"])
