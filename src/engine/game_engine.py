import asyncio
import json
import pygame
import esper

from src.create.prefab_creator import create_bullet, create_enemy_bullet_spawner, create_flag, create_input_player, create_life, create_player, create_star, create_text
from src.create.prefab_creator import create_level
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_game_state import GameState, CGameState
from src.ecs.components.c_player_bullet_state import CPLayerBulletState, PlayerBulletState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import BulletType
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_level import CTagLevel
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.ecs.components.tags.c_tag_ready import CTagReady
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
from src.ecs.systems.s_game_manager import system_game_manager
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

        self.high_score = int(self.interface_cfg["high_score_value"]["text"])
        self.score = 0
        self.enemy_destroyed = None
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
        create_enemy_bullet_spawner(self.ecs_world, self.level_cfg)
        self.game_manager = self.ecs_world.create_entity()
        self.ecs_world.add_component(self.game_manager, CGameState())
        self.game_state = self.ecs_world.component_for_entity(self.game_manager, CGameState)

        self.high_score = int(self.interface_cfg["high_score_value"]["text"])
        self.ready_entity = create_text(self.ecs_world, 
                    self.interface_cfg["ready"])
        self.ecs_world.add_component(self.ready_entity, CTagReady())      
        ServiceLocator.sounds_service.play(self.interface_cfg["ready"]["sound"])

        create_star(self.ecs_world, self.window_cfg, self.starfield_cfg)
        #create_level(self.ecs_world, self.level_cfg, self.enemies_cfg)
        
        self._player_entity = create_player(self.ecs_world, self.player_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_tag = self.ecs_world.component_for_entity(self._player_entity, CTagPlayer)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        create_bullet(self.ecs_world, self.player_bullet_cfg, pygame.Vector2(0,0), pygame.Vector2(0,0), BulletType.PLAYER)
        create_input_player(self.ecs_world)
        create_star(self.ecs_world, self.window_cfg, self.starfield_cfg)
        create_text(self.ecs_world, self.interface_cfg["1up_title"])
        self.score_entity = create_text(self.ecs_world, self.interface_cfg["score_value"])
        create_text(self.ecs_world, self.interface_cfg["high_score_title"])
        self.high_score_entity = create_text(self.ecs_world, self.interface_cfg["high_score_value"], str(self.high_score))
        create_life(self.ecs_world, self.interface_cfg)
        create_flag(self.ecs_world, self.interface_cfg)
        self.level_entity = create_text(self.ecs_world, self.interface_cfg["level_text"])
        self.ecs_world.add_component(self.level_entity, CTagLevel())


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
        #system_screen_bounce(self.ecs_world, self.screen) # ver si en realidad se usa
        system_star_field(self.ecs_world, self.window_cfg, self.delta_time, self.execute_game)
        system_blink(self.ecs_world, self.delta_time)
        system_game_manager(self.ecs_world, self.delta_time, self.level_cfg, self.enemies_cfg, self.game_manager, self.interface_cfg, self._player_entity, self.player_cfg)
        
        if self.game_state.state != GameState.PAUSED:

            system_movement(self.ecs_world, self.delta_time)
            system_enemy_movement(self.ecs_world, self.delta_time, self.screen)
            system_explosion_state(self.ecs_world)
            system_bullet_limit(self.ecs_world, self.screen)
            system_player_limit(self.ecs_world, self.screen)
            system_enemy_bullet_spawn(self.ecs_world, self.enemy_bullet_cfg, self.enemies_cfg, self.level_cfg, self.delta_time)
            system_collision_bullet_player(self.ecs_world, self.player_explosion_cfg, self.game_manager)

            system_player_bullet_state(self.ecs_world, self.enemy_explosion_cfg, self, self.game_manager)

            system_animation(self.ecs_world, self.delta_time)
            
            system_update_score(self.ecs_world,self.interface_cfg,self.enemies_cfg, self)
            system_update_high_score(self.ecs_world,self.interface_cfg, self)
            
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
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
        if c_input.name == "PLAYER_FIRE" and c_input.phase == CommandPhase.START and self.game_state.state == GameState.PLAY:
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
                if self.game_state.state == GameState.PLAY:
                    self.game_state.state = GameState.PAUSED
                    pause_text_entity = create_text(self.ecs_world, self.interface_cfg["pause"])
                    self.ecs_world.add_component(pause_text_entity, CBlink(0.5, 0.5))
                    self.ecs_world.add_component(pause_text_entity, CTagPause())
                    ServiceLocator.sounds_service.play(self.interface_cfg["pause"]["sound"])
                else:
                    if self.game_state.state == GameState.PAUSED:
                        self.game_state.state = GameState.PLAY
                        system_pause(self.ecs_world)
        if c_input.name == "PLAYER_FIRE" and c_input.phase == CommandPhase.START and self.game_state.state == GameState.GAME_OVER:
            enemyes = self.ecs_world.get_components(CTagEnemy)
            #eliminar los enemigos
            for ent, (c_t) in enemyes:
                self.ecs_world.delete_entity(ent)
            self.high_score = int(self.interface_cfg["high_score_value"]["text"])
            component = self.ecs_world.get_component(CTagReady)
            #eliminar el game over text
            for entity, (c_t) in component:
                self.ecs_world.delete_entity(entity)
            
            #reiniciar las variables del juego
            self.score = 0
            self.game_state.current_time = 0
            self.game_state.current_enemyes = 0
            self.game_state.time_dead = 0
            self.game_state.current_level = 1
            self.game_state.number_lives = 4
            self.game_state.game__help_text_created= False
            self.game_state.game_over_text_created = False
            self.game_state.time_game_over = 0
            #Crear nuevamente el texto ready y el sonido
            self.ready_entity = create_text(self.ecs_world, 
                    self.interface_cfg["ready"])
            self.ecs_world.add_component(self.ready_entity, CTagReady())
            ServiceLocator.sounds_service.play(self.interface_cfg["ready"]["sound"])
            #Cambiar el estado a ready
            self.game_state.state = GameState.READY
            #Ajustar la posición del jugador y hacerlo visible nuevamente
            self._player_c_t.pos = pygame.Vector2(self.player_cfg["spawn_point"]["x"] - (self._player_c_s.area.size[0]/2),
                        self.player_cfg["spawn_point"]["y"] - (self._player_c_s.area.size[1]/2))
            self._player_c_s.visible = True
            #crear las vidas nuevamente
            create_life(self.ecs_world, self.interface_cfg)
            #reiniciar el texto de nivel
            level_components = self.ecs_world.get_components(CSurface, CTagLevel) 
            for entity, (c_s, c_lev) in level_components:
                font = ServiceLocator.fonts_service.get_font(self.interface_cfg["level_text"]["font"], self.interface_cfg["level_text"]["size"])
                text_surface = font.render("01", True, pygame.Color(self.interface_cfg["level_text"]["color"]["r"], 
                                                                    self.interface_cfg["level_text"]["color"]["g"], 
                                                                    self.interface_cfg["level_text"]["color"]["b"]))
                c_s.surf = text_surface
                c_s.area = c_s.surf.get_rect()
            #reiniciar el texto de score
            surface_component = self.ecs_world.component_for_entity(self.score_entity, CSurface)
            font = ServiceLocator.fonts_service.get_font(self.interface_cfg["score_value"]["font"], self.interface_cfg["score_value"]["size"])
            surface = font.render("00", True, pygame.Color(self.interface_cfg["score_value"]["color"]["r"], 
                                                                self.interface_cfg["score_value"]["color"]["g"], 
                                                                self.interface_cfg["score_value"]["color"]["b"]))
            surface_component.surf = surface
            surface_component.area = surface_component.surf.get_rect()


      

            


            
