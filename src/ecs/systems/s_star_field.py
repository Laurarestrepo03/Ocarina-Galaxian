import random
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_star_field(ecs_world:esper.World, window_cfg, delta_time):
    star_entities = ecs_world.get_components(CTransform, CVelocity)
    for entity, (c_transform, c_velocity) in star_entities:
        c_transform = ecs_world.component_for_entity(entity, CTransform)
        c_transform.pos += c_velocity.vel * delta_time
        
        if c_transform.pos.y > window_cfg["size"]["h"]:
            c_transform.pos.y = 0
            c_transform.pos.x = random.randint(0, window_cfg["size"]["w"])