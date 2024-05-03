import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

def system_collision_bullet_enemy(ecs_world:esper.World, explosion_cfg:dict):
    enemy_components = ecs_world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagPlayerBullet)

    for enemy_entity, (e_c_s, e_c_t, _) in enemy_components:
        ene_rect = CSurface.get_area_relative(e_c_s.area, e_c_t.pos)
        for bullet_entity, (b_c_s, b_c_t, _) in bullet_components:
            bl_rect = b_c_s.area.copy()
            bl_rect.topleft = b_c_t.pos
            if ene_rect.colliderect(bl_rect):
                ecs_world.delete_entity(enemy_entity)
                ecs_world.delete_entity(bullet_entity)
                create_explosion(ecs_world, ene_rect, e_c_s.area.size, explosion_cfg)

