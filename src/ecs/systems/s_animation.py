import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world:esper.World, delta_time:float):
    components = world.get_components(CSurface, CAnimation)
    
    for _, (c_s, c_a) in components:
        c_a.curr_anim_time -= delta_time        # 1. disminuir el valor del curr_time de la animacion
        if c_a.curr_anim_time <= 0:             # 2. Cuando curr_time <= 0
            c_a.curr_anim_time = c_a.framerate  # RESTAURAR EL TIEMPO
            c_a.curr_frame += 1                 # CAMBIO DE FRAME
            
            if c_a.curr_frame > c_a.end:        
                c_a.curr_frame = c_a.start 
                print("Ya acabo el ciclo")       
            rect_surf = c_s.surf.get_rect()     # Calcular la nueva subarea del rectangulo de sprote
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame