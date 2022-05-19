class Animation:
    def __init__(self, name, start, frames, time):
        self.name = name
        self.start = start
        self.finish = frames + start
        self.time = time

        self.current_frame = start
        self.time_counter = 0

    def update(self, delta_time):
        self.time_counter += delta_time
        if self.time_counter >= self.time:
            self.time_counter = 0
            self.current_frame += 1
            if self.current_frame > self.finish:
                self.current_frame = self.start


def get_surface(surface_num):
    if surface_num < len(loaded_surfaces):
        return loaded_surfaces[surface_num]


loaded_surfaces = list()
animations = list()
