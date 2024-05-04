
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_pause import CTagPause

def system_rendering(world:esper.World, screen:pygame.Surface, delta_time: float):
    components = world.get_components(CTransform, CSurface)
    
    c_t:CTransform
    c_s:CSurface
    for _, (c_t, c_s) in components:
        if world.has_component(_, CTagPause):
            c_p= world.component_for_entity(_,  CTagPause)
            c_p.timer += delta_time
            if 0.5 <= c_p.timer <= 1.0:
                pass
            elif 1.0 <= c_p.timer <= 1.5:
                c_p.timer =0
            else:
                screen.blit(c_s.surf, c_t.pos, area=c_s.area)
                
        else:
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)