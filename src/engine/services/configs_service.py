import json
import pathlib
import os

class ConfigsService:
    def __init__(self) -> None:
        self._prefix_path = "./assets/cfg/"
        self._configs = {}
        self.enemies = self.get("enemies.json")
        self.enemy_bullet = self.get("enemy_bullet.json")
        self.enemy_explosion = self.get("enemy_explosion.json")
        self.interface = self.get("interface.json")
        self.level = self.get("level_01.json")
        self.player_bullet = self.get("player_bullet.json")
        self.player_explosion = self.get("player_explosion.json")
        self.player = self.get("player.json")
        self.starfield = self.get("starfield.json")
        self.window = self.get("window.json")

        # # Precargar y asignar atributos a la clase con cada config
        # for (_, _, files) in os.walk(self._prefix_path, topdown=True):
        #     for file_path in files:
        #         file_no_extension = pathlib.Path(file_path).stem # rchivo sin extension
        #         json_obj = self.get(file_path)
        #         setattr(self, file_no_extension, json_obj) # Igual a self.file = self.get(path)

    def get(self, filename:str):
        final_path = self._prefix_path + filename
        if final_path not in self._configs:
            with open(final_path, encoding="utf-8") as json_file:
                self._configs[final_path] = json.load(json_file)
        return self._configs[final_path]