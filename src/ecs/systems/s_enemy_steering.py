import esper
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_steering(world:esper.World, player_entity:int, delta_time:float):
    enemies_components = world.get_components(CTransform, CVelocity, CSteering, CTagEnemy)
    player_pos = world.component_for_entity(player_entity, CTransform)
    #player_position = pygame.Vector2(player_pos[0], player_pos[1])
    
    for _, (c_t,c_v, c_s, _) in enemies_components:       
        c_v.vel = (player_pos.pos - c_t.pos).normalize() * 75