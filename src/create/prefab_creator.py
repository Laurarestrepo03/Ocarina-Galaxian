
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_enemy_bullet_spawner import CEnemyBulletSpawner
from src.ecs.components.c_enemy_movement import CEnemyMovement
from src.ecs.components.c_enemy_spawner import Line
from src.ecs.components.c_explosion_state import CExplosionState
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_player_bullet_state import CPLayerBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import BulletType, CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_high_score import CTagHighScore
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.ecs.components.tags.c_tag_score import CTagScore
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def create_square(ecs_world:esper.World, size:pygame.Vector2,
                   pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                                    CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                                    CTransform(pos))
    ecs_world.add_component(cuad_entity,
                                    CVelocity(vel))
    return cuad_entity
    
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
    
def create_life(ecs_world:esper.World, interface_info:dict):
    desface = 0.5
    number = 1
    for _ in range(interface_info["lifes"]["lifes_number"]):
        life_surface = ServiceLocator.images_service.get(interface_info["lifes"]["image"])
        size = life_surface.get_rect().size
        pos = pygame.Vector2(interface_info["lifes"]["position"]["x"] + desface,
                            interface_info["lifes"]["position"]["y"])
        desface += size[0]
        vel = pygame.Vector2(0,0)
        life_entity = create_sprite(ecs_world, pos, vel, life_surface)
        ecs_world.add_component(life_entity, CTagLife(number))
        number+=1

def create_flag(ecs_world:esper.World, interface_info:dict):
    flag_surface = ServiceLocator.images_service.get(interface_info["level_flag"]["image"])
    size = flag_surface.get_rect().size
    pos = pygame.Vector2(interface_info["level_flag"]["position"]["x"] ,
                            interface_info["level_flag"]["position"]["y"])
    vel = pygame.Vector2(0,0)
    create_sprite(ecs_world, pos, vel, flag_surface)
    

def create_player(ecs_world:esper.World, player_info:dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_info["image"])
    size = player_surface.get_rect().size
    pos = pygame.Vector2(player_info["spawn_point"]["x"] - (size[0]/2),
                         player_info["spawn_point"]["y"] - (size[1]/2))
    vel = pygame.Vector2(0,0)
    player_entity = create_sprite(ecs_world, pos, vel, player_surface)
    ecs_world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_bullet(ecs_world:esper.World, bullet_info:dict, pos:pygame.Vector2, 
                  vel:pygame.Vector2, type:int) -> int:
    size = pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"])
    col = pygame.Color(bullet_info["color"]["r"], bullet_info["color"]["g"], bullet_info["color"]["b"])
    bullet_entity = create_square(ecs_world, size, pos, vel, col)
    if type == BulletType.PLAYER:
        ecs_world.add_component(bullet_entity, CPLayerBulletState())
        ecs_world.add_component(bullet_entity, CTagBullet(BulletType.PLAYER))
    elif type == BulletType.ENEMY:
        ecs_world.add_component(bullet_entity, CTagBullet(BulletType.ENEMY))
    return bullet_entity
    
def create_input_player(ecs_world:esper.World):
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_space = ecs_world.create_entity()
    input_pause = ecs_world.create_entity()
    #input_p = ecs_world.create_entity()

    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", [pygame.K_LEFT, pygame.K_a]))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", [pygame.K_RIGHT, pygame.K_d]))
    ecs_world.add_component(input_space, CInputCommand("PLAYER_FIRE", [pygame.K_SPACE, pygame.K_z]))
    ecs_world.add_component(input_pause, CInputCommand("PAUSE", [pygame.K_p, pygame.K_m]))
    #ecs_world.add_component(input_p, CInputCommand("PLAYER_PAUSE", [pygame.K_p]))

def create_star(ecs_world:esper.World, window_cfg, starfield_cfg):
    for _ in range(starfield_cfg["number_of_stars"]):
        star_size = pygame.Vector2(starfield_cfg["size"]["h"], starfield_cfg["size"]["w"])
        star_pos = pygame.Vector2(random.randint(0, window_cfg["size"]["w"]),
                             random.randint(0, window_cfg["size"]["h"]))
        star_vel = pygame.Vector2(random.uniform(0, 0), random.uniform(starfield_cfg["vertical_speed"]["min"], starfield_cfg["vertical_speed"]["max"]))
        star_color = random.choice(starfield_cfg["star_colors"])
        star_color = pygame.Color(star_color["r"], star_color["g"], star_color["b"])
        star_entity = create_square(ecs_world, star_size, star_pos, star_vel, star_color)
        ecs_world.add_component(star_entity, CBlink(starfield_cfg["blink_rate"]["min"], starfield_cfg["blink_rate"]["max"]))
        ecs_world.add_component(star_entity, CTagStar())

def create_enemy(ecs_world:esper.World, position:pygame.Vector2, velocity:int,
                  enemy_info:dict, type:str):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])  
    
    size = enemy_surface.get_size()
    number_frames = enemy_info["animations"]["number_frames"]
    size = pygame.Vector2(size[0]/number_frames, size[1])
    
    position = pygame.Vector2(position.x - size[0]/2, position.y - size[1]/2)
    velocity = pygame.Vector2(velocity, 0)

    enemy_entity = create_sprite(ecs_world, position, velocity, enemy_surface)    
    ecs_world.add_component(enemy_entity, CTagEnemy(type))
    ecs_world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
    
def create_level(ecs_world:esper.World, level_info, enemies_info, interface_info):
    level_component = ecs_world.get_component(CLevel)
    if len(level_component) == 0:
        level_entity = ecs_world.create_entity()  
        ecs_world.add_component(level_entity, CLevel(interface_info))
        ecs_world.add_component(level_entity, CEnemyMovement())
     
    line:Line
    #velocity = pygame.Vector2(level_info["velocity"], 0)
    velocity = level_info["velocity"]
    enemies_count = 0
    for line in level_info["lines"]:
        for i in range(0, line["number_enemies"]):
            position = pygame.Vector2(line["position"]["x"] + (line["gap"]*i), line["position"]["y"])
            create_enemy(ecs_world, position, velocity, enemies_info[line["enemy_type"]], line["enemy_type"]) 
            enemies_count +=1
            
    return enemies_count

def create_explosion(ecs_world:esper.World, pos:pygame.Vector2, entity_size:pygame.Vector2, explosion_info:dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    size = explosion_surface.get_size()
    size = (size[0] / explosion_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(pos.x + (entity_size[0] / 2) - (size[0] / 2), 
                         pos.y + (entity_size[1] / 2) - (size[1] / 2))
    vel = pygame.Vector2(0,0)
    explosion_entity = create_sprite(ecs_world, pos, vel, explosion_surface)
    ecs_world.add_component(explosion_entity, CAnimation(explosion_info["animations"]))
    ecs_world.add_component(explosion_entity, CExplosionState())
    ServiceLocator.sounds_service.play(explosion_info["sound"])

def create_text(world:esper.World, text_info:dict, text=None) -> int:
    if text is None:
        text = text_info["text"]
    
    text_font = ServiceLocator.fonts_service.get_font(text_info["font"], text_info["size"])
    text_color = pygame.Vector3(text_info["color"]["r"], text_info["color"]["g"], text_info["color"]["b"])    
    surface = CSurface.from_text(text,text_font,text_color)
    text_size = surface.surf.get_size()
    
    text_pos = pygame.Vector2(text_info["position"]["x"] - text_size[0]/2, text_info["position"]["y"] - text_size[1]/2)
    
    
    text_entity = world.create_entity()
    world.add_component(text_entity, CTransform(text_pos))
    world.add_component(text_entity, CSurface.from_text(text, text_font, text_color))
    
    return text_entity

def create_enemy_bullet_spawner(ecs_world:esper.World, lvl_info:dict):
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, CEnemyBulletSpawner(lvl_info))
