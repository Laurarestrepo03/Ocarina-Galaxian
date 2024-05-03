import random
import esper
from src.ecs.components.c_star_field import CStarField
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_star_field(ecs_world:esper.World, window_cfg, delta_time):
    star_entities = ecs_world.get_component(CStarField)
    for entity, star_field in star_entities:
        c_transform = ecs_world.component_for_entity(entity, CTransform)
        c_velocity = ecs_world.component_for_entity(entity, CVelocity)
        c_transform.pos += c_velocity.vel * delta_time
        
        if c_transform.pos.y > window_cfg["size"]["h"]:
            c_transform.pos.y = 0
            c_transform.pos.x = random.randint(0, window_cfg["size"]["w"])
            
        star_field.current_blink_time -= delta_time
        if star_field.current_blink_time <= 0:
            star_field.star_visible = not star_field.star_visible
            
            if star_field.star_visible:
                star_field.star_surface.fill((window_cfg["bg_color"]["r"], window_cfg["bg_color"]["g"], window_cfg["bg_color"]["b"]))
            else:
                star_field.star_surface.fill((star_field.star_color))
                
            star_field.current_blink_time = random.uniform(star_field.blink_rate_min, star_field.blink_rate_max)