import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(ecs_world:esper.World, delta_time:float):
    components = ecs_world.get_components(CSurface, CAnimation)

    for _, (c_s, c_a) in components:
        # Disminuir el valor de curr_time de la animacion
        c_a.curr_anim_time -= delta_time
        # Cuando curr_time <= 0, hacemos cambio de frame
        if c_a.curr_anim_time <= 0:
            # RESTAURAR TIEMPO
            c_a.curr_anim_time = c_a.animations_list[c_a.curr_anim].framerate
            # CAMBIO DE FRAME
            c_a.curr_frame += 1
            # Limitar el frame con sus propiedades de start y end
            if c_a.curr_frame > c_a.animations_list[c_a.curr_anim].end:
                c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
            # Calcular la nueva subarea del rectangulo de sprite
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.num_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame
