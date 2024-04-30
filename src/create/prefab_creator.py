
import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator
    
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

def create_player(ecs_world:esper.World, player_info:dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_info["image"])
    size = player_surface.get_rect().size
    pos = pygame.Vector2(player_info["spawn_point"]["x"] - (size[0]/2),
                         player_info["spawn_point"]["y"] - (size[1]/2))
    vel = pygame.Vector2(0,0)
    player_entity = create_sprite(ecs_world, pos, vel, player_surface)
    ecs_world.add_component(player_entity, CTagPlayer())
    #ecs_world.add_component(player_entity, CAnimation(player_info["animations"]))
    #ecs_world.add_component(player_entity, CPlayerState())
    return player_entity

def create_bullet(ecs_world:esper.World, bullet_info:dict, player_pos:pygame.Vector2) -> int:
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    pos = pygame.Vector2(0,0)
    vel = pygame.Vector2(0,0)
    bullet_entity = create_sprite(ecs_world, pos, vel, bullet_surface)
    ecs_world.add_component(bullet_entity, CTagBullet())
    return bullet_entity
    #ServiceLocator.sounds_service.play(bullet_info["sound"])

def create_input_player(ecs_world:esper.World):
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_space = ecs_world.create_entity()
    #input_p = ecs_world.create_entity()

    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", [pygame.K_LEFT, pygame.K_a]))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", [pygame.K_RIGHT, pygame.K_d]))
    ecs_world.add_component(input_space, CInputCommand("PLAYER_FIRE", [pygame.K_SPACE]))
    #ecs_world.add_component(input_p, CInputCommand("PLAYER_PAUSE", [pygame.K_p]))