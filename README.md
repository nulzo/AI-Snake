# About this Model
This model is a Python interpretation of the classical reinforcement learning algorithm. This algorithm works by rewarding the snake if it collects a treat (sometimes known as the fruit in Snake games), punishing the snake if it dies, and offering no reward if the snake exhibits neither of these actions. Death in this model can be classified as when the snake hits a border, or when the snake runs into itself. A common manifestation occurs during early iterations of the model where the snake chases it's own tail in an infinte loop to find the treat. Because of this, a feature was implemented that limits the movement of the snake if no treat is collected in a set amount of cycles. This formula can be expressed as "possible_movements = length(snake) * 100". The possible movements is adjusted accordingly to the size of the snake because as the snake gets larger it needs to dodeg itself to collect treats.

# Action
The snake movements depends on several actions. These actions can be classified as:

STRAIGHT  ->  [1, 0, 0]<br />
RIGHT     ->  [0, 1, 0]<br />
LEFT      ->  [0, 0, 1]<br />

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

# Improvements
This model can easily be improved upon. The main problem with the model is that it frequently crashes into itself when trying to find an optimal route to the treat. One such way to improve the model is to implement a convolutional layer that analyses the board during each new iteration. This would allow the snake to make more informed decisions each new cycle. This will likely be added in future updates.
