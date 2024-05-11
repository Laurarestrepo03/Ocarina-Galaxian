import esper
from src.ecs.components.tags.c_tag_pause import CTagPause

def system_pause(world : esper.World):
    component = world.get_component(CTagPause)

    for entity, (c_t) in component:
        world.delete_entity(entity)
