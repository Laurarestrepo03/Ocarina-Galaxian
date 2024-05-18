import esper
import pygame
import json 
import os

from src.create.prefab_creator import create_text
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_high_score import CTagHighScore
from src.engine.service_locator import ServiceLocator

def system_update_high_score(world:esper.World, interface_info:dict):        
       
    level_component =  world.get_component(CLevel)
    high_score_components =  world.get_components(CSurface, CTagHighScore)
    
    font = ServiceLocator.fonts_service.get_font(interface_info["high_score_value"]["font"], interface_info["high_score_value"]["size"])

    for _, (c_l) in level_component:
        if c_l.score > int(c_l.high_score):
            c_l.high_score = c_l.score
            for score, (c_s, _) in high_score_components:
                color = pygame.Color(interface_info["high_score_value"]["color"]["r"], interface_info["high_score_value"]["color"]["g"], interface_info["high_score_value"]["color"]["b"])
                c_s.surf = font.render(str(c_l.high_score), False, color)
                c_s.area = c_s.surf.get_rect()
        
        
def update_high_score_value(value):
    file_path = 'assets/cfg/interface.json'
    with open(file_path, 'r') as archivo_json:
        datos = json.load(archivo_json)
        
    datos["high_score_value"]["text"] = value
    
    with open(file_path, 'w') as archivo_json:
        json.dump(datos, archivo_json, indent=4)
        
        
