
import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator

def create_square(ecs_world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color):
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                CTransform(pos))
    ecs_world.add_component(cuad_entity, 
                CVelocity(vel))
    
def create_sprite(ecs_world:esper.World, pos:pygame.Vector2, vel:pygame.Vector2, 
                  surface:pygame.Vector2) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, 
                            CTransform(pos))
    ecs_world.add_component(sprite_entity, 
                            CVelocity(vel))
    ecs_world.add_component(sprite_entity,
                            CSurface.from_surface(surface))
    return sprite_entity

def create_enemy_square(ecs_world:esper.World, position:pygame.Vector2, enemy_info:dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])  
    print("type: "+ enemy_info["type"] + " size: " + str(enemy_surface.get_size()))   
    '''vel_min = enemy_info["velocity_min"]
    vel_max = enemy_info["velocity_max"]

    if vel_min == vel_max:
        vel_range = vel_min
    else:
        vel_range = random.randrange(vel_min, vel_max)'''
    
    velocity = pygame.Vector2(0, 0)

    enemy_entity = create_sprite(ecs_world, position, velocity, enemy_surface)    
    ecs_world.add_component(enemy_entity, CTagEnemy())
    #ecs_world.add_component(enemy_entity, CTagEnemyAsteroid())
    ##ServiceLocator.sounds_service.play(enemy_info["sound"])  
    
def create_level(ecs_world:esper.World, level):
    level_entity = ecs_world.create_entity()
    ecs_world.add_component(level_entity, CEnemySpawner(level))