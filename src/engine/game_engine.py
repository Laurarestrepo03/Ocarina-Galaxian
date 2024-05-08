import asyncio
import json
import pygame
import esper

from src.create.prefab_creator import create_bullet, create_input_player, create_pause_text, create_player, create_star, create_text
from src.create.prefab_creator import create_level
from src.ecs.components.c_player_bullet_state import CPLayerBulletState, PlayerBulletState
from src.ecs.components.tags.c_tag_bullet import BulletType
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_draw_stars import system_draw_stars
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
from src.engine.service_locator import ServiceLocator

class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode((self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 
                                              pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.current_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()
        self.execute_game = True

        # Original framerate = 0
        # Original bg_color (0, 200, 128)

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
            
    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):       
        create_level(self.ecs_world, self.level_cfg, self.enemies_cfg)
        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_tag = self.ecs_world.component_for_entity(self._player_entity, CTagPlayer)
        create_bullet(self.ecs_world, self.player_bullet_cfg, pygame.Vector2(0,0), pygame.Vector2(0,0), BulletType.PLAYER)
        create_input_player(self.ecs_world)
        create_star(self.ecs_world, self.window_cfg, self.starfield_cfg)
        create_text(self.ecs_world, self.interface_cfg["1up_title"], self.interface_cfg["1up_title"]["text"])
        create_text(self.ecs_world, self.interface_cfg["1up_value"], self.interface_cfg["1up_value"]["text"])
        create_text(self.ecs_world, self.interface_cfg["high_score_title"], self.interface_cfg["high_score_title"]["text"])
        create_text(self.ecs_world, self.interface_cfg["high_score_value"], self.interface_cfg["high_score_value"]["text"])


    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        if self.execute_game:
            self.current_time += self.delta_time 
    
    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        #system_movement(self.ecs_world, self.delta_time)
        #system_screen_bounce(self.ecs_world, self.screen) # ver si en realidad se usa
        
        if self.execute_game:
            system_movement(self.ecs_world, self.delta_time)
            system_enemy_movement(self.ecs_world, self.delta_time, self.screen)
            system_star_field(self.ecs_world, self.window_cfg, self.delta_time)

            system_explosion_state(self.ecs_world)

            system_bullet_limit(self.ecs_world, self.screen)
            system_player_limit(self.ecs_world, self.screen)
    
            system_enemy_bullet_spawn(self.ecs_world, self.enemy_bullet_cfg, self.enemies_cfg, self.delta_time)

            system_collision_bullet_player(self.ecs_world, self.player_explosion_cfg)

            system_player_bullet_state(self.ecs_world, self.enemy_explosion_cfg)

            system_animation(self.ecs_world, self.delta_time)

        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen, self.delta_time)
        system_draw_stars(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def _do_action(self, c_input:CInputCommand):
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
        if c_input.name == "PAUSE":
            if c_input.phase == CommandPhase.START:
                if self.execute_game == True:
                    self.execute_game = False
                    font = ServiceLocator.fonts_service.get_font(self.interface_cfg["pause"]["font"] ,self.interface_cfg["pause"]["size"])
                    r = self.interface_cfg["pause"]["color"]["r"]
                    g = self.interface_cfg["pause"]["color"]["g"]
                    b = self.interface_cfg["pause"]["color"]["b"]
                    create_pause_text(self.ecs_world,
                                      self.interface_cfg["pause"]["text"], 
                                      font, 
                                      pygame.Vector2(self.window_cfg["size"]["w"]/2, 30 + self.window_cfg["size"]["h"]/2),
                                      pygame.Color(r, g, b))
                    ServiceLocator.sounds_service.play(self.interface_cfg["pause"]["sound"])
                else:
                    self.execute_game = True
                    system_pause(self.ecs_world)


            
