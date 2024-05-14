import esper
import pygame
import random
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemy_attack(world:esper.World, delta_time:float, enemy_attack_time:float, self):
    
    self.current_attack_interval += delta_time
    
    if self.current_attack_interval >= random_attack_time():
       self.current_attack_interval = 0
       enemies_components = world.get_components(CTransform, CVelocity, CTagEnemy)
       if len(enemies_components) >= 1:
            enemy_selected = random .choice(enemies_components)
            #world.delete_entity(enemy_selected[0])
            world.add_component(enemy_selected[0], CSteering())
    
    
def random_attack_time()->float:
    return random.uniform(2.0, 10.0)