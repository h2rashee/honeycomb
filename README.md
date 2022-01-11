# Elevator Control System Challenge
This repository is set-up to address the Elevator Control System Challenge.

https://docs.google.com/document/d/1TSjMN-q9bAfzptFBlvqBSRbODVSvUyJ--RN1XIUmyFM/edit#heading=h.9cms0o4oc22w

# Execution
This program can be run by invoking:

`make run`

To configure specific scenarios, edit `src/main.py` on L13 and add any specific elevator requests you have
to watch the simulation take action and execute pick-ups/drop-offs.

`L13:    req_queue.add_request(Request(1, 10, 10.0))`

The Request object follows the signature:

`Request(pickup_floor, dropoff_floor, request_timestamp)`

Time is simulated in this challenge and we assume it takes the elevator one second to travel a floor and that
pickups and dropoffs are instantaneous (no delay).

The height of the elevator shaft (levels) is also modifiable in `main.py` as a constant.

# Running tests
Unit tests can be executed by running:

`make test`


# How long did you spend on this?
I exceeded the 2 hour allotment of spending time on this problem (3.5 hours in total). Since I'm in a bit of
an extreme timezone (PST +12 hours) and had limited time, I didn't want to delay the submission by attempting
to de-scope the problem (via a synchronous conversation).


# What, if anything, would you change if you had more time to spend on it?
I would first parameterize the amount of levels in the building and create a better input mechanism to handle
elevator requests.

I would refactor the ElevatorSystem's complexity so it has better readability and maintainability for the next
developer.


# (Optional) What you would change if anything about this challenge? Anything else you want to share with us?
The challenge was enjoyable to tackle but I think it does take more than 2 hours to complete because of the
amount of ambiguity.

In most professional contexts, cutting scope is common in these situations but since the
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
any requests for trips going in the same direction before moving in the other direction. In the event that opposite
direction requests come at the same time for an idle elevator, the request going up is served first (no semantic
drive behind that decision).

There are numerous other solutions that can be power-saving (electricity) and that involves graphs to find
the shortest path between requests or even first-come-first-serve (FCFS) but I picked the approach that is
most often seen in the wild.

## Data Structures

We take a bit of an unorthodox approach here to track elevator pick-ups and drop-offs by utilizing four hashtables
`trips_up`,`trips_down` and `trips_up_requests`,`trips_down_requests`.

We utilize `trips_up` and `trips_down` to denote pick-ups and drop-offs on a specific floor in the up and down direction
respectively. This differentiation is needed because we only pick-up people in the same direction as the one the elevator
is heading. We don't track the number of people that are being picked-up/dropped off on a particular floor or the capacity
of the elevator. We simply denote whether a stop needs to be made on that floor for a trip heading up or down by using
a 1 or 0 (a rough boolean representation).

When a request is received, we mark the stop and the direction of the stop (READ: pick-up) appropriately. Since we can only
perform drop-offs after the respective pick-up, we track this using the parallel hashtables `trips_up_requests` and
`trips_down_requests`. We store a list of Request objects on the index of the respective pick-up floor. When a pick-up in
the direction is performed, we take any Request objects for that floor and add the drop-off stops to `trips_up` and
`trips_down` and clear the list of Request objects (for that direction). This repeats until there are no requests left to
process and the stream (RequestQueue) has ended.

This solution does not extend well when scaling to multiple elevators. This was a decision made to trade-off limited time
to work on this problem.

# Extending the solution
Things this solution can be extended to and doesn't current handle:
 - Countries where the 1st floor is not the ground floor (Asia)
 - Buildings that have multiple underground levels
 - Multiple elevators serving the building
 - Elevator capacity limits (weight/people) and
 - Potential overriding requests when an elevator is full (avoiding more pick-ups) for more efficiency
 - A multi-threaded context where this would handle a system in real-time vs simulated time
 - An admin API to control the elevator with more specific actions
 - Changing the elevator request serving algorithm (mentioned in prior section) to optimize for KPIs (power used, time waiting)
 - Removing the unused floor 0 that was left as tech debt and align array indexes with actual level numbers