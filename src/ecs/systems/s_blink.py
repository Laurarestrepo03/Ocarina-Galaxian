import random
import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface


def system_blink(ecs_world: esper.World, delta_time: float):
    star_entities = ecs_world.get_components(CBlink, CSurface)
    for entity, (star_field, surface) in star_entities:
        star_field.current_blink_time -= delta_time
        if star_field.current_blink_time <= 0:
            star_field.is_blinking = not star_field.is_blinking
            
            surface.visible = star_field.is_blinking
                
            star_field.current_blink_time = random.uniform(star_field.blink_rate_min, star_field.blink_rate_max)