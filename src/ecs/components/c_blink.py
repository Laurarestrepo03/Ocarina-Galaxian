import random


class CBlink:
    def __init__(self, blink_rate_min, blink_rate_max) -> None:
        self.is_blinking = False
        self.blink_rate_min = blink_rate_min
        self.blink_rate_max = blink_rate_max
        self.current_blink_time = random.uniform(self.blink_rate_min, self.blink_rate_max)