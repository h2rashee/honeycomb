from elevator import Elevator

DEBUG = False

class ElevatorSystem:
    def __init__(self, levels, ts):
        '''
            This project is intended for a one elevator system so we're
            just initializing one
        '''
        self.elevator = Elevator(levels)
        self.top_floor = levels
        self.ts = ts

        # Hash table signalling whether there is a trip pick-up/drop-off
        # at the relevant floor
        self.trips_up = [0 for x in range(levels + 1)]
        self.trips_down = [0 for x in range(levels + 1)]

        # Parallel hashtable tracking the request at the relevant floor
        # We do this to track and execute drop-offs for a respective pick-up.
        self.trips_up_requests = [[] for x in range(levels + 1)]
        self.trips_down_requests = [[] for x in range(levels + 1)]

    def clock_tick(self):
        if DEBUG:
            print self.trips_up
            print self.trips_up_requests
            print self.trips_down
            print self.trips_down_requests
        self.process_requests_for_cur_floor()
        self.direct_the_elevator()
        self.elevator.tick()
        self.ts = self.ts + 1

    def process_requests_from_queue(self, reqs):
        for req in reqs:
            floor = req.get_pickup_floor()
            if req.is_going_up():
                self.trips_up[floor] = 1
                self.trips_up_requests[floor].append(req)
            else:
                self.trips_down[floor] = 1
                self.trips_down_requests[floor].append(req)

    def process_requests_for_cur_floor(self):
        cur_level = self.elevator.get_cur_level()

        # Pickup people going up if we're already going up or doing nothing
        if self.does_current_floor_have_valid_pickup() and self.trips_up[cur_level] == 1:
            # and drop-off while we're at it
            self.trips_up[cur_level] = 0
            
            if self.trips_down[cur_level] == 1 and len(self.trips_down_requests[cur_level]) == 0:
                self.trips_down[cur_level] = 0
            
            # we also need to mark the floors to drop-off the people we just picked-up
            for req in self.trips_up_requests[cur_level]:
                assert req.get_pickup_floor() == cur_level
                self.trips_up[req.get_dest_floor()] = 1
                if DEBUG:
                    print "Picking up someone on floor {} heading up".format(cur_level)
            self.trips_up_requests[cur_level] = []

        # Pickup people going down in any other case
        elif self.does_current_floor_have_valid_pickup() and self.trips_down[cur_level] == 1:
            self.trips_down[cur_level] = 0

            if self.trips_up[cur_level] == 1 and len(self.trips_up_requests[cur_level]) == 0:
                self.trips_up[cur_level] = 0

            for req in self.trips_down_requests[cur_level]:
                assert req.get_pickup_floor() == cur_level
                self.trips_down[req.get_dest_floor()] = 1
                if DEBUG:
                    print "Picking up someone on floor {} heading down".format(cur_level)
            self.trips_down_requests[cur_level] = []

        else:
            if DEBUG:
                print "Passing floor {}".format(cur_level)

    def direct_the_elevator(self):
        if not self.has_active_trip():
            self.elevator.set_idle()
            return
        
        # Set the elevator direction if we were idling but now there is an active request
        if self.elevator.is_idle() and self.has_trip_up_from_floor():
            self.elevator.set_direction_up()
        elif self.elevator.is_idle() and self.has_trip_down_from_floor():
            self.elevator.set_direction_down()
        
        # Change the elevator direction if there are no trips in the current direction
        elif self.elevator.is_going_up() and not self.has_trip_up_from_floor():
            self.elevator.set_direction_down()
        elif self.elevator.is_going_down() and not self.has_trip_down_from_floor():
            self.elevator.set_direction_up()

        else:
            if DEBUG:
                print "Has trip in direction so do nothing"

    def has_trip_up(self):
        return 1 in self.trips_up
    
    def has_trip_up_from_floor(self):
        if self.elevator.get_cur_level() == self.top_floor:
            return False
        # Are there any trips on the floors above us?
        return 1 in self.trips_up[self.elevator.get_cur_level()+1:] or 1 in self.trips_down[self.elevator.get_cur_level()+1:]

    def has_trip_down_from_floor(self):
        if self.elevator.get_cur_level() == 0:
            return False
        # Are there any trips on the floors below us?
        return 1 in self.trips_up[:self.elevator.get_cur_level()] or 1 in self.trips_down[:self.elevator.get_cur_level()]

    def has_active_trip(self):
        return 1 in self.trips_up or 1 in self.trips_down

    def is_elevator_at_top_floor(self):
        return self.elevator.get_cur_level() == self.top_floor

    def is_elevator_at_bottom_floor(self):
        return self.elevator.get_cur_level() == 0

    def does_current_floor_have_valid_pickup(self):
        cur_level = self.elevator.get_cur_level()
        
        if self.trips_up[cur_level] == 0 and self.trips_down[cur_level] == 0:
            return False

        if self.elevator.is_idle():
            return True

        if self.is_elevator_at_bottom_floor() or self.is_elevator_at_top_floor():
            return True

        if self.trips_up[cur_level] == 1 and self.elevator.is_going_down() and self.has_trip_down_from_floor():
            return False
        
        if self.trips_down[cur_level] == 1 and self.elevator.is_going_up() and self.has_trip_up_from_floor():
            return False

        return True