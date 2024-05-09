import esper
from src.create.prefab_creator import create_text
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_surface import CSurface

def system_update_score(world:esper.World, interface_cfg:dict, enemies_info, self):        

    if self.enemy_destroyed is not None:
        points = enemies_info[self.enemy_destroyed]["points"]
        world.delete_entity(self.score_entity)
        self.score += points
        self.score_entity = create_text(world, interface_cfg["score_value"], str(self.score))
        self.enemy_destroyed = None
            
    
        
    
    
    