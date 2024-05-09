import esper
import pygame

from src.create.prefab_creator import create_explosion
from src.ecs.components.c_player_bullet_state import CPLayerBulletState, PlayerBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_level import CLevel
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_bullet_state(ecs_world:esper.World, explosion_cfg:dict, self):
    components = ecs_world.get_components(CTransform, CSurface, CPLayerBulletState)
    
    response = ""
    for _, (c_t, c_s, c_pbs) in components:
        if c_pbs.state == PlayerBulletState.NOT_FIRED:
            _do_not_fired_state(ecs_world, c_t, c_s)
        elif c_pbs.state == PlayerBulletState.FIRED:
            response = _do_fired_state(ecs_world, c_t, c_s, c_pbs, explosion_cfg, self)

    return response


def _do_not_fired_state(ecs_world:esper.World, c_t:CTransform, c_s:CSurface):
    player_components = ecs_world.get_components(CTransform, CSurface, CTagPlayer)

    for _, (p_c_t, p_c_s, _) in player_components:
            bullet_size = c_s.area.size
            player_pos = p_c_t.pos
            player_size = p_c_s.area.size
            c_t.pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2), 
                        player_pos.y - (bullet_size[1]) + 1) # + 1 porque el jugador tiene un espacio
     
def _do_fired_state(ecs_world: esper.World, c_t:CTransform, c_s:CSurface, 
                    c_pbs:CPLayerBulletState, explosion_cfg:dict, self) -> str:
    enemy_components = ecs_world.get_components(CSurface, CTransform, CTagEnemy)
    level_component = ecs_world.get_component(CLevel)

    for enemy_entity, (e_c_s, e_c_t, e_c_te) in enemy_components:
        ene_rect = CSurface.get_area_relative(e_c_s.area, e_c_t.pos)
        bl_rect = c_s.area.copy()
        bl_rect.topleft = c_t.pos
        if ene_rect.colliderect(bl_rect):
            ecs_world.delete_entity(enemy_entity)
            create_explosion(ecs_world, ene_rect, e_c_s.area.size, explosion_cfg)
            c_pbs.state = PlayerBulletState.NOT_FIRED
            self.enemy_destroyed = e_c_te.type
            
            
