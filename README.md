# Elevator Control System Challenge
This repository is set-up to address the Elevator Control System Challenge.

https://docs.google.com/document/d/1TSjMN-q9bAfzptFBlvqBSRbODVSvUyJ--RN1XIUmyFM/edit#heading=h.9cms0o4oc22w

# Execution
This program can be run by invoking

`python main.py`

To configure specific scenarios, edit `src/main.py` on L13 and add any specific elevator requests you have
to watch the simulation take action and execute pick-ups/drop-offs.
`L13:    req_queue.add_request(Request(1, 10, 10.0))`

The Request object follows the signature:
`Request(pickup_floor, dropoff_floor, request_timestamp)`

Time is simulated in this challenge and we assume it takes the elevator one second to travel a floor and that
pickups and dropoffs are instantaneous (no delay).

The height of the elevator shaft (levels) is also modifiable in `main.py` as a constant.


# How long did you spend on this?
I exceeded the 2 hour allotment of spending time on this problem (3.5 hours in total). Since I'm in a bit of
an extreme timezone (PST +12 hours) and had limited time, I didn't want to delay the submission by attempting
to de-scope the problem.


# What, if anything, would you change if you had more time to spend on it?
I would refactor the ElevatorSystem's complexity so it has better readability and maintainability for the next
developer.

Also, significantly expanding the test suite coverage (a no-brainer in maintaining the stability of
a system that has real-world people impact).


# (Optional) What you would change if anything about this challenge? Anything else you want to share with us?
The challenge was enjoyable to tackle but I think it does take more than 2 hours to complete because of the
amount of ambiguity. In most professional contexts, cutting scope is common in these situations but since the
challenge is done in an async context, balancing a robust, well-thought out solution without going overboard
is a delicate act and can often take more time in that decision-making process (which eats into the 2 hours)
versus a well-scoped problem.


# Architectural overview
The main entities in this system are the:
- ElevatorSystem,
- Request,
- RequestQueue and
- Elevator

The driver file (main.py) manages the RequestQueue and ElevatorSystem to run the simulated experience.

In reality, a request queue would not be needed and would be managed internally real-time by the ElevatorSystem.

## Algorithm

We use a traditional algorithm for the elevator's journey by going to both ends of the elevator shaft to find
any requests for trips going in the same direction before moving in the other direction. There are numerous
other solutions that can be power-saving (electricity) and that involves graphs to find the shortest path
between requests or even first-come-first-serve (FCFS).

# Extending the solution
Things this solution can be extended to and doesn't current handle:
 - Countries where the 1st floor is not the ground floor (Asia)
 - Buildings that have multiple underground levels
 - Multiple elevators serving the building
 - Elevator capacity limits (weight/people) and
 - potential overriding requests when an elevator is full (avoiding more pick-ups) for more efficiency
 - A multi-threaded context where this would handle a system in real-time vs simulated time
 - An admin API to control the elevator with more specific actions