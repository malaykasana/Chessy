"""
CHESSY - Chess Game with Stockfish AI
A complete graphical chess game where you can play against Stockfish
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================

import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import tkinter.ttk as ttk
import chess
import chess.engine
import chess.pgn
import os
import sys
import threading
import json
from datetime import datetime


# =============================================================================
# SECTION 2: CONSTANTS AND CONFIGURATION
# =============================================================================

WINDOW_TITLE = "Chessy - Play Chess vs Stockfish"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SQUARE_SIZE = 72

# Unicode chess pieces
PIECES = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

# Color themes
THEMES = {
    'Classic': {
        'light': '#F0D9B5', 'dark': '#B58863', 'highlight': '#90EE90',
        'select': '#FFFF00', 'hint': '#87CEEB', 'last_move': '#CDD26A',
        'coord': '#000000', 'white_piece': '#FFFFFF', 'black_piece': '#000000',
        'bg': '#F5F5F5'
    },
    'Blue': {
        'light': '#DEE3E6', 'dark': '#8CA2AD', 'highlight': '#7FC97F',
        'select': '#FFD700', 'hint': '#87CEFA', 'last_move': '#FFD700',
        'coord': '#000000', 'white_piece': '#FFFFFF', 'black_piece': '#1A1A1A',
        'bg': '#F5F5F5'
    },
    'Green': {
        'light': '#FFFFDD', 'dark': '#86A666', 'highlight': '#B4D7A8',
        'select': '#FFA500', 'hint': '#87CEEB', 'last_move': '#FFA500',
        'coord': '#000000', 'white_piece': '#FFFFFF', 'black_piece': '#000000',
        'bg': '#F5F5F5'
    },
    'Dark': {
        'light': '#404040', 'dark': '#1A1A1A', 'highlight': '#505050',
        'select': '#FFD700', 'hint': '#4682B4', 'last_move': '#FFD700',
        'coord': '#FFFFFF', 'white_piece': '#E0E0E0', 'black_piece': '#303030',
        'bg': '#1F1F1F'
    }
}


# =============================================================================
# SECTION 3: MAIN CHESSY CLASS
# =============================================================================

class Chessy:
    """Main chess game application"""
    
    def __init__(self, root):
        """Initialize Chessy game"""
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(1100, 720)
        
        # Game state
        self.board = chess.Board()
        self.move_history = []
        self.engine = None
        self.engine_lock = threading.Lock()
        
        # UI state
        self.selected_square = None
        self.legal_moves_list = []
        self.last_move = None
        self.hint_move = None
        self.show_hint = False
        
        # Player settings
        self.player_color = chess.WHITE
        self.ai_difficulty = 1.0
        self.ai_thinking = False
        
        # Display settings
        self.current_theme = 'Classic'
        self.board_flipped = False
        
        # Analysis/Review state
        self.review_mode = False
        self.review_board = None
        self.review_moves = []
        self.review_index = 0
        self.analysis_cache = {}
        self.current_evaluation = 0.0
        
        # Settings storage
        self.settings_file = 'chess_settings.json'
        self.lichess_username = ""
        self.chesscom_username = ""
        
        # UI widgets
        self.canvas = None
        self.status_label = None
        self.move_list_text = None
        
        # Initialize
        self.load_settings()
        self.load_stockfish()
        self.create_ui()
        self.draw_board()
        
        print("✓ Chessy initialized")
    
    # =========================================================================
    # SECTION 4: SETTINGS MANAGEMENT
    # =========================================================================
    
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.lichess_username = settings.get('lichess_username', '')
                    self.chesscom_username = settings.get('chesscom_username', '')
                    self.current_theme = settings.get('theme', 'Classic')
                    self.ai_difficulty = float(settings.get('ai_difficulty', 1.0))
                    print(f"✓ Settings loaded")
        except Exception as e:
            print(f"⚠ Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            settings = {
                'lichess_username': self.lichess_username,
                'chesscom_username': self.chesscom_username,
                'theme': self.current_theme,
                'ai_difficulty': self.ai_difficulty
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            print(f"✓ Settings saved")
        except Exception as e:
            print(f"⚠ Error saving settings: {e}")
    
    # =========================================================================
    # SECTION 5: STOCKFISH ENGINE
    # =========================================================================
    
    def load_stockfish(self):
        """Load Stockfish chess engine"""
        paths = [
            os.path.join('stockfish', 'stockfish-windows-x86-64-avx2.exe'),
            os.path.join('stockfish', 'stockfish.exe'),
            'stockfish.exe',
            'stockfish',
            '/usr/bin/stockfish',
            '/usr/local/bin/stockfish',
        ]
        
        found = None
        for path in paths:
            if os.path.exists(path):
                found = path
                break
            elif path in ['stockfish', 'stockfish.exe']:
                found = path
                break
        
        if found:
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(found)
                print(f"✓ Stockfish loaded: {found}")
            except Exception as e:
                print(f"✗ Stockfish error: {e}")
                messagebox.showwarning("Stockfish Error", f"Could not load Stockfish:\n{e}")
        else:
            print("✗ Stockfish not found")
            messagebox.showinfo(
                "Stockfish Not Found",
                "Stockfish not detected.\nDownload from: https://stockfishchess.org/download/"
            )
    
    # =========================================================================
    # SECTION 6: UI CREATION
    # =========================================================================
    
    def create_ui(self):
        """Create all UI widgets"""
        theme = THEMES[self.current_theme]
        self.root.configure(bg=theme['bg'])
        
        # Main frame
        main = tk.Frame(self.root, bg=theme['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # LEFT SIDE: Board and controls
        left = tk.Frame(main, bg=theme['bg'])
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Canvas for board
        self.canvas = tk.Canvas(
            left, width=SQUARE_SIZE*8, height=SQUARE_SIZE*8,
            bg=theme['bg'], highlightthickness=0
        )
        self.canvas.pack(pady=(0, 10))
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Status label
        self.status_label = tk.Label(
            left, text="Welcome to Chessy!",
            font=("Arial", 11), bg=theme['bg'], fg="#333333"
        )
        self.status_label.pack(fill=tk.X, pady=(0, 10))
        
        # Control buttons
        btn_frame = tk.Frame(left, bg=theme['bg'])
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="New Game", command=self.new_game, width=14).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Undo", command=self.undo_move, width=14).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Hint", command=self.toggle_hint, width=14).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Flip Board", command=self.flip_board, width=14).pack(side=tk.LEFT, padx=2)
        
        # Analysis buttons
        analysis_frame = tk.Frame(left, bg=theme['bg'])
        analysis_frame.pack(fill=tk.X, pady=(5, 0))
        tk.Button(analysis_frame, text="Analyze", command=self.analyze_position, width=14).pack(side=tk.LEFT, padx=2)
        tk.Button(analysis_frame, text="Review Game", command=self.open_game_review, width=14).pack(side=tk.LEFT, padx=2)
        tk.Button(analysis_frame, text="Find Blunders", command=self.find_blunders, width=14).pack(side=tk.LEFT, padx=2)
        
        # RIGHT SIDE: Info panel
        right = tk.Frame(main, bg=theme['bg'])
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="Game Info", font=("Arial", 12, "bold"), bg=theme['bg']).pack(anchor="w", pady=(0, 5))
        
        # Move list
        move_frame = tk.Frame(right, bg=theme['bg'])
        move_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        tk.Label(move_frame, text="Moves:", font=("Arial", 10), bg=theme['bg']).pack(anchor="w")
        self.move_list_text = scrolledtext.ScrolledText(
            move_frame, width=30, height=15, font=("Courier", 9), bg="#FFFFFF"
        )
        self.move_list_text.pack(fill=tk.BOTH, expand=True)
        self.move_list_text.config(state=tk.DISABLED)
        
        # Settings panel
        settings = tk.LabelFrame(right, text="Settings", font=("Arial", 10, "bold"), bg=theme['bg'])
        settings.pack(fill=tk.X, pady=(0, 10))
        
        # Player color
        color_frame = tk.Frame(settings, bg=theme['bg'])
        color_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(color_frame, text="Play as:", bg=theme['bg']).pack(side=tk.LEFT)
        self.color_var = tk.StringVar(value="white")
        tk.Radiobutton(color_frame, text="White", variable=self.color_var, value="white",
                      command=self.on_color_change, bg=theme['bg']).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(color_frame, text="Black", variable=self.color_var, value="black",
                      command=self.on_color_change, bg=theme['bg']).pack(side=tk.LEFT, padx=10)
        
        # AI difficulty
        diff_frame = tk.Frame(settings, bg=theme['bg'])
        diff_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(diff_frame, text="AI Speed (sec):", bg=theme['bg']).pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value=str(self.ai_difficulty))
        tk.Spinbox(diff_frame, from_=0.1, to=10.0, increment=0.5,
                  textvariable=self.difficulty_var, width=8).pack(side=tk.LEFT, padx=10)
        
        # Theme selector
        theme_frame = tk.Frame(settings, bg=theme['bg'])
        theme_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(theme_frame, text="Theme:", bg=theme['bg']).pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_menu = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                 values=list(THEMES.keys()), state="readonly", width=15)
        theme_menu.pack(side=tk.LEFT, padx=10)
        theme_menu.bind("<<ComboboxSelected>>", lambda e: self.on_theme_change())
        
        # Action buttons
        action_frame = tk.Frame(settings, bg=theme['bg'])
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(action_frame, text="Save PGN", command=self.save_game, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(action_frame, text="Load PGN", command=self.load_game, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(action_frame, text="Accounts", command=self.open_accounts, width=12).pack(side=tk.LEFT, padx=2)
    
    # =========================================================================
    # SECTION 7: BOARD DRAWING
    # =========================================================================
    
    def draw_board(self):
        """Draw chess board with pieces"""
        if not self.canvas:
            return
        
        self.canvas.delete("all")
        theme = THEMES[self.current_theme]
        
        for rank in range(8):
            for file in range(8):
                x1 = file * SQUARE_SIZE
                y1 = rank * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                
                # Calculate square index
                square_idx = 8 * (7 - rank) + file
                
                # Determine color
                is_light = (rank + file) % 2 == 0
                color = theme['light'] if is_light else theme['dark']
                
                # Highlight selected square
                if self.selected_square == square_idx:
                    color = theme['select']
                # Highlight legal moves
                elif square_idx in self.legal_moves_list:
                    color = theme['highlight']
                # Highlight last move
                elif self.last_move and (square_idx == self.last_move.from_square or 
                                        square_idx == self.last_move.to_square):
                    color = theme['last_move']
                # Highlight hint
                elif self.show_hint and self.hint_move and (square_idx == self.hint_move.from_square or
                                                            square_idx == self.hint_move.to_square):
                    color = theme['hint']
                
                # Draw square
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                # Draw piece
                piece = self.board.piece_at(square_idx)
                if piece:
                    symbol = PIECES.get(str(piece), str(piece))
                    piece_color = theme['white_piece'] if piece.color else theme['black_piece']
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=symbol,
                                           font=("Arial", 48), fill=piece_color)
                
                # Draw coordinates
                if file == 0:
                    rank_text = str(8 - rank)
                    self.canvas.create_text(x1+2, y1+2, text=rank_text, font=("Arial", 8),
                                           fill=theme['coord'], anchor="nw")
                if rank == 7:
                    file_text = chr(97 + file)
                    self.canvas.create_text(x2-2, y2-2, text=file_text, font=("Arial", 8),
                                           fill=theme['coord'], anchor="se")
    
    # =========================================================================
    # SECTION 8: MOUSE INPUT
    # =========================================================================
    
    def on_click(self, event):
        """Handle board click"""
        file = event.x // SQUARE_SIZE
        rank = event.y // SQUARE_SIZE
        square = 8 * (7 - rank) + file
        
        if not 0 <= square < 64:
            return
        
        if self.selected_square is None:
            # Select piece
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.legal_moves_list = [m.to_square for m in self.board.legal_moves 
                                        if m.from_square == square]
                self.draw_board()
        else:
            if square == self.selected_square:
                # Deselect
                self.selected_square = None
                self.legal_moves_list = []
                self.draw_board()
            elif square in self.legal_moves_list:
                # Move piece
                move = chess.Move(self.selected_square, square)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.move_history.append(move)
                    self.last_move = move
                    self.selected_square = None
                    self.legal_moves_list = []
                    self.show_hint = False
                    self.hint_move = None
                    self.update_moves()
                    self.draw_board()
                    self.update_status()
                    
                    # AI move
                    if self.board.turn != self.player_color and not self.board.is_game_over():
                        threading.Thread(target=self.ai_move, daemon=True).start()
            else:
                # Select different piece
                piece = self.board.piece_at(square)
                if piece and piece.color == self.board.turn:
                    self.selected_square = square
                    self.legal_moves_list = [m.to_square for m in self.board.legal_moves
                                            if m.from_square == square]
                    self.draw_board()
    
    # =========================================================================
    # SECTION 9: AI MOVE
    # =========================================================================
    
    def ai_move(self):
        """Make AI move"""
        if not self.engine or self.board.is_game_over():
            return
        
        self.ai_thinking = True
        self.update_status()
        
        try:
            difficulty = float(self.difficulty_var.get())
            with self.engine_lock:
                result = self.engine.play(self.board, chess.engine.Limit(time=difficulty))
            
            if result.move:
                self.board.push(result.move)
                self.move_history.append(result.move)
                self.last_move = result.move
                self.update_moves()
                self.draw_board()
                self.update_status()
        except Exception as e:
            print(f"AI error: {e}")
        finally:
            self.ai_thinking = False
    
    # =========================================================================
    # SECTION 10: GAME CONTROL
    # =========================================================================
    
    def new_game(self):
        """Start new game"""
        self.board = chess.Board()
        self.move_history = []
        self.selected_square = None
        self.legal_moves_list = []
        self.last_move = None
        self.hint_move = None
        self.show_hint = False
        self.update_moves()
        self.draw_board()
        self.update_status()
    
    def undo_move(self):
        """Undo last move"""
        if not self.move_history:
            messagebox.showinfo("Undo", "No moves to undo!")
            return
        
        self.board.pop()
        self.move_history.pop()
        
        # Undo AI move too
        if self.board.turn != self.player_color and self.move_history:
            self.board.pop()
            self.move_history.pop()
        
        self.selected_square = None
        self.legal_moves_list = []
        self.last_move = None
        self.update_moves()
        self.draw_board()
        self.update_status()
    
    def toggle_hint(self):
        """Toggle hint display"""
        if not self.engine:
            messagebox.showwarning("Hint", "Stockfish not loaded!")
            return
        
        self.show_hint = not self.show_hint
        
        if self.show_hint:
            threading.Thread(target=self.calculate_hint, daemon=True).start()
        else:
            self.hint_move = None
            self.draw_board()
    
    def calculate_hint(self):
        """Calculate best move"""
        if not self.engine or self.board.is_game_over() or self.ai_thinking:
            return
        
        try:
            with self.engine_lock:
                result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            self.hint_move = result.move
            self.draw_board()
        except Exception as e:
            print(f"Hint error: {e}")
    
    def flip_board(self):
        """Flip board orientation"""
        self.board_flipped = not self.board_flipped
        self.draw_board()
    
    def on_color_change(self):
        """Handle color change"""
        self.player_color = chess.WHITE if self.color_var.get() == "white" else chess.BLACK
        self.new_game()
    
    def on_theme_change(self):
        """Handle theme change"""
        new_theme = self.theme_var.get()
        if new_theme in THEMES:
            self.current_theme = new_theme
            self.save_settings()
            # Recreate UI with new theme
            for widget in self.root.winfo_children():
                widget.destroy()
            self.create_ui()
            self.draw_board()
    
    def update_status(self):
        """Update status bar"""
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            self.status_label.config(text=f"Checkmate! {winner} wins!")
        elif self.board.is_stalemate():
            self.status_label.config(text="Stalemate! Draw.")
        elif self.board.is_check():
            color = "White" if self.board.turn else "Black"
            self.status_label.config(text=f"Check! {color} to move.")
        elif self.ai_thinking:
            self.status_label.config(text="Stockfish thinking...")
        else:
            color = "White" if self.board.turn else "Black"
            self.status_label.config(text=f"{color} to move")
    
    def update_moves(self):
        """Update move list display"""
        self.move_list_text.config(state=tk.NORMAL)
        self.move_list_text.delete(1.0, tk.END)
        
        board_copy = chess.Board()
        moves_san = []
        for move in self.move_history:
            moves_san.append(board_copy.san(move))
            board_copy.push(move)
        
        text = ""
        for i, move in enumerate(moves_san):
            if i % 2 == 0:
                text += f"{i//2 + 1}. {move} "
            else:
                text += f"{move}\n"
        
        self.move_list_text.insert(tk.END, text if text else "(No moves)")
        self.move_list_text.config(state=tk.DISABLED)
    
    # =========================================================================
    # SECTION 11: PGN OPERATIONS
    # =========================================================================
    
    def save_game(self):
        """Save game to PGN"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pgn",
            filetypes=[("PGN files", "*.pgn"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                game = chess.pgn.Game()
                game.headers["Event"] = "Chessy Game"
                game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
                game.headers["White"] = "You" if self.player_color == chess.WHITE else "Stockfish"
                game.headers["Black"] = "Stockfish" if self.player_color == chess.WHITE else "You"
                
                node = game
                for move in self.move_history:
                    node = node.add_variation(move)
                
                with open(filename, 'w') as f:
                    f.write(str(game))
                
                messagebox.showinfo("Success", f"Game saved!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save: {e}")
    
    def load_game(self):
        """Load game from PGN"""
        filename = filedialog.askopenfilename(
            filetypes=[("PGN files", "*.pgn"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    game = chess.pgn.read_game(f)
                
                if game:
                    self.board = chess.Board()
                    self.move_history = []
                    for move in game.mainline_moves():
                        self.board.push(move)
                        self.move_history.append(move)
                    
                    self.selected_square = None
                    self.legal_moves_list = []
                    self.last_move = self.move_history[-1] if self.move_history else None
                    self.update_moves()
                    self.draw_board()
                    self.update_status()
                    messagebox.showinfo("Success", "Game loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load: {e}")
    
    # =========================================================================
    # SECTION 12: DIALOGS
    # =========================================================================
    
    def open_accounts(self):
        """Open accounts dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Accounts")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text="Lichess:", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor="w")
        lichess_entry = tk.Entry(dialog, font=("Arial", 10), width=40)
        lichess_entry.pack(pady=(0, 10), padx=10)
        lichess_entry.insert(0, self.lichess_username)
        
        tk.Label(dialog, text="Chess.com:", font=("Arial", 10)).pack(pady=(0, 0), padx=10, anchor="w")
        chesscom_entry = tk.Entry(dialog, font=("Arial", 10), width=40)
        chesscom_entry.pack(pady=(0, 20), padx=10)
        chesscom_entry.insert(0, self.chesscom_username)
        
        def save():
            self.lichess_username = lichess_entry.get()
            self.chesscom_username = chesscom_entry.get()
            self.save_settings()
            messagebox.showinfo("Success", "Accounts saved!")
            dialog.destroy()
        
        tk.Button(dialog, text="Save", command=save, width=40).pack(pady=10)
    
    # =========================================================================
    # SECTION 13: GAME ANALYSIS AND REVIEW
    # =========================================================================
    
    def open_game_review(self):
        """Open game review window for analysis"""
        if not self.move_history:
            messagebox.showinfo("Review", "Play a game first before reviewing!")
            return
        
        review_win = tk.Toplevel(self.root)
        review_win.title("Game Review - Chessy")
        review_win.geometry("700x600")
        
        # Title
        tk.Label(review_win, text="Game Analysis", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Analysis info
        info_frame = tk.Frame(review_win)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(info_frame, text=f"Total Moves: {len(self.move_history)}", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Label(info_frame, text=f"Evaluation: {self.current_evaluation:+.1f}", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # Move list with analysis
        frame = tk.Frame(review_win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="Moves (click to review):", font=("Arial", 10, "bold")).pack(anchor="w")
        
        text = scrolledtext.ScrolledText(frame, width=80, height=25, font=("Courier", 9))
        text.pack(fill=tk.BOTH, expand=True)
        
        # Generate analysis text
        analysis_text = self.generate_game_analysis()
        text.insert(tk.END, analysis_text)
        text.config(state=tk.DISABLED)
    
    def generate_game_analysis(self):
        """Generate analysis of the current game"""
        if not self.move_history:
            return "No moves to analyze."
        
        analysis = "GAME ANALYSIS\n"
        analysis += "=" * 60 + "\n\n"
        
        board = chess.Board()
        for i, move in enumerate(self.move_history):
            move_num = i // 2 + 1
            is_white = i % 2 == 0
            
            move_san = board.san(move)
            
            # Try to evaluate position
            eval_str = ""
            try:
                if self.engine and i % 2 == 1:  # Analyze after each pair
                    with self.engine_lock:
                        result = self.engine.analyse(board, chess.engine.Limit(time=0.1))
                    if result and "score" in result:
                        score = result["score"]
                        eval_str = f" [Eval: {str(score)}]"
            except:
                eval_str = ""
            
            color = "White" if is_white else "Black"
            analysis += f"{move_num}. {move_san:6} ({color}){eval_str}\n"
            
            board.push(move)
        
        # Game result
        analysis += "\n" + "=" * 60 + "\n"
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            analysis += f"Result: {winner} wins by checkmate\n"
        elif self.board.is_stalemate():
            analysis += "Result: Draw (Stalemate)\n"
        elif self.board.is_insufficient_material():
            analysis += "Result: Draw (Insufficient Material)\n"
        else:
            analysis += "Result: Game not finished\n"
        
        return analysis
    
    def analyze_position(self):
        """Analyze current position with Stockfish"""
        if not self.engine:
            messagebox.showwarning("Engine", "Stockfish not loaded!")
            return
        
        try:
            with self.engine_lock:
                result = self.engine.analyse(self.board, chess.engine.Limit(time=1.0))
            
            if result and "score" in result:
                score = result["score"]
                self.current_evaluation = float(score.relative.cp) / 100.0 if score.relative.cp else 0.0
                
                analysis_win = tk.Toplevel(self.root)
                analysis_win.title("Position Analysis")
                analysis_win.geometry("400x250")
                
                tk.Label(analysis_win, text="Position Evaluation", font=("Arial", 12, "bold")).pack(pady=10)
                
                eval_text = f"Current Evaluation: {str(score)}"
                if score.relative.cp:
                    eval_num = score.relative.cp / 100.0
                    if eval_num > 0:
                        eval_text += f"\nWhite advantage: {eval_num:+.1f}"
                    else:
                        eval_text += f"\nBlack advantage: {-eval_num:+.1f}"
                
                tk.Label(analysis_win, text=eval_text, font=("Arial", 11)).pack(pady=10)
                
                if "pv" in result:
                    pv_moves = result["pv"]
                    pv_text = "Best continuation:\n"
                    board_copy = self.board.copy()
                    for move in pv_moves[:5]:
                        pv_text += f"{board_copy.san(move)} "
                        board_copy.push(move)
                    
                    tk.Label(analysis_win, text=pv_text, font=("Courier", 9), wraplength=350).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error analyzing position: {e}")
    
    def find_blunders(self):
        """Analyze game to find blunders"""
        if not self.move_history or not self.engine:
            messagebox.showinfo("Blunder Check", "Play a game with Stockfish first!")
            return
        
        blunder_win = tk.Toplevel(self.root)
        blunder_win.title("Blunder Analysis")
        blunder_win.geometry("600x500")
        
        tk.Label(blunder_win, text="Analyzing for blunders...", font=("Arial", 11)).pack(pady=10)
        blunder_win.update()
        
        blunders = []
        board = chess.Board()
        
        for i, move in enumerate(self.move_history):
            try:
                # Evaluate before move
                with self.engine_lock:
                    result_before = self.engine.analyse(board, chess.engine.Limit(time=0.2))
                
                board.push(move)
                
                # Evaluate after move
                with self.engine_lock:
                    result_after = self.engine.analyse(board, chess.engine.Limit(time=0.2))
                
                if result_before and result_after and "score" in result_before and "score" in result_after:
                    score_before = result_before["score"].relative.cp or 0
                    score_after = result_after["score"].relative.cp or 0
                    
                    eval_loss = (score_before - score_after) / 100.0
                    
                    if eval_loss > 0.5:  # Significant loss
                        move_num = i // 2 + 1
                        color = "White" if i % 2 == 0 else "Black"
                        blunders.append({
                            "move": board.san(move),
                            "color": color,
                            "num": move_num,
                            "loss": eval_loss
                        })
            except:
                pass
        
        # Display results
        blunder_win.winfo_children()[0].destroy()
        
        if blunders:
            text = scrolledtext.ScrolledText(blunder_win, width=70, height=25, font=("Courier", 9))
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text.insert(tk.END, f"Found {len(blunders)} questionable move(s):\n\n")
            for blunder in sorted(blunders, key=lambda x: x["loss"], reverse=True):
                text.insert(tk.END, f"Move {blunder['num']}. {blunder['move']} ({blunder['color']})\n")
                text.insert(tk.END, f"   Evaluation loss: -{blunder['loss']:.1f}\n\n")
            
            text.config(state=tk.DISABLED)
        else:
            tk.Label(blunder_win, text="No significant blunders found!", font=("Arial", 11)).pack(pady=20)


# =============================================================================
# SECTION 13: MAIN ENTRY POINT
# =============================================================================

def main():
    """Start Chessy application"""
    root = tk.Tk()
    app = Chessy(root)
    root.mainloop()
    
    # Cleanup
    if app.engine:
        try:
            app.engine.quit()
        except:
            pass


if __name__ == "__main__":
    main()
