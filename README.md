# Game-of-Life
Conway's Game of Life in Python using Pygame

Press 1 to pause the simulation  
Press 2 to slow down the simulation  
Press 3 to speed up the simulation  
Press 4 to toggle displaying the speed in FPS of the simulation  

The program will randomly generate a starting state if run from the command line without arguments. A starting state can be given by passing start coordinates separated by semicolons.  

For example:  
python game_of_life.py (50,50);(62,62)...  

The coordinates start at (0,0) in the upper left corner of the screen and end at (588,588) in the bottom right corner of the screen. Coordinates should be given in multiples of 12 with no spaces.
