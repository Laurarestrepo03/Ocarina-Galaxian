import esper
from src.create.prefab_creator import create_level
from src.ecs.components.tags.c_tag_ready import CTagReady

def system_ready(world : esper.World, current_time, level_cfg, enemies_cfg):
    component = world.get_component(CTagReady)

    for entity, (c_t) in component:
        if current_time >= 3  and c_t.init: 
            create_level(world, level_cfg, enemies_cfg)
            world.delete_entity(entity)
            c_t.init = False