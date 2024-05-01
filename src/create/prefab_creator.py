
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner, Line
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

def create_enemy(ecs_world:esper.World, position:pygame.Vector2, enemy_info:dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])  
    
    size = enemy_surface.get_size()
    number_frames = enemy_info["animation"]["number_frames"]
    size = pygame.Vector2(size[0]/number_frames, size[1])
    
    position = pygame.Vector2(position.x - size[0]/2, position.y - size[1]/2)
    velocity = pygame.Vector2(0, 0)

    enemy_entity = create_sprite(ecs_world, position, velocity, enemy_surface)    
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ##ServiceLocator.sounds_service.play(enemy_info["sound"])  
    ecs_world.add_component(enemy_entity, CAnimation(enemy_info["animation"]))
    
def create_level(ecs_world:esper.World, level_info, enemies_info):
    level_entity = ecs_world.create_entity()   
    line:Line
    for line in level_info["lines"]:
        for i in range(0, line["number_enemies"]):
            position = pygame.Vector2(line["position"]["x"] + (line["gap"]*i), line["position"]["y"])
            create_enemy(ecs_world, position, enemies_info[line["enemy_type"]])    
    
    