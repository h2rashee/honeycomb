class Request:
    def __init__(self, floor, dest_floor, ts):
        self.ts = ts
        self.pickup_floor = floor
        self.dest_floor = dest_floor

    def __repr__(self):
        return "{}->{}".format(self.pickup_floor, self.dest_floor)

    def get_time(self):
        return self.ts

    def get_pickup_floor(self):
        return self.pickup_floor

    def get_dest_floor(self):
        return self.dest_floor

    def is_going_up(self):
        return self.dest_floor > self.pickup_floor

    def validate(self, total_floors):
        if self.pickup_floor < 0 or self.pickup_floor> total_floors:
            return False

        if self.dest_floor < 0 or self.dest_floor > total_floors:
            return False

        # No-op: Request to the same floor won't be served
        if self.pickup_floor == self.dest_floor:
            return False

        return True

class RequestQueue:
    def  __init__(self, floors, ts):
        self.request_queue = []
        self.ts = ts
        self.total_floors = floors

    def add_request(self, req):
        if not req.validate(self.total_floors):
            return

        self.request_queue.append(req)

    def is_empty(self):
        return len(self.request_queue) == 0

    def get_pending_requests(self):
        pending_reqs = []
        
        if self.is_empty():
            return None
        
        while self.is_request_ready(self.ts):
            req = self.request_queue.pop(0)
            pending_reqs.append(req)

        return pending_reqs

    def is_request_ready(self, cur_time):
        if self.is_empty():
            return False

        return self.request_queue[0].get_time() <= cur_time
        
    def clock_tick(self):
        self.ts = self.ts + 1