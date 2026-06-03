1. Navigation is an excellent example of a computationally hard problem that AI can help solve more efficiently. 

A heuristics is some additional piece of information, a rule, function or constraint - that informs otherwise brute force algorithm to act in a more optimal manner.    

Does crow finds the shortest path between two points? 

A* is an AI algorithm that uses heuristics to find the shortest path between two points.

2. Many real world problems require us to react to changes to our environment, maybe changes caused by things like other drivers. I would expect intelligent agent to be able to react to such changes and maybe even anticipate them. What if we could adapt similar search strategies to solve problems that involve other agents, like playing games. AI agents can win game from chess to starcraft. 

3. Tic Tac Toe Question:

Goal: Our goal is to use a search strategy similar to the route-finding problem to design an AI that can play tic-tac-toe. Now, in your opinion, what is your nodes and edges in the graph that we search ? Answer of this question would be to think of whole board as a node, so we'll have one node for every possible arrangement of Xs and Os on the board. In this case, connect two nodes if there is a valid move that changes the board from one to another.

Here, edges embody the rules of the game. For instance, you can go to a finite number of states from each current state. 

Mini-Max algorithm: You are trying to maximize your chances of winning on your turn, and your opponent is trying to minimize your chances of winning on their turn. This approach is so effective because when you rule out a move as being bad, you are actually getting rid of its potential successors from consideration. This a better definition of intelligent agent to me. It is able to anticipate and plan around expected changes in its environment including those introduced by other agents.

4. We often think intelligence as the ability to accomplish a variety of intellectual tasks just like humans do. A subfield of AI called artificial general intelligence (AGI) deals with this specific goal. But we are far from replicating the complex nature of human thinking. 

Intelligence should be defined within the context of tasks. For example, If my goal is to solve sudoku puzzles, and I am able to do it with decent rate of success. Then I can say I am intelligent to solve sudoku puzzles. 

5. Understanding the task or problem domain is key to designing intelligent systems. 

An intelligent agent is one that takes that take actions to maximize its expected utility given a desired goal. This is commonly referred to as a rational behavior.

6. Solving a Sudoku problem:

https://norvig.com/sudoku.html

Sudoku is one of the world's most popular puzzles. It consists of a 9x9 grid, and the objective is to fill the grid with digits in such a way that each row, each column, and each of the 9 principal 3x3 subsquares contains all of the digits from 1 to 9. The detailed rules can be found, for example, [here](http://www.conceptispuzzles.com/?uri=puzzle/sudoku/rules).

The main goal of this project is to build an intelligent agent that will solve every sudoku while introducing you to two powerful techniques that are used throughout the field of AI:

- Constraint Propagation

When trying to solve a problem, you'll find that there are some local constraints to each square. These constraints help you narrow the possibilities for the answer, which can be very helpful. We will learn to extract the maximum information out of these constraints in order to get closer to our solution. Additionally, you'll see how we can repeatedly apply simple constraints to iteratively narrow the search space of possible solutions. Constraint propagation can be used to solve a variety of problems such as calendar scheduling, and cryptographic puzzles.

- Search

In the process of problem solving, we may get to the point where two or more possibilities are available. What do we do? What if we branch out and consider both of them? Maybe one of them will lead us to a position in which three or more possibilities are available. Then, we can branch out again. At the end, we can create a whole tree of possibilities and find ways to traverse the tree until we find our solution. This is an example of how search can be used.
These ideas may seem simple and they're actually intended to be! Through this lesson you'll see how AI is really composed of very simple ideas that can be put together to solve complex problems. Throughout this lesson, we challenge you to think of how you can apply these ideas to build AI agents to solve other puzzles and problems in your world!

7. Here is the solution for the Sudoku.

Your solution probably consisted of the following two steps (and maybe more):

- If a box has a value, then all the boxes in the same row, same column, or - same 3x3 square cannot have that same value.
- If there is only one allowed value for a given box in a row, column, or 3x3 square, then the box is assigned that value.

8. Boxes, Units and Peers:

And let's start naming the important elements created by these rows and columns that are relevant to solving a Sudoku:

- The individual squares at the intersection of rows and columns will be called boxes. These boxes will have labels 'A1', 'A2', …, 'I9'.

- The complete rows, columns, and 3x3 squares, will be called units. Thus, each unit is a set of 9 boxes, and there are 27 units in total.

- For a particular box (such as 'A1'), its peers will be all other boxes that belong to a common unit (namely, those that belong to the same row, column, or 3x3 square).

Let's see an example. In the grids below, the set of highlighted boxes represent units. Each grid shows a different peer of the box at E3.

9. Constraint Propagation:
 
If you've made it this far, you've already gained hands on exposure to a powerful technique in AI - Constraint Propagation. Constraint Propagation is all about using local constraints in a space (in the case of Sudoku, the constraints of each square) to dramatically reduce the search space. As we enforce each constraint, we see how it introduces new constraints for other parts of the board that can help us further reduce the number of possibilities. We have an entire lesson devoted to Constraint Propagation but let's quickly see some other famous AI problems it helps us solve.




