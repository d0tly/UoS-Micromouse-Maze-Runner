# Maze Runner

Maze Runner is a Python project designed to simulate a runner navigating through a maze. The project includes functionalities for creating mazes, controlling the runner's movements, and finding the shortest path to a goal.

## Features

- Create and manipulate mazes.
- Control a runner's movements within the maze.
- Find the shortest path from a starting position to a goal.
- Export exploration steps and statistics to CSV and text files.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/maze-runner.git
    ```
2. Navigate to the project directory:
    ```sh
    cd maze-runner
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running the Maze Runner

To run the Maze Runner, use the following command:
```sh
python maze_runner.py <maze_file> --starting <start_x,start_y> --goal <goal_x,goal_y>
```
Example
```sh
python maze_runner.py maze1.mz --starting 2,1 --goal 4,5
```

Example
Here is an example of how to use the Maze Runner:

Create a maze file (maze1.mz) with the following content:
```sh
#######
#.....#
#.###.#
#.....#
#######
```

Run the Maze Runner:
```sh
python maze_runner.py maze1.mz --starting 1,1 --goal 5,3
```
The program will output the exploration steps and the shortest path to the goal.

Files
maze_runner.py: Main script to run the Maze Runner.
runner.py: Contains the Runner class and functions to control the runner.
maze.py: Functions to create and manipulate mazes.
test_runner.py: Unit tests for the runner functions.
algoChecker.py: Additional script for checking algorithms and exploring the maze.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Mykyta Chursin
Acknowledgments
University of Southampton


This README file provides an overview of the project, installation instructions, usage examples, and information about the files and author.
