# Action
The snake movements depends on several actions. These actions can be classified as:

STRAIGHT  ->  [1, 0, 0]
RIGHT     ->  [0, 1, 0]
LEFT      ->  [0, 0, 1]

As shown, the snake cannot turn backwards while moving in a straight direction. If the snake is moving forward, the only option is to either turn left or right. This is implemented to prevent the snake from turning it's head 180 degrees and running into itself. Without this, the snake would easily make errors that would cause premature death.

# State
There are several states in which the snake can inhabit. These states are:

   ### ☢︎ Danger ☢︎
   This state occurs when there is "danger" straight ahead, to the left, or to the right relative to the head of the snake. Danger within this model can be classified as the borders surrounding the game area.

   ### ⇡ Movement ⇣
   There are four directions that the snake can inhabit. These directions are represnted as up (0,+), down (0,-), left (-,0), and right (+,0) on an (x,y)      cordinate plane.
   
   ### ☺︎ Treat ☺︎
   This state is satisfied when there is a "treat" in the vacinity of the snakes head. Similar to the danger state, this state is achieved when the treat is immediately next to the snakes head.
   
# Model
The model is trained on PyTorch, a machine learning library built for python.
