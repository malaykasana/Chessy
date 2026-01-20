# Chess Analyser - Quick Start Guide

## ✅ Your App is Ready!

The Chess Analyser application is now fully functional and ready to use.

### Launch Options

#### Option 1: Direct Command (Fastest)
```powershell
python chessy.py
```

#### Option 2: Using Launcher Script
```powershell
python launcher.py
```

#### Option 3: Batch File (Windows)
Double-click: `run_chessy.bat`

#### Option 4: CLI Version
```powershell
python main.py
```

---

## 🎮 Game Controls

### Mouse Controls
- **Click piece** → Select and see legal moves (green squares)
- **Click destination** → Move piece
- **Click same piece** → Deselect

### Buttons
- **New Game** → Start fresh
- **Undo Move** → Take back last move
- **Hint** → Show best move (sky blue)
- **Save PGN** → Export game
- **Load PGN** → Import game

### Settings
- **Play as:** White or Black
- **AI time:** 0.5 - 10 seconds per move
- **Theme:** 8 beautiful themes
- **Piece Set:** Classic, Bold, or Text

---

## 🎨 Themes Available

1. **Classic** - Traditional brown & beige
2. **Chesscom** - Chess.com style
3. **Slate Dark** - Dark professional theme
4. **Blue** - Cool blue tones
5. **Green** - Natural green board
6. **Purple** - Royal purple
7. **Modern** - Lichess-inspired
8. **Dark** - Night mode

---

## 📊 Game Features

### Real-Time Evaluation Bar
- Shows position advantage (left side)
- Updates after each move
- White advantage = bar extends down
- Black advantage = bar extends up

### Move History
- View all moves in notation
- Click "Moves" button to see full list
- Moves displayed in algebraic notation

### Captured Pieces
- See what each player captured
- Piece count and display

### Account Integration
- Connect Lichess & Chess.com
- Fetch your recent games
- Review and analyze games

---

## ⚙️ Settings

All settings auto-save to `chess_settings.json`:
- Usernames (Lichess/Chess.com)
- Current theme
- Piece style
- Engine difficulty
- Your preferences

---

## 🐛 If Something Goes Wrong

### App Won't Start
```powershell
# Check dependencies
pip install -r requirements.txt

# Run with diagnostics
python chessy.py
```

### Stockfish Not Found
1. Download: https://stockfishchess.org/download/
2. Add to PATH or place in `stockfish/` folder
3. Restart the app

### GUI Issues
- Ensure tkinter is installed
- Try different theme
- Check display settings

---

## 🚀 Next Steps

1. **Play a Game** - Start with "New Game"
2. **Practice Hints** - Use "Hint" to learn moves
3. **Adjust Difficulty** - Change AI time setting
4. **Save Games** - Export to PGN format
5. **Try Themes** - Switch board themes
6. **Connect Accounts** - Add Lichess/Chess.com

---

## 📝 Project Files

| File | Purpose |
|------|---------|
| `chessy.py` | Main GUI application |
| `main.py` | Command-line version |
| `launcher.py` | Python launcher |
| `run_chessy.bat` | Windows launcher |
| `requirements.txt` | Dependencies |
| `chess_settings.json` | User settings |
| `FEATURES.md` | Feature documentation |
| `REWRITE_SUMMARY.md` | Technical details |

---

## 💾 File Locations

- **Saved Games:** Your PGN files (anywhere you choose)
- **Settings:** `chess_settings.json` (in project folder)
- **Stockfish:** `stockfish/` folder (included or PATH)

---

## ✨ You're All Set!

Your Chess Analyser is ready to use. Enjoy playing!

**Questions?** Check FEATURES.md for detailed documentation.

