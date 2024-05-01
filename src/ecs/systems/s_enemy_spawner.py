import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner, Line
from src.create.prefab_creator import create_enemy

def system_enemy_spawner(world:esper.World, enemies:dict):
    components = world.get_component(CEnemySpawner)

    c_esp:CEnemySpawner
            
    for _, c_esp in components:
        line:Line
        for line in c_esp.lines:
            for i in range(0, line.number_enemies):
                position = pygame.Vector2(line.position["x"] + (line.gap*i), line.position["y"])
                create_enemy(world, position, enemies[line.enemy_type])    
    
