import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_limit(ecs_world:esper.World, screen:pygame.Surface):
    
    screen_rect = screen.get_rect()
    components = ecs_world.get_components(CTransform, CVelocity, CSurface, CTagPlayer)

    for _, (c_t, _, c_s, _) in components:
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if player_rect.left < 10:
            c_t.pos.x = 10
        elif player_rect.right > screen_rect.width - 10:
            c_t.pos.x = screen_rect.width - player_rect.width - 10
