import esper
import pygame
import random

from src.create.prefab_creator import create_bullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_bullet_spawn(ecs_world:esper.World, bullet_cfg:dict, delta_time:float):
    components = ecs_world.get_components(CTransform, CTagEnemy)

    non_fired_entities = []

    for enemy_entity, (_, c_te) in components:
        if c_te.bullets_fired == 0:
            non_fired_entities.append(enemy_entity)

    if len(non_fired_entities) == 0:
        for _, (_, c_te) in components:
            c_te.bullets_fired = 0
    else:
        random_enemy = random.choice(non_fired_entities)

        ene_c_t = ecs_world.component_for_entity(random_enemy, CTransform)
        ene_pos = ene_c_t.pos.copy()
        ene_c_s = ecs_world.component_for_entity(random_enemy, CSurface)
        ene_surf = ene_c_s.area.copy()
        ene_size = ene_surf.size
        pos = pygame.Vector2(ene_pos.x + (ene_size[0] / 2) - (bullet_cfg["size"]["x"] / 2), 
                         ene_pos.y + (ene_size[1] / 2))
        
        vel = pygame.Vector2(0, 1)
        vel = vel.normalize() * bullet_cfg["velocity"] 
        
        create_bullet(ecs_world, bullet_cfg, pos, vel, "ENEMY")