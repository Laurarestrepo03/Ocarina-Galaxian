import random

class CStarField:
    def __init__(self, window_width, window_height, star_surface, blink_rate_min, blink_rate_max, star_color):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.star_surface = star_surface
        self.star_rect = self.star_surface.get_rect()
        self.star_rect.x = random.randrange(0, self.window_width)
        self.star_rect.y = random.randrange(0, self.window_height)
        self.blink_rate_min = blink_rate_min
        self.blink_rate_max = blink_rate_max
        self.current_blink_time = random.uniform(blink_rate_min, blink_rate_max)
        self.star_visible = True
        self.star_color = ((star_color["r"], star_color["g"], star_color["b"]))