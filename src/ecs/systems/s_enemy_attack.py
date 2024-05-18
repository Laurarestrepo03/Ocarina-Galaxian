import esper
import pygame
import random
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


def system_enemy_attack(world:esper.World, delta_time:float, level_info:dict):
    
    enemy_attack_component = world.get_component(CLevel)
    
    for _, (c_ea) in enemy_attack_component:
        c_ea.current_attack_interval += delta_time
        
        if c_ea.current_attack_interval >= random_attack_time():
            c_ea.current_attack_interval = 0
            enemies_components = world.get_components(CTransform, CVelocity, CTagEnemy)
            if len(enemies_components) >= 1:
                enemies_steering_components = world.get_components(CSteering)
                print("Cantidad steerings: " + str(len(enemies_steering_components)))
                if len (enemies_steering_components) < 2:
                        enemy_selected = random.choice(enemies_components)
                        enemy_initial_position = pygame.Vector2(enemy_selected[1][0].pos.x, enemy_selected[1][0].pos.y) 
                        #print("Posicion inicial:" + str(enemy_initial_position))
                        world.add_component(enemy_selected[0], CSteering(enemy_selected[0], enemy_initial_position))   
                        #print("primer posicion inicial en CSterring:" + str(enemy_initial_position))        
                        ServiceLocator.sounds_service.play(level_info["enemy_attack_sound"])
                        #world.remove_component(enemy_selected, )
        
def random_attack_time()->float:
    return random.uniform(2.0, 10.0)