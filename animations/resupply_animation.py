from  .def_animation import Animation

class SlashAnimation(Animation):
    def __init__(self, x, y ,switch_speed=500):
        super().__init__(x,y,"img/anime/resupply")
       