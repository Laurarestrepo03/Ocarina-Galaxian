import esper
from src.ecs.components.c_star_field import CStarField
from src.ecs.components.c_transform import CTransform

def system_draw_stars(ecs_world: esper.World, screen):
    star_entities = ecs_world.get_component(CStarField)
    for entity, star_field in star_entities:
        c_transform = ecs_world.component_for_entity(entity, CTransform)
        screen.blit(star_field.star_surface, c_transform.pos)