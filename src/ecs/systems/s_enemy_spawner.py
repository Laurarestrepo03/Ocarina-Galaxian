import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner, Enemy
from src.create.prefab_creator import create_enemy_square

def system_enemy_spawner(world:esper.World, enemies:dict):
    components = world.get_component(CEnemySpawner)

    c_esp:CEnemySpawner
            
    for _, c_esp in components:
        enemy:Enemy
        for enemy in c_esp.enemies:
            create_enemy_square(world, enemy.position, enemies[enemy.enemy_type])    
    
