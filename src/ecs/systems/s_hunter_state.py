import esper
from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def system_enemies_state(world:esper.World):
    components = world.get_component(CAnimation)
    
    for _, (c_a) in components:
        set_animation(c_a, 1)
  