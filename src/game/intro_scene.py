import json
import pygame

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
import src.engine.game_engine
from src.create.prefab_creator import create_bullet, create_input_player, create_pause_text, create_player, create_star, create_text, create_text
from src.create.prefab_creator import create_level
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_player_bullet_state import CPLayerBulletState, PlayerBulletState
from src.ecs.components.tags.c_tag_bullet import BulletType
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_enemy_bullet_spawn import system_enemy_bullet_spawn
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.create.prefab_creator import create_input_player, create_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_bullet_limit import system_bullet_limit
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_pause import system_pause
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_bullet_state import system_player_bullet_state
from src.ecs.systems.s_player_limit import system_player_limit
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_star_field import system_star_field
from src.ecs.systems.s_update_high_score import system_update_high_score
from src.ecs.systems.s_update_score import system_update_score
from src.engine.service_locator import ServiceLocator
from src.engine.scenes.scene import Scene

class IntroScene(Scene):
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self._load_config_files()
        
        self.high_score = 0
        self.score = 0

    
    def _load_config_files(self):
        path = 'assets/cfg/'
        with open(path + "window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(path + "player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open(path + "player_bullet.json", encoding="utf-8") as player_bullet_file:
            self.player_bullet_cfg = json.load(player_bullet_file)
        with open(path + "enemy_bullet.json", encoding="utf-8") as enemy_bullet_file:
            self.enemy_bullet_cfg = json.load(enemy_bullet_file)
        with open(path + "starfield.json", encoding="utf-8") as starfield_file:
            self.starfield_cfg = json.load(starfield_file)
        with open(path + "level_01.json", encoding="utf-8") as level_file:
            self.level_cfg = json.load(level_file)
        with open(path + "enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open(path + "enemy_explosion.json", encoding="utf-8") as enemy_explosion_file:
            self.enemy_explosion_cfg = json.load(enemy_explosion_file)
        with open(path + "player_explosion.json", encoding="utf-8") as player_explosion_file:
            self.player_explosion_cfg = json.load(player_explosion_file)
        with open(path + "interface.json", encoding="utf-8") as interface_file:
            self.interface_cfg = json.load(interface_file)

    def do_create(self):
        self.high_score = int(self.interface_cfg["high_score_value"]["text"])
        self.ready_entity = create_text(self.ecs_world, 
                    self.interface_cfg["ready"])
                    
        ServiceLocator.sounds_service.play(self.interface_cfg["ready"]["sound"])

        create_star(self.ecs_world, self.window_cfg, self.starfield_cfg)
        
        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_tag = self.ecs_world.component_for_entity(self._player_entity, CTagPlayer)
        self._player_trans= self.ecs_world.component_for_entity(self._player_entity, CTransform)
        #create_bullet(self.ecs_world, self.player_bullet_cfg, pygame.Vector2(0,0), pygame.Vector2(0,0), BulletType.PLAYER)
        create_text(self.ecs_world, self.interface_cfg["1up_title"])
        self.score_entity = create_text(self.ecs_world, self.interface_cfg["score_value"])
        create_text(self.ecs_world, self.interface_cfg["high_score_title"])
        self.high_score_entity = create_text(self.ecs_world, self.interface_cfg["high_score_value"], str(self.high_score))
        self.execute_game = True
        create_input_player(self.ecs_world)
        

    
    def do_update(self, delta_time: float, screen):

        system_star_field(self.ecs_world, self.window_cfg, delta_time)
        system_blink(self.ecs_world, delta_time)
        system_movement(self.ecs_world, delta_time)
        system_player_limit(self.ecs_world, screen)
        system_animation(self.ecs_world, delta_time)
            
        self.ecs_world._clear_dead_entities()

    def do_clean(self):
        self._paused = False

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_tag.keys_left += 1
                if self._player_tag.keys_left == 1:
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_tag.keys_left -= 1
                if self._player_tag.keys_left == 0:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_tag.keys_right += 1
                if self._player_tag.keys_right == 1:
                    self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_tag.keys_right -= 1
                if self._player_tag.keys_right == 0:
                    self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_FIRE" and c_input.phase == CommandPhase.START and self.execute_game:
            bullet_components = self.ecs_world.get_components(CVelocity, CPLayerBulletState)
            for _, (c_v, c_pbs) in bullet_components:   
                if not c_pbs.state == PlayerBulletState.FIRED:
                    ServiceLocator.sounds_service.play(self.player_bullet_cfg["sound"])
                c_pbs.state = PlayerBulletState.FIRED
                vel = pygame.Vector2(0, -1)
                vel = vel.normalize() * self.player_bullet_cfg["velocity"]
                c_v.vel = vel
    
    def get_player_pos(self):
        return self._player_trans.pos

