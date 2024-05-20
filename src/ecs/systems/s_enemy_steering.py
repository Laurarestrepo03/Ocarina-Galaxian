import esper
import pygame
from src.ecs.components.c_level import CLevel
from src.ecs.components.c_enemy_steering import CEnemySteering, EnemySteeringState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_steering(world:esper.World, player_entity:int, delta_time:float, screen:pygame.Surface):
    enemies_components = world.get_components(CTransform, CVelocity, CSurface, CEnemySteering, CTagEnemy)
    level_component = world.get_component(CLevel)
    player_pos = world.component_for_entity(player_entity, CTransform)
    enemy_grup_vel = 0
     
    #player_position = pygame.Vector2(player_pos[0], player_pos[1])
    
    for _, (c_t, c_v, c_s, c_st,_) in enemies_components:       
        for _, (c_el) in level_component:
            c_st.return_position.x += c_el.x_relative_position
            enemy_grup_vel = c_el.vel
        
        if c_st.state == EnemySteeringState.JUMPING:
            if c_st.jumping_counter < 20:
                c_v.vel.y = -20
                c_v.vel.x = (player_pos.pos.x - c_t.pos.x)  
                cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
                screen_rect = screen.get_rect()
                c_st.jumping_counter += 1
            else:
                c_st.jumping_counter = 5 
                c_st.state = EnemySteeringState.HUNTING
            
        elif c_st.state == EnemySteeringState.HUNTING:
            c_v.vel.y = 40
            c_v.vel.x = (player_pos.pos.x - c_t.pos.x)  
            cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
            screen_rect = screen.get_rect()
            if cuad_rect.bottom > screen_rect.height:
                c_t.pos.y = 0
                c_st.state = EnemySteeringState.RETURNING
                
        elif c_st.state == EnemySteeringState.RETURNING:
            c_v.vel = (c_st.return_position - c_t.pos).normalize() * 40
            if abs(c_st.return_position.x - c_t.pos.x) < 5 and  abs(c_st.return_position.y - c_t.pos.y) < 5:
                c_t.pos = c_st.return_position
                c_v.vel = pygame.Vector2(enemy_grup_vel, 0)

                world.remove_component(c_st.entity, CEnemySteering)

    

    