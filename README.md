# Pong
# README.md generator script

content = """
# Pong Game

A simple Pong game implemented in Python using the Pygame library.

## How to Play

- Press `Enter` to start the game.
- Use the `Up` and `Down` arrow keys to control the paddle.
- Score points by making the ball pass the opponent's paddle.
- The game ends when one of the players reaches a score of 10.

## Controls

- **Up Arrow**: Move paddle up
- **Down Arrow**: Move paddle down
- **R**: Restart the game
- **Q**: Quit the game

## Dependencies

- Python 3.x
- Pygame library

## How to Run

1. Install Python from [python.org](https://www.python.org/).
2. Install Pygame using `pip install pygame`.
3. Run the game script: `python pong.py`.

"""

# Write content to README.md file
with open("README.md", "w") as readme_file:
    readme_file.write(content)

print("README.md generated successfully.")
