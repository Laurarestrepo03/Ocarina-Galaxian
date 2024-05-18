import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_game_state import CGameState, GameState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import BulletType, CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_collision_bullet_player(ecs_world:esper.World, explosion_cfg:dict, game_manager_entity):
    player_components = ecs_world.get_components(CSurface, CTransform, CTagPlayer)
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagBullet)
    game_state = ecs_world.component_for_entity(game_manager_entity,CGameState)
    if game_state.state == GameState.PLAY:
        for player_entity, (p_c_s, p_c_t, _) in player_components:
            pl_rect = CSurface.get_area_relative(p_c_s.area, p_c_t.pos)
            for bullet_entity, (b_c_s, b_c_t, b_tb) in bullet_components:
                bl_rect = b_c_s.area.copy()
                bl_rect.topleft = b_c_t.pos
                if pl_rect.colliderect(bl_rect) and b_tb.type == BulletType.ENEMY:
                    #TODO: quitar comentario cuando se implemente reinicio
                    p_c_s.visible= False
                    game_state.state = GameState.DEAD
                    game_state.number_lives -=1
                    ecs_world.delete_entity(bullet_entity)
                    create_explosion(ecs_world, pl_rect, p_c_s.area.size, explosion_cfg)

    
    for bullet_entity, (b_c_s, b_c_t, b_tb) in bullet_components:
        if (game_state.state == GameState.DEAD and b_tb.type == BulletType.PLAYER) or (game_state.state == GameState.GAME_OVER and b_tb.type == BulletType.PLAYER) :
            #TODO: quitar comentario cuando se implemente reinicio
            b_c_s.visible= False
        elif game_state.state == GameState.GAME_OVER and b_tb.type == BulletType.ENEMY:
            b_c_s.visible= False
        else:
            b_c_s.visible= True