import pytest
from mock import MagicMock

from elevator_system import ElevatorSystem
from elevator_requests import Request

LEVELS = 10
TS = 0

@pytest.fixture
def elevator_system():
    es = ElevatorSystem(LEVELS, TS)
    return es

@pytest.fixture
def elevator_request_1():
    req = Request(2, 5, 1.0)
    return req

@pytest.fixture
def elevator_request_2():
    req = Request(7, 3, 1.0)
    return req

def test__init__(elevator_system):
    assert elevator_system.trips_up == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert elevator_system.trips_down == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert elevator_system.trips_up_requests == [[], [], [], [], [], [], [], [], [], [], []]
    assert elevator_system.trips_down_requests == [[], [], [], [], [], [], [], [], [], [], []]
    assert elevator_system.top_floor == LEVELS
    assert elevator_system.ts == TS
    assert elevator_system.elevator is not None

def test_clock_tick(elevator_system):
    elevator_system.process_requests_for_cur_floor = MagicMock()
    elevator_system.direct_the_elevator = MagicMock()
    elevator_system.elevator.tick = MagicMock()

    elevator_system.clock_tick()

    elevator_system.process_requests_for_cur_floor.assert_called_once()
    elevator_system.direct_the_elevator.assert_called_once()
    elevator_system.elevator.tick.assert_called_once()
    assert elevator_system.ts == 1

def test_process_requests_from_queue(elevator_system, elevator_request_1, elevator_request_2):
    elevator_request_1.is_going_up = MagicMock(return_value=True)
    elevator_request_2.is_going_up = MagicMock(return_value=False)
    assert elevator_system.trips_up[2] == 0
    assert len(elevator_system.trips_up_requests[2]) == 0
    assert elevator_system.trips_down[7] == 0
    assert len(elevator_system.trips_down_requests[7]) == 0

    elevator_system.process_requests_from_queue([elevator_request_1, elevator_request_2])

    assert elevator_system.trips_up[2] == 1
    assert elevator_system.trips_up_requests[2][-1] == elevator_request_1
    assert elevator_system.trips_down[7] == 1
    assert elevator_system.trips_down_requests[7][-1] == elevator_request_2