from elevator import Elevator

import pytest
from mock import MagicMock

LEVELS = 10

@pytest.fixture
def elevator():
    e = Elevator(LEVELS)
    return e

@pytest.fixture
def top_floor_elevator():
    e = Elevator(LEVELS)
    e.cur_level = LEVELS
    e.cur_direction = -1
    return e

@pytest.fixture
def bottom_floor_elevator():
    e = Elevator(LEVELS)
    e.cur_level = 0
    e.cur_direction = 1
    return e


def test_move_while_idle(elevator):
    assert elevator.cur_direction == 0
    assert elevator.cur_level == 1

    elevator.move()

    assert elevator.cur_level == 1

def test_move_down(top_floor_elevator):
    assert top_floor_elevator.cur_level == 10

    top_floor_elevator.move()

    assert top_floor_elevator.cur_level == 9

def test_move_up(bottom_floor_elevator):
    assert bottom_floor_elevator.cur_level == 0

    bottom_floor_elevator.move()

    assert bottom_floor_elevator.cur_level == 1

def test_move_up_no_op(top_floor_elevator):
    top_floor_elevator.cur_direction = 1
    assert top_floor_elevator.cur_level == LEVELS

    top_floor_elevator.move()

    assert top_floor_elevator.cur_level == LEVELS

def test_set_idle(top_floor_elevator):
    assert top_floor_elevator.cur_direction == -1

    top_floor_elevator.set_idle()

    assert top_floor_elevator.cur_direction == 0

def test_is_idle(elevator):
    assert elevator.cur_direction == 0
    assert elevator.is_idle()

def test_set_direction_up(elevator):
    assert elevator.cur_direction == 0
    
    elevator.set_direction_up()

    assert elevator.cur_direction == 1

def test_set_direction_down(elevator):
    assert elevator.cur_direction == 0
    
    elevator.set_direction_down()

    assert elevator.cur_direction == -1

def test_get_cur_level(elevator):
    assert elevator.cur_level == 1

    assert elevator.get_cur_level() == 1

def test_is_going_up(bottom_floor_elevator):
    assert bottom_floor_elevator.cur_direction == 1

    assert bottom_floor_elevator.is_going_up()

def test_is_going_down(top_floor_elevator):
    assert top_floor_elevator.cur_direction == -1

    assert top_floor_elevator.is_going_down()

def test_tick(elevator):
    elevator.move = MagicMock()
    elevator.tick()

    elevator.move.assert_called_once()