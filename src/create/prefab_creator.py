
import random
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
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_star_field import CStarField
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
    
def create_star(ecs_world:esper.World, window_cfg, starfield_cfg):
    window_width = window_cfg["size"]["w"]
    window_height = window_cfg["size"]["h"]
    num_stars = starfield_cfg["number_of_stars"]
    for _ in range(num_stars):
        pos = pygame.Vector2(random.randint(0, window_width),
                             random.randint(0, window_height))
        vel = pygame.Vector2(random.uniform(0, 0), random.uniform(starfield_cfg["vertical_speed"]["min"], starfield_cfg["vertical_speed"]["max"]))
        star_color = random.choice(starfield_cfg["star_colors"])
        star_surface = pygame.Surface((starfield_cfg["size"]["h"], starfield_cfg["size"]["w"]))
        star_surface.fill((star_color["r"], star_color["g"], star_color["b"]))
        star_entity = create_sprite(ecs_world, pos, vel, star_surface)
        ecs_world.add_component(star_entity, CStarField(window_width, window_height, star_surface, starfield_cfg["blink_rate"]["min"], starfield_cfg["blink_rate"]["max"], star_color))

def create_enemy(ecs_world:esper.World, position:pygame.Vector2, velocity:int, enemy_info:dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])  
    
    size = enemy_surface.get_size()
    number_frames = enemy_info["animation"]["number_frames"]
    size = pygame.Vector2(size[0]/number_frames, size[1])
    
    position = pygame.Vector2(position.x - size[0]/2, position.y - size[1]/2)
    velocity = pygame.Vector2(velocity, 0)

    enemy_entity = create_sprite(ecs_world, position, velocity, enemy_surface)    
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ##ServiceLocator.sounds_service.play(enemy_info["sound"])  
    ecs_world.add_component(enemy_entity, CAnimation(enemy_info["animation"]))
    
def create_level(ecs_world:esper.World, level_info, enemies_info):
    level_entity = ecs_world.create_entity()   
    line:Line
    #velocity = pygame.Vector2(level_info["velocity"], 0)
    velocity = level_info["velocity"]
    for line in level_info["lines"]:
        for i in range(0, line["number_enemies"]):
            position = pygame.Vector2(line["position"]["x"] + (line["gap"]*i), line["position"]["y"])
            create_enemy(ecs_world, position, velocity, enemies_info[line["enemy_type"]]) 
