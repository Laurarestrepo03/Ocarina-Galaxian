import esper
import pygame
import random

from src.create.prefab_creator import create_bullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, FiringState

def system_enemy_bullet_spawn(ecs_world:esper.World, bullet_cfg:dict, enemies_cfg: dict, delta_time:float):
    components = ecs_world.get_components(CTransform, CTagEnemy)
    firing_enemy = -1
    non_fired_entities = []

    for enemy_entity, (_, c_te) in components:
        if c_te.firing_state == FiringState.FIRING:
            firing_enemy = enemy_entity
        elif c_te.firing_state == FiringState.NOT_FIRED:
            non_fired_entities.append(enemy_entity)

    if firing_enemy > -1:
        c_te = ecs_world.component_for_entity(firing_enemy, CTagEnemy)
        c_te.timer += delta_time

        if c_te.timer > 0.2:
            c_t = ecs_world.component_for_entity(firing_enemy, CTransform)
            pos = c_t.pos.copy()
            c_s = ecs_world.component_for_entity(firing_enemy, CSurface)
            area = c_s.area.copy()
            size = area.size
            final_pos = pygame.Vector2(pos.x + (size[0] / 2) - (bullet_cfg["size"]["x"] / 2),
                                       pos.y + (size[1] / 2))
            vel = pygame.Vector2(0, 1)
            vel = vel.normalize() * bullet_cfg["velocity"]

            create_bullet(ecs_world, bullet_cfg, final_pos, vel, "ENEMY")

            c_te.timer = 0
            c_te.bullets_fired += 1

            if c_te.bullets_fired == enemies_cfg[c_te.type]["bullet_count"]:
                c_te.firing_state = FiringState.FIRED 

    elif len(non_fired_entities) > 0:
        random_enemy = random.choice(non_fired_entities)
        c_te = ecs_world.component_for_entity(random_enemy, CTagEnemy)
        c_te.firing_state = FiringState.FIRING

    elif len(non_fired_entities) == 0:
        for enemy_entity, (_, c_te) in components:
            c_te.firing_state = FiringState.NOT_FIRED
    
