import esper
import pygame
from src.create.prefab_creator import create_bullet
from src.ecs.components.c_enemy_bullet_spawner_hunting import CEnemyBulletSpawnerHunting
from src.ecs.components.c_enemy_steering import CEnemySteering, EnemySteeringState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import BulletType

def system_enemy_attack_fire(world:esper.World, bullet_info:dict, delta_time:float):
    enemy_steering_components = world.get_component(CEnemySteering)
    for entity, (c_es) in enemy_steering_components:
        
        c_bs = world.component_for_entity(entity, CEnemyBulletSpawnerHunting)       
        if c_es.state == EnemySteeringState.HUNTING:
            if c_bs.timer < c_bs.max_time * 3 and c_es.state == EnemySteeringState.HUNTING :
                c_bs.timer += delta_time
            else:
                c_t = world.component_for_entity(entity, CTransform)
                c_bs.timer = 0
                pos = c_t.pos.copy()
                c_s = world.component_for_entity(entity, CSurface)
                area = c_s.area.copy()
                size = area.size
                final_pos = pygame.Vector2(pos.x + (size[0] / 2) - (bullet_info["size"]["x"] / 2), pos.y + (size[1] / 2))
                vel = pygame.Vector2(0, 1)
                vel = vel.normalize() * bullet_info["velocity"]
                create_bullet(world, bullet_info, final_pos, pygame.Vector2(0, 1).normalize() * bullet_info["velocity"], BulletType.ENEMY)