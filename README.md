# Chess Analyser
Chess.comâ€‘style Python chess analyser with Stockfish, analysis, and game review.
=======
# Chess Game with Stockfish AI

A command-line chess game where you can play against the powerful Stockfish chess engine.

## Features\r\n# Chess Analyser\r\nChess.comâ€‘style Python chess analyser with Stockfish, analysis, and game review.

[![Build Windows](https://github.com/malaykasana/ChessAnalyser/actions/workflows/build-windows.yml/badge.svg)](https://github.com/malaykasana/ChessAnalyser/actions/workflows/build-windows.yml)

This project includes both a full GUI app (`chess_gui.py`) and a simple command-line game (`main.py`).


### Command-Line Version (main.py)
- â™Ÿ Full chess game implementation with move validation
- ðŸ¤– Play against Stockfish AI engine
- ðŸŽ¨ Clear command-line board display
- âš™ï¸ Adjustable AI difficulty (thinking time)
- â†©ï¸ Undo moves
- âœ… Detects checkmate, stalemate, and draw conditions
- ðŸ“ Move input in standard UCI notation (e.g., e2e4)

### GUI Version (chess_gui.py) âœ¨NEW
- ðŸŽ® **Graphical chess board** with Unicode pieces
- ðŸ–±ï¸ **Click to move** - Intuitive drag-free interface
- ðŸ’¡ **Legal move highlights** - See where you can move
- ðŸ¤– **AI opponent** with adjustable thinking time
- ðŸŽ¨ **6 Beautiful themes** - Classic, Blue, Green, Purple, Modern, Dark
- ðŸ”„ **New Game, Undo** buttons
- âšªâš« **Choose your color** (White or Black)
- ðŸ“Š **Live evaluation bar** - Real-time position analysis
- ðŸ’¡ **Hint system** - Get best move suggestions from Stockfish
- ðŸ’¾ **Save/Load PGN** - Export and import games
- ðŸ“œ **Move history** - View all moves in the game
- ðŸ”— **Account integration** - Connect Lichess & Chess.com accounts
- ðŸ“Š **Game review mode** - Fetch and analyze your online games
- ðŸ” **Move-by-move analysis** - Find blunders, mistakes, and inaccuracies
- â®â­ **Game navigation** - Step through moves with live eval

## Requirements

- Python 3.7+
- Stockfish chess engine installed on your system

## Installation 
## Windows Version is also available in RELEASES section (No dependencies required).

### 1. Install Python Dependencies

```powershell
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate

# Install required packages
pip install -r requirements.txt
```

### 2. Install Stockfish Engine

Download and install Stockfish from: https://stockfishchess.org/download/

**Windows:**
- Download the Windows executable
- Extract it to a location (e.g., `C:\Program Files\Stockfish\`)
- Add to PATH or provide the full path when running the game

**Linux:**
```bash
sudo apt-get install stockfish
```

**macOS:**
```bash
brew install stockfish
```

## Usage

### Quick Start

**Command-Line Version:**
```powershell
python main.py
```

**GUI Version (Graphical Interface):**
```powershell
python chess_gui.py
```


### Run with VS Code tasks

- Use the built-in task "Run Chess Analyser" to start the app.
- Use the built-in task "Build Windows EXE" to package a distributable.
### Game Setup

When you start the game, you'll be prompted to:
1. Choose your color (white/black)
2. Set AI difficulty (0.5-10 seconds thinking time)
3. Optionally specify a custom Stockfish path

### Making Moves

Enter moves in UCI notation:
- `e2e4` - Move piece from e2 to e4
- `g1f3` - Move knight from g1 to f3
- `e7e8q` - Pawn promotion (to queen)

### Special Commands

- `help` - Display move format help
- `undo` - Take back the last move (yours and AI's)
- `quit` or `exit` - End the game

### Example Game Session

```
Choose your color (white/black) [white]: white
AI difficulty - thinking time in seconds (0.5-10) [1.0]: 1.5

â™Ÿ Chess Game - Play against Stockfish â™Ÿ
========================================
You are playing as: White
AI difficulty (thinking time): 1.5s

========================================
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
========================================
Turn: White
Legal moves: 20

Your move (e.g., 'e2e4' or 'quit'): e2e4
```

## Project Structure

```
New folder/
â”œâ”€â”€ main.py              # Command-line chess game
â”œâ”€â”€ chess_gui.py         # GUI version with tkinter âœ¨NEW
â”œâ”€â”€ requirements.txt     # Python dependencies
â”œâ”€â”€ README.md           # This file
â”œâ”€â”€ .gitignore          # Git ignore rules
â”œâ”€â”€ .venv/              # Virtual environment
â””â”€â”€ .github/
    â””â”€â”€ copilot-instructions.md
```

## Dependencies

- **python-chess** (1.999): Chess game logic and move validation
- **stockfish** (3.28.0): Python wrapper for Stockfish engine
- **requests** (2.31.0): HTTP library for fetching online games

## How to Use New Features

### ðŸ’¡ Hints
1. Click the **"ðŸ’¡ Hint"** button during your turn
2. The best move will be highlighted in sky blue
3. Click again to hide the hint

### ðŸ’¾ Save & Load Games
- **Save PGN**: Export your current game to a .pgn file
- **Load PGN**: Import and replay any chess game

### ðŸ“Š Game Review
1. Click **"âš™ï¸ Accounts"** to set up your usernames:
   - Enter your Lichess username
   - Enter your Chess.com username
   - Click Save
2. Click **"ðŸ“Š Review"** to fetch your recent games
3. View game details including opponents, results, and dates

### ðŸ” Game Analysis (Review Mode)
1. **Load a PGN file** with "Load PGN" button
2. Use navigation buttons to step through moves:
   - **â® Start**: Go to beginning
   - **â—€ Prev**: Previous move
   - **Next â–¶**: Next move
   - **End â­**: Go to end
3. **Watch evaluation bar** change with each move (left side of board)
   - White advantage: Bar goes down (white area)
   - Black advantage: Bar goes up (black area)
   - Center red line = Equal position
4. **Click "ðŸ” Analyze All Moves"** to get full game analysis:
   - Finds blunders (âŒ -2.0 or worse)
   - Finds mistakes (âš ï¸ -1.0 to -2.0)
   - Finds inaccuracies (?! -0.5 to -1.0)
   - Shows evaluation changes
5. **Learn from mistakes** and improve your game!

### ðŸŽ¨ Themes
1. Click **"ðŸŽ¨ Theme"** button
2. Choose from 6 beautiful themes:
   - **Classic**: Traditional brown & beige
   - **Blue**: Cool blue tones
   - **Green**: Natural green board
   - **Purple**: Royal purple theme
   - **Modern**: Lichess-style green
   - **Dark**: Dark mode for night play
3. Preview before applying
4. Theme auto-saves for next session

### ðŸ“Š Evaluation Bar
- **Left side of board** shows live position evaluation
- **Updates automatically** after each move
- **White advantage**: Bar extends downward (white area grows)
- **Black advantage**: Bar extends upward (black area grows)
- **Equal**: Red line in center
- **Numbers**: +2.0 = White up 2 pawns, -1.5 = Black up 1.5 pawns
- **Â±âˆž**: Winning/losing position or mate detected

### ðŸ“œ Move History
- Click **"ðŸ“œ Moves"** to see all moves in the current game
- Moves are displayed in standard algebraic notation (SAN)

## Troubleshooting

### Stockfish Not Found

If you see "Stockfish engine not found":
1. Make sure Stockfish is installed
2. Add Stockfish to your system PATH, or
3. Provide the full path when prompted at startup

### Virtual Environment Issues

Make sure to activate the virtual environment before running:
```powershell
.\venv\Scripts\Activate
```

### Move Format Errors

Use UCI notation: `source_square + destination_square`
- Valid: e2e4, g1f3, a7a8q
- Invalid: e4, Nf3, O-O (use e1g1 for castling)

## Future Enhancements

- [ ] GUI interface with tkinter or pygame
- [ ] Save/load game functionality (PGN format)
- [ ] Multiple difficulty presets
- [ ] Game analysis and move suggestions
- [ ] Opening book integration
- [ ] Time controls and clocks

## License

This project is open source and available for educational purposes.

## Credits

- Chess engine: [Stockfish](https://stockfishchess.org/)
- Python chess library: [python-chess](https://python-chess.readthedocs.io/)

---

Enjoy your game! â™”â™•â™–â™—â™˜â™™
>>>>>>> d8e6fd4 (Initial commit: Chess Analyser with GUI, review, Windows build)


