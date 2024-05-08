import esper
import pygame

from src.ecs.components.c_player_bullet_state import CPLayerBulletState, PlayerBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import BulletType, CTagBullet

def system_bullet_limit(ecs_world:esper.World, screen:pygame.Surface):
    
    screen_rect = screen.get_rect()
    player_bullet_components = ecs_world.get_components(CTransform, CSurface, CTagBullet)

    for bullet_entity, (c_t, c_s, c_tb) in player_bullet_components:
        bullet_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(bullet_rect):
            if c_tb.type == BulletType.PLAYER:
                c_pbs = ecs_world.component_for_entity(bullet_entity, CPLayerBulletState)
                c_pbs.state = PlayerBulletState.NOT_FIRED
            elif c_tb.type == BulletType.ENEMY:
                ecs_world.delete_entity(bullet_entity)