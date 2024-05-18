import esper
import pygame

from src.ecs.components.c_enemy_movement import CEnemyMovement
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_movement(world:esper.World, delta_time:float, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    system_enemy_movement_component = world.get_component(CEnemyMovement)

    direction = 1
    c_t:CTransform
    c_v:CVelocity
    for _, (c_t, c_v, c_s, c_e) in components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 26 or cuad_rect.left + 10 > screen_rect.width - 26:
            direction *= -1
            break

    for _, (c_t, c_v, c_s, c_e) in components:
        c_v.vel.x *= direction

    for _, (c_em) in system_enemy_movement_component:
        c_em.direction = direction
        c_em.x_relative_position = c_v.vel.x * delta_time
        c_em.vel = c_v.vel.x
 