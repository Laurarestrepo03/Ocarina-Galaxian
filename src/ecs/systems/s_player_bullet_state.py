import esper
import pygame

from src.ecs.components.c_player_bullet_state import CPLayerBulletState, PlayerBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_bullet_state(ecs_world:esper.World):
    components = ecs_world.get_components(CTransform, CSurface, CPLayerBulletState)
    
    for _, (c_t, c_s, c_pbs) in components:
        if c_pbs.state == PlayerBulletState.NOT_FIRED:
            _do_not_fired_state(ecs_world, c_t, c_s)
        elif c_pbs.state == PlayerBulletState.FIRED:
             pass

def _do_not_fired_state(ecs_world: esper.World, c_t:CTransform, c_s:CSurface):
    player_components = ecs_world.get_components(CTransform, CSurface, CTagPlayer)

    for _, (p_c_t, p_c_s, _) in player_components:
            bullet_size = c_s.area.size
            player_pos = p_c_t.pos
            player_size = p_c_s.area.size
            c_t.pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2), 
                        player_pos.y - (bullet_size[1]) + 1) # + 1 porque el jugador tiene un espacio
     