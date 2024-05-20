import esper
import pygame
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_game_state import CGameState, GameState


def system_collision_enemy_player(world:esper.World, explosion_cfg:dict, game_manager_entity ):
                       
    player_components = world.get_components(CSurface, CTransform, CTagPlayer)
    enemies_components = world.get_components(CSurface, CTransform, CTagEnemy)
    game_state = world.component_for_entity(game_manager_entity,CGameState)

    for player_entity, (p_c_s, p_c_t, _) in player_components:
        pl_rect = CSurface.get_area_relative(p_c_s.area, p_c_t.pos)
        for enemy_entity, (e_c_s, e_c_t, e_te) in enemies_components:
            e_rect = e_c_s.area.copy()
            e_rect.topleft = e_c_t.pos
            if pl_rect.colliderect(e_rect) and p_c_s.visible:
                world.delete_entity(enemy_entity)
                p_c_s.visible= False
                game_state.state = GameState.DEAD
                game_state.number_lives -=1
                #world.delete_entity(player_entity)
                create_explosion(world, pl_rect, p_c_s.area.size, explosion_cfg)