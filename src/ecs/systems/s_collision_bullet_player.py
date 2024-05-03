import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_collision_bullet_player(ecs_world:esper.World, explosion_cfg:dict):
    player_components = ecs_world.get_components(CSurface, CTransform, CTagPlayer)
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagEnemyBullet)

    for player_entity, (p_c_s, p_c_t, _) in player_components:
        pl_rect = CSurface.get_area_relative(p_c_s.area, p_c_t.pos)
        for bullet_entity, (b_c_s, b_c_t, _) in bullet_components:
            bl_rect = b_c_s.area.copy()
            bl_rect.topleft = b_c_t.pos
            if pl_rect.colliderect(bl_rect):
                #TODO: quitar comentario cuando se implemente reinicio
                #ecs_world.delete_entity(player_entity)
                ecs_world.delete_entity(bullet_entity)
                create_explosion(ecs_world, pl_rect, p_c_s.area.size, explosion_cfg)