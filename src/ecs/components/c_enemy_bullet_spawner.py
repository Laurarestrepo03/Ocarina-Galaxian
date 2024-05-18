import random

class CEnemyBulletSpawner:
    def __init__(self, lvl_info:dict) -> None:
        self.timer = 0
        CEnemyBulletSpawner.change_max_time(lvl_info)

    @classmethod
    def change_max_time(cls, lvl_info):
        cls.max_time = random.uniform(lvl_info["min_bullet_interval"], lvl_info["max_bullet_interval"])