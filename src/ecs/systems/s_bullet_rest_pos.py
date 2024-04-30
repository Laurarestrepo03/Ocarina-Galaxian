import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_bullet_rest_pos(ecs_world:esper.World):
    bullet_components = ecs_world.get_components(CTransform, CSurface, CTagBullet)
    player_components = ecs_world.get_components(CTransform, CSurface, CTagPlayer)

    for _, (b_c_t, b_c_s, c_tb) in bullet_components:
        if not c_tb.fired:
            for _, (p_c_t, p_c_s, _) in player_components:
                bullet_size = b_c_s.surf.get_size()
                player_pos = p_c_t.pos
                player_size = p_c_s.area.size
                b_c_t.pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2), 
                         player_pos.y - (bullet_size[1]) + 2)

