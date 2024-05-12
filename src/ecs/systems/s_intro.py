
import random
import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_intro(ecs_world: esper.World, current_time):
    enemy_entities = ecs_world.get_components(CTagEnemy, CSurface)
    for entity, (star_field, surface) in enemy_entities:
        if current_time <= 3:
            surface.surf.set_alpha(0)
        else:
            surface.surf.set_alpha(255)