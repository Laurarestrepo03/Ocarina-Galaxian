import esper
import json 
import os

from src.create.prefab_creator import create_text
from src.ecs.components.c_surface import CSurface

def system_update_high_score(world:esper.World, interface_cfg:dict, self):        

    if self.score > self.high_score:
        self.high_score = self.score
        world.delete_entity(self.high_score_entity)
        self.high_score_entity = create_text(world, interface_cfg["high_score_value"], str(self.high_score))
        update_high_score_value(self.high_score)
    
def update_high_score_value(value):
    file_path = 'assets/cfg/interface.json'
    with open(file_path, 'r') as archivo_json:
        datos = json.load(archivo_json)
        
    datos["high_score_value"]["text"] = value
    
    with open(file_path, 'w') as archivo_json:
        json.dump(datos, archivo_json, indent=4)