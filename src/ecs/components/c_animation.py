from typing import List

class CAnimation:
    def __init__(self, animation:dict) -> None:
        self.number_frames = animation["number_frames"]
        self.name = animation["name"]
        self.start = animation["start"] 
        self.end = animation["end"]
        self.framerate = 1.0 / animation["framerate"]

        self.curr_anim = 0
        #self.curr_anim_time = self.animations_list[self.curr_anim].framerate
        self.curr_anim_time = 0
        self.curr_frame = self.start
                
def set_animation(c_a:CAnimation, num_amim:int):
    if c_a.curr_anim == num_amim:
        return
    c_a.curr_anim = num_amim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.start
    