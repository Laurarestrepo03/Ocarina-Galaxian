import esper
from src.create.prefab_creator import create_level, create_text
from src.ecs.components.tags.c_tag_ready import CTagReady
from src.ecs.components.c_game_state import CGameState, GameState

def system_game_manager(world : esper.World, delta_time: float, level_cfg, enemies_cfg, game_manager_entity, interface_cfg):
    manager_component = world.component_for_entity(game_manager_entity, CGameState)
    component = world.get_component(CTagReady)


        
    if manager_component.state != GameState.PAUSED:
            manager_component.current_time += delta_time
            
    if manager_component.current_time >= 3: 
        if  manager_component.state == GameState.READY:
            for entity, (c_t) in component:
                world.delete_entity(entity)
            enemies = create_level(world, level_cfg, enemies_cfg)
            manager_component.state = GameState.PLAY
            manager_component.current_enemyes = enemies
            print(enemies)

        elif manager_component.current_enemyes == 0 and manager_component.state == GameState.PLAY:
            
            win =create_text(world, 
                        interface_cfg["win"])
            ready_win = create_text(world, 
                        interface_cfg["ready_win"])
            world.add_component(win, CTagReady())
            world.add_component(ready_win, CTagReady())
            manager_component.state = GameState.WIN
            manager_component.current_time = 0
            print("win ", manager_component.current_time)

        elif manager_component.state == GameState.WIN:
            print(manager_component.current_time)
            for entity, (c_t) in component:
                world.delete_entity(entity)
            enemies = create_level(world, level_cfg, enemies_cfg)
            manager_component.state = GameState.PLAY
            manager_component.current_enemyes = enemies
            print(enemies)


             
             
            
        

            