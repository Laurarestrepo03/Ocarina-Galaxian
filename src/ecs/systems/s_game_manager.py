import esper
import pygame
from src.create.prefab_creator import create_level, create_player, create_text
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_level import CTagLevel
from src.ecs.components.tags.c_tag_life import CTagLife
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_ready import CTagReady
from src.ecs.components.c_game_state import CGameState, GameState
from src.engine.service_locator import ServiceLocator

def system_game_manager(world : esper.World, delta_time: float, level_cfg, enemies_cfg, game_manager_entity, interface_cfg, player_entity, player_info):
    manager_component = world.component_for_entity(game_manager_entity, CGameState)
    component = world.get_component(CTagReady)
    player_surface = world.component_for_entity(player_entity, CSurface)
    player_pos = world.component_for_entity(player_entity, CTransform)
    life_component = world.get_component(CTagLife)
    level_components = world.get_components(CSurface, CTagLevel)

        
    if manager_component.state != GameState.PAUSED:
            manager_component.current_time += delta_time
            
    if manager_component.current_time >= 3: 
        if  manager_component.state == GameState.READY:
            for entity, (c_t) in component:
                world.delete_entity(entity)
            enemies = create_level(world, level_cfg, enemies_cfg, interface_cfg)
            manager_component.state = GameState.PLAY
            manager_component.current_enemyes = enemies

        elif manager_component.current_enemyes == 0 and manager_component.state == GameState.PLAY:
            
            win =create_text(world, 
                        interface_cfg["win"])
            ready_win = create_text(world, 
                        interface_cfg["ready_win"])
            world.add_component(win, CTagReady())
            world.add_component(ready_win, CTagReady())
            manager_component.state = GameState.WIN
            manager_component.current_time = 0

        elif manager_component.state == GameState.WIN:
            manager_component.current_level += 1
            print(manager_component.current_level)
            for entity, (c_t) in component:
                world.delete_entity(entity)
            for entity, (c_s, c_lev) in level_components:
                font = ServiceLocator.fonts_service.get_font(interface_cfg["level_text"]["font"], interface_cfg["level_text"]["size"])
                text_surface = font.render(str("0")+str(manager_component.current_level), True, pygame.Color(interface_cfg["level_text"]["color"]["r"], 
                                                                                                            interface_cfg["level_text"]["color"]["g"], 
                                                                                                            interface_cfg["level_text"]["color"]["b"]))
                c_s.surf = text_surface
                c_s.area = c_s.surf.get_rect()
                
            enemies = create_level(world, level_cfg, enemies_cfg)
            manager_component.state = GameState.PLAY
            manager_component.current_enemyes = enemies
        
        elif manager_component.state == GameState.DEAD:
            manager_component.time_dead += delta_time

            if  manager_component.time_dead >= 3:
                if manager_component.number_lives == 0 and not manager_component.game_over_text_created:
                    manager_component.state = GameState.GAME_OVER
                    game_over = create_text(world, 
                            interface_cfg["game_over"])
                    world.add_component(game_over, CTagReady())
                    ServiceLocator.sounds_service.play(interface_cfg["game_over"]["sound"])
                    manager_component.game_over_text_created = True
                else:
                    size = player_surface.area.size
                    player_pos.pos = pygame.Vector2(player_info["spawn_point"]["x"] - (size[0]/2),
                            player_info["spawn_point"]["y"] - (size[1]/2))
                    player_surface.visible = True
                    manager_component.state = GameState.PLAY
                    manager_component.time_dead = 0
                    for entity, (c_l) in life_component:
                        if c_l.number == manager_component.number_lives:
                            world.delete_entity(entity)
        
        elif manager_component.state == GameState.GAME_OVER:
            manager_component.time_game_over += delta_time
            if manager_component.time_game_over >= 1 and not manager_component.game__help_text_created :
                game_over_help = create_text(world, 
                            interface_cfg["game_over_help"])
                world.add_component(game_over_help, CTagReady())
                world.add_component(game_over_help, CBlink(0.7, 0.7))
                manager_component.game__help_text_created = True


        
        



             
             
            
        

            