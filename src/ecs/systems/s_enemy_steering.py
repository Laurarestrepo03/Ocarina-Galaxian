import esper
import pygame
from src.ecs.components.c_enemy_movement import CEnemyMovement
from src.ecs.components.c_steering import CSteering, SteeringState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_steering(world:esper.World, player_entity:int, delta_time:float, screen:pygame.Surface):
    enemies_components = world.get_components(CTransform, CVelocity, CSurface, CSteering, CTagEnemy)
    player_pos = world.component_for_entity(player_entity, CTransform)
    
    #player_position = pygame.Vector2(player_pos[0], player_pos[1])
    
    for _, (c_t, c_v, c_s, c_st,_) in enemies_components:       
        if c_st.state == SteeringState.HUNTING:
            c_v.vel.y = 40
            c_v.vel.x = (player_pos.pos.x - c_t.pos.x)  
            cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
            screen_rect = screen.get_rect()
            if cuad_rect.bottom > screen_rect.height:
                c_t.pos.y = 0
                c_st.state = SteeringState.RETURNING
                
        elif c_st.state == SteeringState.RETURNING:
            c_v.vel = (c_st.return_position - c_t.pos)
            #print("Velocidad:" + str(c_v.vel))
            if abs(c_st.return_position.x - c_t.pos.x) < 3 and  abs(c_st.return_position.y - c_t.pos.y) < 3:
                c_t.pos = c_st.return_position
                c_v.vel = pygame.Vector2(0, 0)
                               
                #world.delete_entity(c_st.entity)
                world.remove_component(c_st.entity, CSteering)
                c_st.state = SteeringState.GROUP
        
        elif c_st.state == SteeringState.GROUP:
            world.remove_component(c_st.entity, CSteering)
    
        enemy_movement_component = world.get_component(CEnemyMovement)
        for _, (c_em) in enemy_movement_component:
            c_st.return_position.x += c_em.x_relative_position
    