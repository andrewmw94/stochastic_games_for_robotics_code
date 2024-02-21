## About

This folder contains code to build model where at each state there is non-zero probability of human terminating (Probabilistic Human Termination case).

### Valid locations

`NUM_LOCATIONS` - Total no. of locations of interest + 3 (see below). 

Fixed locations
- `ROBOT_GRIPPER` location = 0
- `HUMAN_GRIPPER` location = 1
- `Termination state` location = #NUM_LOCS - 1
- The rest of the locations are where the objects can be placed. 

### Human actions

The set of valid human actions is:

- `humannoop` - with 95% human does nothing and with 5% probability evolves to `Terminal state` 
- `humantermselfloop` - a terminal state from which the human can not intervene with 100% probability. This action is a self loop to this state.
- `humangrasp` - human's action to grasp any object that is grounded. There is 5% probability of evolving to `Termination state` location.
- `humanplace` - human's action to place an object that is in `HUMAN_GRIPPER` location. There is 5% probability of evolving to `Termination state` location.
- `humanmotion` - human's action to move (without an object in `HUMAN_GRIPPER` location) from one location to another. There is 5% probability of evolving to `Termination state` location.
- `humanchooseterm` - human's action to choose terminal state. If the human chooses this action, with 100% probability it ends up `Termination state` location



### Robot Actions

The set of valid robot actions is:

- `robotnoop` - with 100% probability there is no effect to the position of robot's gripper or objects under the action. 
- `robotmotion` - with 100% probability robot's gripper moves from one location to another.
- `robotplace` - with 100% probability robot places the object in `ROBOT_GRIPPER` location at the gripper current location.
- `robotgrasp` - robot's action to grasp any object that are grounded. There is 10% probability that it might fail to grasp the object
- `robottermselfloop` - an action to the robot's terminal state once the task has been achieved. 