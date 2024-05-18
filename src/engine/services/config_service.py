import json

class ConfigsService:
    def __init__(self) -> None:
        self._prefix_path = "./assets/cfg/"
        self._configs = {}
            # Archivos personales de config precargados
        self.window = self.get("window.json")
        self.player = self.get("player.json")
        self.enemies = self.get("enemies.json")
            #... etcetera

    def get(self, filename:str):
        final_path = self._prefix_path + filename
        if final_path not in self._configs:
            with open(final_path, encoding="utf-8") as json_file:
                self._configs[final_path] = json.load(json_file)
        return self._configs[final_path]