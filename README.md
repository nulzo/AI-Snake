# Action
The snake movements depends on several actions. These actions can be classified as:

STRAIGHT  ->  [1, 0, 0]
RIGHT     ->  [0, 1, 0]
LEFT      ->  [0, 0, 1]

As shown, the snake cannot turn backwards while moving in a straight direction. If the snake is moving forward, the only option is to either turn left or right. This is implemented to prevent the snake from turning it's head 180 degrees and running into itself. Without this, the snake would easily make errors that would cause premature death.

# State
There are several states in which the snake can inhabit. These states are:
  ## Danger
   ### Danger Straight
   This state occurs when there is "danger" straight ahead. Danger within this model can be classified as the borders surrounding the game area.
   ### Danger Left
   This state occurs when there is danger to the left side of the snake, relative to the direction of the head.
   ### Danger Right
   This state occurs when there is danger to the right side of the snake, relative to the direction of the head.
  
  ## Directional
   ### Movement
   There are four directions that the snake can inhabit. These directions are represnted as up (0,+), down (0,-), left (-,0), and right (+,0) on an (x,y)      cordinate plane.
