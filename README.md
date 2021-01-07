# Battleship

## Story

> One of the reasons microcomputers progressed so fast is people are willing to
> accept crashes. It's faster to build something and try it, even if it means
> you'll have to rebuild later... If you spent too much time building and
> massaging one vehicle, you don't learn anything.
> <div style="text-align:right">John Carmack,<br>lead programmer of Doom (and more)</div>

In this project your job is to implement the
[Battleship game](https://en.wikipedia.org/wiki/Battleship_%28game%29) for two players.

## What are you going to learn?

You will learn and practice how to do the following things in Python:

- variables
- functions,
- loops and conditionals,
- nested lists,
- print formatting,
- handling user input,
- error handling,
- clean code.



## Tasks

1. Implement the placement phase of the battleship program where players can place ships on a board.
    - Row (as character), column (as number) and direction (horizontal/vertical) for placement are asked from user as user input
    - A 5x5 board is shown after each placement like below, where
`0` indicates an empty space and `X` indicates a ship part
```
  1 2 3 4 5
A 0 0 0 0 0
B X X 0 0 0
C 0 0 0 0 0
D 0 0 0 0 0
E 0 0 0 0 0
```
    - If user enters invalid input (outside range), then the error message `Invalid input!` is displayed and the program asks again for an input
    - User can place ships with at least two different sizes (e.g. 1 block long and 2 blocks long)
    - The program keeps asking for input until all ships are placed
    - If user wants to place two ships next to each other (touching corners are okay), then the error message `Ships are too close!` is displayed and the program asks again for an input
    - After one player is finished with the placement phase, a waiting screen is displayed with no boards just with the message `Next player's placement phase`
    - If the user presses any button on the waiting screen, the second player's placement phase begins

2. Implement the shooting phase of the battleship program where players have to sink each others' ships.
    - Row (as character) and column (as number) for shooting are asked from user as user input
    - Both players' 5x5 board is shown after each shooting like below, where
`0` indicates an undiscovered tile, `M` indicates a missed shot,
`H` indicates a hit ship part and `S` indicates a sunk ship part
```
Player 1      Player 2
  1 2 3 4 5     1 2 3 4 5
A 0 0 0 0 M   A 0 0 0 0 M
B S S M 0 0   B 0 0 0 0 0
C 0 0 0 0 0   C H M 0 0 0
D 0 0 0 0 0   D 0 0 0 0 0
E 0 0 0 0 0   E 0 0 S 0 0
```
    - Players change turns after each shot
    - It is clearly indicated, whose turn is happening actually
    - If user enters invalid input (outside range), then the error message `Invalid input!` is displayed and the program asks again for an input (shooting twice at the same spot is a valid but unnecessary move)
    - Hitting, missing and sinking ship (parts) results in a message displayed as `You've hit a ship!`, `You've missed!` and `You've sunk a ship!` respectively
    - If one of the players sinks all ships of the other player then the message `Player <n> wins!` is displayed where <n> is the number of the player who wins and the game ends

3. [OPTIONAL] Extend the game so user can choose a custom board size at the beginning.
    - Before the placement phase the size of the board is asked from the user as user input
    - If the given board size is out of range (5-10) then the error message `Invalid input! (must be between 5-10)` is displayed
    - The given board size is used and displayed during the placement phase with characters between A-J indicating rows and numbers between 1-10 indicating columns
    - The given board size is used and displayed during shooting phase with characters between A-J indicating rows and numbers between 1-10 indicating columns

4. [OPTIONAL] Extend the game so there is a turn limit in the game after that the game result is a draw.
    - Before the placement phase the turn limit is asked from the user as user input
    - If the given turn limit is out of range (5-50) then the error message `Invalid input! (must be between 5-50)` is displayed
    - The number of turns left is constantly displayed above the boards (e.g. `Turns left: 18`)
    - The number of turns left is decreased after each player had one shot
    - If the number of turns left reaches zero the message `No more turns, it's a draw!` is displayed and the game ends

5. [OPTIONAL] Extend the game so there is a single player mode where the user can play against the computer
    - Before the placement phase the game mode is asked from the user as user input and by printing a menu with two items (`1. Single player`, `2. Multiplayer`)
    - If the given choice is out of range (1-2) then the error message `Invalid input!` is displayed
    - If multiplayer is chosen as game mode then game works with two players as in the above tasks
    - If single player is chosen as game mode then both during placement and shooting phases Player 2 is the computer and generates its moves

## General requirements

- Variable names in the program are meaningful nouns and not abbreviated
- Function names in the program are meaningful verbs and not abbreviated
- There are no unnecessary (dead) code or comments in the program
- There are no duplicating code parts or code parts doing the same thing differently in the program
- There are no function that doing more than one thing in the program

## Hints

- There is no skeleton code for this project (on purpose), just an empty file.
  Try to create it from scratch.
- Focus on features first, and refactor it at the end.

## Background materials

- <i class="far fa-exclamation"></i> [Basics of clean code](project/curriculum/materials/competencies/clean-code.md.html)
- <i class="far fa-exclamation"></i> [Refactoring in action](project/curriculum/materials/competencies/clean-code/refactoring.md.html)
