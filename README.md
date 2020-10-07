# Online-Courses-Harvard-CS50AI
This repository serves as a way for me to document my experience
with the [CS50 Artificial Intelligence class](https://cs50.harvard.edu/ai/2020/).

Following is just a little description about each of the assignments.
I do so to keep a thorough documentation on concepts that each assignment employs.

<big>Week 0</big>

**Degrees (BFS)**:
    
* The assignment is about finding a shortest path between two nodes
* The database comes from IMDb, and the task is to tell how one actor is connected to another through their common movie casts
* My solution is based on Breadth-First Search (BFS) because the task requires the shortest path between nodes
* To implement the search, I used a Queue-based Frontier. The Frontier is filled with neighboring nodes that share the same parameter(movie)
* You can find the demonstration of how it all works [here](https://www.youtube.com/watch?v=0bksDFskiRM&t=1s&ab_channel=DamirTemir).
    
**Tic-Tac-Toe (Minimax)**:

* The assignment is about writing an AI algorithm to play Tic-Tac-Toe optimally
* The pygame module provided inside the runner.py file was outside the scope of the project
* My solution is based on Minimax decision rule which perfectly works for games that clash two opponents against each other
    * The algorithm is all about calculating the best utility out of all possible solutions 
    The algorithm relies on calculating prospective steps that the opponent (AI) might take
* The tictactoe.py file (where the solution lies) consists of many minor functions that construct the game of Tic-Tac-Toe 
Thus, I recommend paying better attention to the last function called <i>minimax</i>.
    * The function determines which side AI plays for, and then finds the best optimal score that the player can get
* You can find the demonstration of how it works [here](https://www.youtube.com/watch?v=jgmtzfJTEgY&t=1s&ab_channel=DamirTemir).