# Light Up Puzzle Generator

## Description
The Light Up Puzzle Generator is an interactive GUI for playing light-up board puzzles. You can generate a random puzzle based on difficulty, as well as create custom puzzles and solve them on your own.

### Puzzle Generator
You can generate puzzles of the three given sizes: small (7x7), medium (10x10), and large (14x14). The program will consider the difficulty you chose (easy or hard) and generate a puzzle. The program will first try to create a puzzle with a single solution, but after a certain attempts it is guaranteed to produce a puzzle even if it has multiple solutions. All puzzles are solvable.

If you don't like how puzzles are being generated, you can make a custom .xml file to create your own puzzle. The puzzle format of your xml file must match the format of puzzle files created by this program in order to be readable.

### LEGUP Puzzle Generator
If you are a part of the LEGUP team, you may also want to use this to create new Light Up Puzzles for LEGUP. It will always create a new board, which means if you open up the file you saved on LEGUP, all the progress you made on the board will be lost. 

### Save and Load
You can save the current state of the board (whether finished or not) by clicking the 'save' button. You can load saved files as well. You can load custom puzzles the same way you would load any computer-generated puzzle. 

**You cannot load files created for LEGUP as their formats are different.**

### Solving Puzzles 
You can solve a puzzle manually. Left click a tile to place lightbulbs. Right click a tile to mark it and indicate a lightbulb isn't there. 

You can load the solved board state by clicking 'Solve'.

**The feature for auto-solving custom puzzles has not been implemented. If you'd like it to solve it you need to provide the solution in the custom xml file you provide.**

## Running the program
1. Clone the repository and download the files locally
2. Navigate to the folder the files are stored
3. Go to dist. There should be one folder named 'main'. Click on it.
4. Run main.exe 
