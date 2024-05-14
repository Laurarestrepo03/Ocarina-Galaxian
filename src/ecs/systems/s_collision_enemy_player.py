import esper
import pygame
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_collision_enemy_player(world:esper.World, player_entity:int, player_info:dict, explosion_cfg:dict ):
                       
    player_components = world.get_components(CSurface, CTransform, CTagPlayer)
    enemies_components = world.get_components(CSurface, CTransform, CTagEnemy)

    for player_entity, (p_c_s, p_c_t, _) in player_components:
        pl_rect = CSurface.get_area_relative(p_c_s.area, p_c_t.pos)
        for enemy_entity, (e_c_s, e_c_t, e_te) in enemies_components:
            e_rect = e_c_s.area.copy()
            e_rect.topleft = e_c_t.pos
            if pl_rect.colliderect(e_rect):
                world.delete_entity(enemy_entity)
                #world.delete_entity(player_entity)
                create_explosion(world, pl_rect, p_c_s.area.size, explosion_cfg)