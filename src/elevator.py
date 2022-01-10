DEBUG = False

class Elevator:
    def __init__(self, levels):
        self.cur_level = self.get_current_level_from_sensor() or 1
        self.cur_direction = 0
        self.top_floor = levels
        self.bottom_floor = 0

    def move(self):
        target_floor = self.cur_level + self.cur_direction

        if target_floor > self.top_floor or target_floor < self.bottom_floor:
            return

        self.cur_level = target_floor

        if DEBUG:
            if self.cur_direction == 1:
                print "Elevator is moving up"
            elif self.cur_direction == -1:
                print "Elevator is moving down"
            else:
                print "Elevator is idling at floor {}".format(self.cur_level)

    def set_idle(self):
        self.cur_direction = 0

    def is_idle(self):
        return self.cur_direction == 0
    
    def set_direction_up(self):
        self.cur_direction = 1

    def set_direction_down(self):
        self.cur_direction = -1

    def get_cur_level(self):
        return self.cur_level

    def get_current_level_from_sensor(self):
        '''
            Stubbed for a sensor to detect
            (to handle for when the system is turned off and on again)
        '''
        pass

    def is_going_up(self):
        return self.cur_direction == 1

    def is_going_down(self):
        return self.cur_direction == -1

    def tick(self):
        self.move()