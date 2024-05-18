import esper
import pygame
from src.create.prefab_creator import create_text
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_score import CTagScore
from src.engine.service_locator import ServiceLocator

def system_update_score(world:esper.World, interface_info:dict, enemies_info):        

    level_component =  world.get_component(CLevel)
    score_components =  world.get_components(CSurface, CTagScore)
    
    font = ServiceLocator.fonts_service.get_font(interface_info["score_value"]["font"], interface_info["score_value"]["size"])

    for _, (c_l) in level_component:
        if c_l.enemy_destroyed is not None:
            for score, (c_s, _) in score_components:
                points = enemies_info[c_l.enemy_destroyed]["points"]
                c_l.score += points
                color = pygame.Color(interface_info["score_value"]["color"]["r"], interface_info["score_value"]["color"]["g"], interface_info["score_value"]["color"]["b"])
                c_s.surf = font.render(str(c_l.score), False, color)
                c_s.area = c_s.surf.get_rect()
                
                c_l.enemy_destroyed = None
            
    
        
    
    
    