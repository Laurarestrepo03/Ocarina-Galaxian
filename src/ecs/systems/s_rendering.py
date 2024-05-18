
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    
    c_t:CTransform
    c_s:CSurface
    for _, (c_t, c_s) in components:
        alpha = c_s.surf.get_alpha()
        if not c_s.visible or alpha == 0:
            continue

        screen.blit(c_s.surf, c_t.pos, area=c_s.area)