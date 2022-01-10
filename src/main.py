from elevator_system import ElevatorSystem
from elevator_requests import Request, RequestQueue

LEVELS = 10
TS = 0

if __name__ == "__main__":
    print "Bootstrapping elevator control system"
    es = ElevatorSystem(LEVELS, TS)
    req_queue = RequestQueue(LEVELS, TS)

    # Requests must be added to the queue in chronological order (time-sorted)
    # req_queue.add_request(Request(<pickup_floor>, <dropoff_floor>, <request_timestamp>))
    req_queue.add_request(Request(1, 7, 1.0))
    req_queue.add_request(Request(10, 1, 10.0))
    req_queue.add_request(Request(1, 10, 10.0))

    def clock_tick():
        '''
            Represents a single second passing (we are simulating time)
        '''
        es.clock_tick()

        req_queue.clock_tick()

        reqs = req_queue.get_pending_requests()
        if reqs:
            es.process_requests_from_queue(reqs)

    while es.has_active_trip() or not req_queue.is_empty():
        clock_tick()

    print "Elevator simulation complete"