# Tic-Tac-Toe Game

## Requirements

- Python 3.9 or greater
- pygame

## Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## How to Play

- Select difficulty level from the menu (Easy, Medium, Hard, or Impossible)
- Click on any empty cell to place your X
- The AI (O) will automatically make its move
- First player to get 3 in a row wins
- Track your performance with the built-in statistics
- Build your win streak and challenge yourself!

## Features

- **Multiple Difficulty Levels**: Choose your challenge
- **Smart AI**: Minimax algorithm with alpha-beta pruning
- **Statistics**: Win rate, streaks, and game history
- **Smooth Animations**: Visual feedback for all moves
- **Modern UI**: Clean design with difficulty-based themes
- **AI First Move**: On harder difficulties, AI may go first

## Project Structure

```
.
├── main.py          # Entry point and game loop
├── game_logic.py    # Game state, rules, and statistics
├── ai.py            # AI player with adaptive difficulty
├── renderer.py      # UI rendering and animations
├── constants.py     # Game configuration and colors
└── requirements.txt # Python dependencies
```

## AI Difficulty

The AI adapts its strategy based on the selected difficulty:
- **Easy**: Makes mistakes ~40% of the time, simple strategy
- **Medium**: Strategic play with occasional errors (~15%)
- **Hard**: Strong opponent with rare mistakes (~5%), may go first
- **Impossible**: Perfect play using full minimax depth, may go first

## Technical Implementation

- **Minimax Algorithm**: Full game tree search with alpha-beta pruning
- **Dynamic Difficulty**: AI behavior adapts based on selected level
- **Statistics Tracking**: Real-time win rate and streak monitoring
- **Smooth Animations**: CSS-like animation system for game elements