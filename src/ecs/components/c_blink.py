import random


class CBlink:
    def __init__(self, starfield_cfg:dict) -> None:
        self.is_blinking = False
        self.blink_rate_min = starfield_cfg["blink_rate"]["min"]
        self.blink_rate_max = starfield_cfg["blink_rate"]["max"]
        self.current_blink_time = random.uniform(self.blink_rate_min, self.blink_rate_max)