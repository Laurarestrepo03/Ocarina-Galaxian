import esper
import pygame

from src.create.prefab_creator import create_bullet
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

def system_player_bullet_spawn(ecs_world:esper.World, bullet_cfg: dict):
    bullet_count = len(ecs_world.get_component(CTagPlayerBullet))

    if bullet_count < 1:
        pos = pygame.Vector2(0,0)
        vel = pygame.Vector2(0,0)
        create_bullet(ecs_world, bullet_cfg, pos, vel, "PLAYER")