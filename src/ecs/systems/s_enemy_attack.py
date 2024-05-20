import esper
import pygame
import random
from src.ecs.components.c_enemy_bullet_spawner import CEnemyBulletSpawner
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_enemy_steering import CEnemySteering
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
                enemies_steering_components = world.get_components(CEnemySteering)
                if len (enemies_steering_components) < 2:
                    enemies_components_updated = eliminate_already_selected(enemies_components, enemies_steering_components)
                    enemy_selected = random.choice(enemies_components_updated)
                    
                    enemy_initial_position = pygame.Vector2(enemy_selected[1][0].pos.x, enemy_selected[1][0].pos.y) 
                    world.add_component(enemy_selected[0], CEnemySteering(enemy_selected[0], enemy_initial_position))   
                    world.add_component(enemy_selected[0], CEnemyBulletSpawner(level_info))
                    ServiceLocator.sounds_service.play(level_info["enemy_attack_sound"])
 
        
def random_attack_time()->float:
    return random.uniform(2.0, 10.0)

def eliminate_already_selected(enemies_components:list, enemies_steering_components:list)->list:
    i = 0
    for enemy, (_, _, _) in enemies_components:
        for enemy_steering, (_) in enemies_steering_components:
            if enemy == enemy_steering:
                enemies_components.remove(enemies_components[i])
        i += 1    
    return enemies_components


