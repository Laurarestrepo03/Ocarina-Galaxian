import esper
import pygame
import random

from src.create.prefab_creator import create_bullet
from src.ecs.components.c_enemy_bullet_spawner import CEnemyBulletSpawner
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import BulletType
from src.ecs.components.tags.c_tag_enemy import CTagEnemy, FiringState

def system_enemy_bullet_spawn(ecs_world:esper.World, bullet_cfg:dict, enemies_cfg: dict, lvl_cfg:dict, delta_time:float, game_manager_entity):
    spawner_component = ecs_world.get_component(CEnemyBulletSpawner)
    game_state = ecs_world.component_for_entity(game_manager_entity,CGameState)
    if game_state.state != GameState.GAME_OVER:
        for _, (c_spa) in spawner_component:
            if c_spa.timer < c_spa.max_time:
                c_spa.timer += delta_time
            else:
                enemy_components = ecs_world.get_components(CTransform, CTagEnemy)
                firing_enemy = None
                non_fired_entities = []
                fired_entities = []

                for enemy_entity, (_, c_te) in enemy_components:
                    if c_te.firing_state == FiringState.FIRING:
                        firing_enemy = enemy_entity
                        break
                    elif c_te.firing_state == FiringState.NOT_FIRED:
                        non_fired_entities.append(enemy_entity)
                    elif c_te.firing_state == FiringState.FIRED:
                        fired_entities.append(enemy_entity)

                if len(fired_entities) == len(enemy_components):
                    for enemy_entity, (_, c_te) in enemy_components:
                        c_te.firing_state = FiringState.NOT_FIRED
                    non_fired_entities = fired_entities

                if firing_enemy:
                    c_te = ecs_world.component_for_entity(firing_enemy, CTagEnemy)
                    c_te.timer += delta_time

                    if c_te.timer > 0.15:
                        c_t = ecs_world.component_for_entity(firing_enemy, CTransform)
                        pos = c_t.pos.copy()
                        c_s = ecs_world.component_for_entity(firing_enemy, CSurface)
                        area = c_s.area.copy()
                        size = area.size
                        final_pos = pygame.Vector2(pos.x + (size[0] / 2) - (bullet_cfg["size"]["x"] / 2),
                                                pos.y + (size[1] / 2))
                        vel = pygame.Vector2(0, 1)
                        vel = vel.normalize() * bullet_cfg["velocity"]

                        create_bullet(ecs_world, bullet_cfg, final_pos, vel, BulletType.ENEMY)

                        c_te.timer = 0
                        c_te.bullets_fired += 1

                        if c_te.bullets_fired == enemies_cfg[c_te.type]["bullet_count"]:
                            
                            c_te.firing_state = FiringState.FIRED
                            c_te.bullets_fired = 0
                            c_spa.timer = 0
                            CEnemyBulletSpawner.change_max_time(lvl_cfg)
                
                elif len(non_fired_entities) > 0:
                    random_enemy = random.choice(non_fired_entities)
                    c_te = ecs_world.component_for_entity(random_enemy, CTagEnemy)
                    c_te.firing_state = FiringState.FIRING

    
    
