import asyncio
import json
import pygame
import esper

from src.create.prefab_creator import create_enemy, create_level, create_square
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.create.prefab_creator import create_input_player, create_player, create_star
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_star_field import CStarField
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_bullet_limit import system_bullet_limit
from src.ecs.systems.s_bullet_rest_pos import system_bullet_rest_pos
from src.ecs.systems.s_bullet_spawn import system_bullet_spawn
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limit import system_player_limit
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_star_field import system_draw_stars, system_star_field

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
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

        # Original framerate = 0
        # Original bg_color (0, 200, 128)

    def _load_config_files(self):
        path = 'assets/cfg/'
        with open(path + "window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(path + "player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open(path + "bullet.json", encoding="utf-8") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open(path + "starfield.json", encoding="utf-8") as starfield_file:
            self.starfield_cfg = json.load(starfield_file)
        with open(path + "level_01.json", encoding="utf-8") as level_file:
            self.level_cfg = json.load(level_file)
        with open(path + "enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
            
            

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
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_tag = self.ecs_world.component_for_entity(self._player_entity, CTagPlayer)
        create_input_player(self.ecs_world)
        create_star(self.ecs_world, self.window_cfg, self.starfield_cfg)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
    
    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        #system_movement(self.ecs_world, self.delta_time)
        #system_screen_bounce(self.ecs_world, self.screen) # ver si en realidad se usa
        system_animation(self.ecs_world, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_player_limit(self.ecs_world, self.screen)
        system_bullet_spawn(self.ecs_world, self.bullet_cfg, self._player_c_t.pos)
        system_bullet_rest_pos(self.ecs_world)
        system_bullet_limit(self.ecs_world, self.screen)
        system_star_field(self.ecs_world, self.window_cfg, self.delta_time)
        system_enemy_movement(self.ecs_world, self.delta_time, self.screen)
        self.ecs_world._clear_dead_entities()
        
    def system_draw_stars(ecs_world: esper.World, screen):
        star_entities = ecs_world.get_component(CStarField)
        for entity, star_field in star_entities:
            c_transform = ecs_world.component_for_entity(entity, CTransform)
            screen.blit(star_field.star_surface, c_transform.pos)

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
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
        if c_input.name == "PLAYER_FIRE":
            bullet_components = self.ecs_world.get_components(CVelocity, CTagBullet)
            for _, (c_v, c_tb) in bullet_components:
                c_tb.fired = True
                vel = pygame.Vector2(0, -1)
                vel = vel.normalize() * self.bullet_cfg["velocity"]
                c_v.vel = vel
            
