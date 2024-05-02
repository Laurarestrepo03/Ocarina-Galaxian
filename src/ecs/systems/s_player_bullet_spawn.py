import esper
import pygame

from src.create.prefab_creator import create_bullet
from src.ecs.components.tags.c_tag_bullet import BulletType, CTagBullet

def system_player_bullet_spawn(ecs_world:esper.World, player_bullet_cfg: dict):
    bullet_count = len(ecs_world.get_component(CTagBullet))
    if bullet_count < 1:
        create_bullet(ecs_world, player_bullet_cfg, BulletType.PLAYER)