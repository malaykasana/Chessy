"""
Chess Analyser using tkinter
A graphical chess game where you can play against Stockfish AI
Features: Hints, Game Review, Lichess/Chess.com Integration
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog, scrolledtext, simpledialog
import chess
import chess.engine
import chess.pgn
import os
import sys
import threading
import requests
import json
from datetime import datetime
from io import StringIO


class ChessAnalyser:
    # Unicode chess pieces - Multiple styles
    PIECE_SETS = {
        'Classic': {
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
        },
        'Bold': {
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
        },
        'Text': {
            'P': 'P', 'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K',
            'p': 'p', 'r': 'r', 'n': 'n', 'b': 'b', 'q': 'q', 'k': 'k'
        }
    }
    
    PIECES = PIECE_SETS['Classic']  # Default
    
    # Board themes
    THEMES = {
        'Classic': {
            'light': '#F0D9B5',
            'dark': '#B58863',
            'highlight': '#90EE90',
            'select': '#FFFF00',
            'hint': '#87CEEB',
            'border': '#8B4513',
            'coord': '#000000',
            'white_piece': '#FFFFFF',
            'black_piece': '#000000'
        },
        'Chesscom': {
            'light': '#EAEED2',
            'dark': '#769656',
            'highlight': '#BACA44',
            'select': '#F7C631',
            'hint': '#88C0D0',
            'border': '#5A6E4B',
            'coord': '#2E3440',
            'white_piece': '#ECEFF4',
            'black_piece': '#2E3440'
        },
        'Slate Dark': {
            'light': '#3B4252',
            'dark': '#2E3440',
            'highlight': '#A3BE8C',
            'select': '#EBCB8B',
            'hint': '#88C0D0',
            'border': '#434C5E',
            'coord': '#D8DEE9',
            'white_piece': '#E5E9F0',
            'black_piece': '#D8DEE9'
        },
        'Blue': {
            'light': '#DEE3E6',
            'dark': '#8CA2AD',
            'highlight': '#7FC97F',
            'select': '#FFD700',
            'hint': '#87CEFA',
            'border': '#4682B4',
            'coord': '#000000',
            'white_piece': '#FFFFFF',
            'black_piece': '#1A1A1A'
        },
        'Green': {
            'light': '#FFFFDD',
            'dark': '#86A666',
            'highlight': '#B4D7A8',
            'select': '#FFA500',
            'hint': '#87CEEB',
            'border': '#2F4F2F',
            'coord': '#000000',
            'white_piece': '#FFFFFF',
            'black_piece': '#000000'
        },
        'Purple': {
            'light': '#E8D0E8',
            'dark': '#9370DB',
            'highlight': '#DDA0DD',
            'select': '#FFD700',
            'hint': '#B0E0E6',
            'border': '#4B0082',
            'coord': '#000000',
            'white_piece': '#FFFFFF',
            'black_piece': '#2F2F2F'
        },
        'Modern': {
            'light': '#EBECD0',
            'dark': '#739552',
            'highlight': '#B4C7A8',
            'select': '#F7C631',
            'hint': '#88C0D0',
            'border': '#5A6E4B',
            'coord': '#2E3440',
            'white_piece': '#ECEFF4',
            'black_piece': '#2E3440'
        },
        'Dark': {
            'light': '#404040',
            'dark': '#1A1A1A',
            'highlight': '#505050',
            'select': '#FFD700',
            'hint': '#4682B4',
            'border': '#000000',
            'coord': '#FFFFFF',
            'white_piece': '#E0E0E0',
            'black_piece': '#303030'
        }
    }
    
    # Last move highlight color
    LAST_MOVE_COLOR = "#CDD26A"  # Yellow-green for last move
    
    SQUARE_SIZE = 72
    
    # Opening book - maps move sequences to opening names
    OPENING_BOOK = {
        "e2e4": "King's Pawn Opening",
        "e2e4 e7e5": "Open Game",
        "e2e4 e7e5 g1f3 b8c6 f1b5": "Ruy Lopez",
        "e2e4 e7e5 g1f3 b8c6 f1c4": "Italian Game",
        "e2e4 e7e5 g1f3 b8c6 d2d4": "Scotch Game",
        "e2e4 e7e5 g1f3 f7f6": "Damiano Defense",
        "e2e4 e7e5 f1c4 g8f6": "Two Knights Defense",
        "e2e4 c7c5": "Sicilian Defense",
        "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4": "Sicilian: Open",
        "e2e4 c7c5 c2c3": "Sicilian: Alapin",
        "e2e4 c7c5 b1c3": "Sicilian: Closed",
        "e2e4 c7c6": "Caro-Kann Defense",
        "e2e4 e7e6": "French Defense",
        "e2e4 d7d5": "Scandinavian Defense",
        "e2e4 g8f6": "Alekhine's Defense",
        "e2e4 b8c6": "Nimzowitsch Defense",
        "d2d4": "Queen's Pawn Opening",
        "d2d4 d7d5": "Closed Game",
        "d2d4 d7d5 c2c4": "Queen's Gambit",
        "d2d4 d7d5 c2c4 d5c4": "Queen's Gambit Accepted",
        "d2d4 d7d5 c2c4 e7e6": "Queen's Gambit Declined",
        "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4": "Nimzo-Indian Defense",
        "d2d4 g8f6 c2c4 g7g6": "King's Indian Defense",
        "d2d4 g8f6 c2c4 e7e6": "Indian Defense",
        "d2d4 g8f6": "Indian Game",
        "d2d4 f7f5": "Dutch Defense",
        "c2c4": "English Opening",
        "c2c4 e7e5": "English: Reversed Sicilian",
        "c2c4 g8f6": "English: Anglo-Indian",
        "g1f3": "RÃ©ti Opening",
        "g1f3 d7d5 c2c4": "RÃ©ti: Anglo-Slav",
        "g1f3 g8f6 c2c4": "English via RÃ©ti",
        "b2b3": "Larsen's Opening",
        "f2f4": "Bird's Opening",
        "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6": "Ruy Lopez: Morphy Defense",
        "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6": "Ruy Lopez: Berlin Defense",
        "e2e4 c7c5 g1f3 d7d6 d2d4": "Sicilian: Open Variation",
        "e2e4 c7c5 g1f3 b8c6": "Sicilian: Old Sicilian",
        "d2d4 d7d5 c2c4 c7c6": "Slav Defense",
        "d2d4 g8f6 c2c4 c7c5": "Benoni Defense"
    }
    
    def __init__(self, root, stockfish_path=None):
        self.root = root
        self.root.title("Chess Analyser - Play vs Stockfish")
        self.root.geometry("1280x720")  # Optimized window size for 16:9 layouts
        self.root.minsize(1100, 720)
        self.root.resizable(False, False)

        self.board = chess.Board()
        self.selected_square = None
        self.legal_moves = []
        self.engine = None
        self.player_color = chess.WHITE
        self.ai_thinking = False
        self.hint_move = None
        self.show_hint = False
        self.move_history = []
        self.current_theme = 'Classic'
        self.last_move = None  # Track last move for highlighting
        self.piece_style = 'Classic'  # Track piece style
        self.piece_size = int(self.SQUARE_SIZE * 0.68)  # Default piece font size aligned with board size
        self.board_flipped = False  # Track board orientation
        self.REVIEW_SQUARE_SIZE = 56  # Dedicated square size for review board canvas

        # Captured pieces tracking
        self.captured_white = []
        self.captured_black = []

        # Opening tracking
        self.current_opening = ""

        # Timer tracking
        self.white_time = 0  # seconds
        self.black_time = 0  # seconds
        self.move_start_time = None
        self.timer_running = False

        # Analysis/Review mode
        self.review_mode = False
        self.review_board = None
        self.review_move_index = 0
        self.review_moves = []
        self.current_evaluation = 0.0
        self.inline_review_games = []
        self.top_move_arrows = []
        # Review engine caching
        self.review_analysis_cache = {}
        self._review_cache_order = []
        self._review_cache_max = 300
        self.review_ply_sans = []
        self.review_pair_rows = []
        self.review_window = None
        self.review_browser_window = None
        self._updating_review_slider = False
        self.review_engine_token = 0
        self.review_engine_busy = False
        self.review_analysis_text = None
        self.review_eval_value_label = None
        self.review_engine_info_var = None
        self.review_move_label = None
        self.review_slider = None
        self.review_move_table = None
        self.review_row_ids = []
        # Review performance controls
        self._review_after_id = None
        self._review_debounce_ms = 160
        self._review_slider_dragging = False

        # Account settings
        self.lichess_username = ""
        self.chesscom_username = ""
        self.settings_file = "chess_settings.json"

        # Engine settings
        self.skill_level = 20  # Maximum by default
        self.multipv_count = 3  # Show top 3 moves

        # Engine coordination lock
        self.engine_lock = threading.Lock()

        # Live evaluation controls (performance)
        self._eval_after_id = None
        self._last_eval_ms = 0
        self._eval_interval_ms = 400  # Minimum interval between eval requests
        self.live_eval_var = tk.BooleanVar(value=True)
        self.eval_pause_on_ai = tk.BooleanVar(value=True)

        # Animation settings
        self.enable_animations = tk.BooleanVar(value=True)
        self._anim_item = None
        self._anim_running = False

        self.load_settings()

        # Try to load Stockfish
        self.load_stockfish(stockfish_path)

        # Create UI
        self.create_widgets()
        self.draw_board()
    
    def load_settings(self):
        """Load user settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.lichess_username = settings.get('lichess_username', '')
                    self.chesscom_username = settings.get('chesscom_username', '')
                    self.skill_level = settings.get('skill_level', 20)
                    self.multipv_count = settings.get('multipv_count', 3)
                    self.current_theme = settings.get('theme', 'Classic')
                    self.piece_style = settings.get('piece_style', 'Classic')
                    self.piece_size = settings.get('piece_size', 52)
        except Exception as e:
            print(f"Could not load settings: {e}")
    
    def save_settings(self):
        """Save user settings to file."""
        try:
            settings = {
                'lichess_username': self.lichess_username,
                'chesscom_username': self.chesscom_username,
                'theme': self.current_theme,
                'piece_style': self.piece_style,
                'piece_size': self.piece_size,
                'skill_level': self.skill_level,
                'multipv_count': self.multipv_count
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
        
    def load_stockfish(self, stockfish_path):
        """Try to load Stockfish engine."""
        engine_path = None
        # 1) Explicit path provided
        if stockfish_path and os.path.exists(stockfish_path):
            engine_path = stockfish_path
        # 2) PyInstaller bundle (sys._MEIPASS) or next to executable
        if not engine_path:
            bundle_dir = getattr(sys, "_MEIPASS", None)
            if bundle_dir:
                candidate = os.path.join(bundle_dir, "stockfish", "stockfish-windows-x86-64-avx2.exe")
                if os.path.exists(candidate):
                    engine_path = candidate
            else:
                # If frozen, look next to the EXE
                if getattr(sys, 'frozen', False):
                    exe_dir = os.path.dirname(sys.executable)
                    candidate = os.path.join(exe_dir, "stockfish", "stockfish-windows-x86-64-avx2.exe")
                    if os.path.exists(candidate):
                        engine_path = candidate
        # 3) Project and PATH fallbacks
        if not engine_path:
            possible_paths = [
                os.path.join("stockfish", "stockfish-windows-x86-64-avx2.exe"),
                os.path.join("stockfish", "stockfish.exe"),
                "stockfish.exe",
                "stockfish",
                "/usr/bin/stockfish",
                "/usr/local/bin/stockfish",
                r"C:\\Program Files\\Stockfish\\stockfish.exe",
                r"C:\\Stockfish\\stockfish.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    engine_path = path
                    break
                elif path in ["stockfish", "stockfish.exe"]:
                    engine_path = path
                    break
        
        if engine_path:
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
                print(f"Stockfish loaded: {engine_path}")
            except Exception as e:
                print(f"Could not load Stockfish: {e}")
                messagebox.showwarning(
                    "Stockfish Not Found",
                    "Stockfish engine not found!\n\n"
                    "Download from: https://stockfishchess.org/download/\n"
                    "You can still play, but there will be no AI opponent."
                )
        else:
            messagebox.showinfo(
                "Stockfish Not Found",
                "Stockfish engine not detected.\n\n"
                "Download from: https://stockfishchess.org/download/"
            )
    
    def toggle_hint(self):
        """Toggle hint display."""
        if not self.engine:
            messagebox.showwarning("No Engine", "Stockfish engine is required for hints!")
            return
        
        if self.ai_thinking:
            return
        
        self.show_hint = not self.show_hint
        
        if self.show_hint:
            # Calculate hint in background
            threading.Thread(target=self.calculate_hint, daemon=True).start()
        else:
            self.hint_move = None
            self.draw_board()
    
    def calculate_hint(self):
        """Calculate the best move as a hint."""
        if not self.engine:
            return
        if self.review_mode or self.ai_thinking:
            return

        try:
            with self.engine_lock:
                result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            self.hint_move = result.move if result else None
            self.root.after(0, self.draw_board)
        except Exception as e:
            print(f"Error calculating hint: {e}")
    
    def save_game(self):
        """Save current game to PGN file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pgn",
            filetypes=[("PGN files", "*.pgn"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                game = chess.pgn.Game()
                game.headers["Event"] = "Casual Game"
                game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
                game.headers["White"] = "Player" if self.player_color == chess.WHITE else "Stockfish"
                game.headers["Black"] = "Stockfish" if self.player_color == chess.WHITE else "Player"
                
                node = game
                board = chess.Board()
                for move in self.move_history:
                    node = node.add_variation(move)
                
                with open(filename, 'w') as f:
                    f.write(str(game))
                
                messagebox.showinfo("Success", f"Game saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save game: {e}")
    
    def load_game(self):
        """Load game from PGN file."""
        filename = filedialog.askopenfilename(
            filetypes=[("PGN files", "*.pgn"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    game = chess.pgn.read_game(f)
                
                if game:
                    # Enter review mode
                    self.review_mode = True
                    self.review_board = chess.Board()
                    self.review_moves = list(game.mainline_moves())
                    self.review_move_index = 0
                    
                    # Show review window
                    self.open_review_window()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Could not load game: {e}")
    
    def create_widgets(self):
        """Build the main UI layout with a board, sidebar, and control tray."""
        self.root.geometry("1280x720")
        self.root.minsize(1100, 720)
        self.root.configure(bg="#F5F5F5")

        content_frame = tk.Frame(self.root, bg="#F5F5F5")
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=16, pady=(16, 8))

        # Left column: board, evaluation bar, status, timers, captured pieces
        left_column = tk.Frame(content_frame, bg="#F5F5F5")
        left_column.pack(side=tk.LEFT, fill=tk.Y)

        board_wrapper = tk.Frame(left_column, bg="#F5F5F5")
        board_wrapper.pack()

        self.canvas = tk.Canvas(
            board_wrapper,
            width=self.SQUARE_SIZE * 8,
            height=self.SQUARE_SIZE * 8,
            highlightthickness=0,
            bg="#F5F5F5",
        )
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.on_square_click)

        eval_frame = tk.Frame(board_wrapper, bg="#F5F5F5")
        eval_frame.pack(side=tk.LEFT, padx=(12, 0), fill=tk.Y)

        self.eval_canvas = tk.Canvas(
            eval_frame,
            width=40,
            height=self.SQUARE_SIZE * 8,
            highlightthickness=0,
            bg="#F5F5F5",
        )
        self.eval_canvas.pack()
        self.eval_label = tk.Label(
            eval_frame,
            text="+0.0",
            font=("Segoe UI", 12, "bold"),
            bg="#F5F5F5",
            fg="#333333",
        )
        self.eval_label.pack(pady=(8, 0))

        status_frame = tk.Frame(left_column, bg="#F5F5F5")
        status_frame.pack(fill=tk.X, pady=(12, 0))
        self.status_label = tk.Label(
            status_frame,
            text="Welcome to Chess!",
            font=("Segoe UI", 12),
            bg="#F5F5F5",
            fg="#333333",
        )
        self.status_label.pack(anchor="w")

        timer_frame = tk.Frame(left_column, bg="#F5F5F5")
        timer_frame.pack(fill=tk.X, pady=(4, 0))
        self.white_timer_label = tk.Label(
            timer_frame,
            text="Time 0:00",
            font=("Segoe UI", 10, "bold"),
            bg="#F5F5F5",
            fg="#1F1F1F",
        )
        self.white_timer_label.pack(anchor="w")
        self.black_timer_label = tk.Label(
            timer_frame,
            text="Time 0:00",
            font=("Segoe UI", 10, "bold"),
            bg="#F5F5F5",
            fg="#1F1F1F",
        )
        self.black_timer_label.pack(anchor="w")

        captured_frame = tk.Frame(left_column, bg="#F5F5F5")
        captured_frame.pack(fill=tk.X, pady=(10, 0))

        white_capture = tk.Frame(captured_frame, bg="#F5F5F5")
        white_capture.pack(fill=tk.X)
        tk.Label(
            white_capture,
            text="White captures:",
            font=("Segoe UI", 10, "bold"),
            bg="#F5F5F5",
            fg="#555555",
        ).pack(side=tk.LEFT)
        self.captured_white_label = tk.Label(
            white_capture,
            text="",
            font=("Segoe UI", 16),
            bg="#F5F5F5",
        )
        self.captured_white_label.pack(side=tk.LEFT, padx=(8, 0))
        self.material_label_white = tk.Label(
            white_capture,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="#F5F5F5",
            fg="green",
        )
        self.material_label_white.pack(side=tk.LEFT, padx=(6, 0))

        black_capture = tk.Frame(captured_frame, bg="#F5F5F5")
        black_capture.pack(fill=tk.X, pady=(4, 0))
        tk.Label(
            black_capture,
            text="Black captures:",
            font=("Segoe UI", 10, "bold"),
            bg="#F5F5F5",
            fg="#555555",
        ).pack(side=tk.LEFT)
        self.captured_black_label = tk.Label(
            black_capture,
            text="",
            font=("Segoe UI", 16),
            bg="#F5F5F5",
        )
        self.captured_black_label.pack(side=tk.LEFT, padx=(8, 0))
        self.material_label_black = tk.Label(
            black_capture,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="#F5F5F5",
            fg="green",
        )
        self.material_label_black.pack(side=tk.LEFT, padx=(6, 0))

        quick_actions = tk.Frame(left_column, bg="#F5F5F5")
        quick_actions.pack(fill=tk.X, pady=(10, 0))
        tk.Button(
            quick_actions,
            text="Flip Board",
            command=self.flip_board,
            font=("Segoe UI", 10),
            width=12,
            relief=tk.GROOVE,
            bg="#FFFFFF",
            activebackground="#E0E0E0",
        ).pack(side=tk.LEFT, padx=(0, 8))

        # Right column: game info and review hub
        sidebar_container = tk.Frame(content_frame, bg="#F5F5F5")
        sidebar_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))

        sidebar_notebook = ttk.Notebook(sidebar_container)
        sidebar_notebook.pack(fill=tk.BOTH, expand=True)

        # --- Game info tab ---
        game_tab = tk.Frame(sidebar_notebook, bg="#FFFFFF")
        sidebar_notebook.add(game_tab, text="Game Info")

        tk.Label(
            game_tab,
            text="Game Details",
            font=("Segoe UI", 13, "bold"),
            bg="#FFFFFF",
            fg="#1F1F1F",
        ).pack(anchor="w")

        move_list_frame = tk.Frame(game_tab, bg="#FFFFFF")
        move_list_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 12))
        self.move_list_text = scrolledtext.ScrolledText(
            move_list_frame,
            width=34,
            height=18,
            font=("Consolas", 11),
            bg="#F8F9FA",
            relief=tk.FLAT,
            borderwidth=0,
        )
        self.move_list_text.pack(fill=tk.BOTH, expand=True)
        self.move_list_text.config(state=tk.DISABLED)

        options_frame = tk.LabelFrame(
            game_tab,
            text="Display Options",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#1F1F1F",
            labelanchor="n",
            relief=tk.GROOVE,
        )
        options_frame.pack(fill=tk.X, pady=(0, 12))
        self.show_top_moves_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Show engine arrows in review mode",
            variable=self.show_top_moves_var,
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            anchor="w",
        ).pack(fill=tk.X, padx=8, pady=4)

        tk.Checkbutton(
            options_frame,
            text="Live evaluation during play",
            variable=self.live_eval_var,
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            anchor="w",
        ).pack(fill=tk.X, padx=8, pady=4)

        tk.Checkbutton(
            options_frame,
            text="Pause evaluation on AI turn",
            variable=self.eval_pause_on_ai,
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            anchor="w",
        ).pack(fill=tk.X, padx=8, pady=4)

        tk.Checkbutton(
            options_frame,
            text="Enable move animations",
            variable=self.enable_animations,
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            anchor="w",
        ).pack(fill=tk.X, padx=8, pady=4)

        engine_info_frame = tk.Frame(game_tab, bg="#FFFFFF")
        engine_info_frame.pack(fill=tk.X)
        tk.Label(
            engine_info_frame,
            text="Engine Skill:",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#555555",
        ).grid(row=0, column=0, sticky="w")
        self.engine_skill_value = tk.Label(
            engine_info_frame,
            text=str(self.skill_level),
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#1F1F1F",
        )
        self.engine_skill_value.grid(row=0, column=1, sticky="w", padx=(6, 0))
        tk.Label(
            engine_info_frame,
            text="MultiPV:",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#555555",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.engine_multipv_value = tk.Label(
            engine_info_frame,
            text=str(self.multipv_count),
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#1F1F1F",
        )
        self.engine_multipv_value.grid(row=1, column=1, sticky="w", padx=(6, 0), pady=(4, 0))

        for widget in engine_info_frame.grid_slaves():
            widget.grid_configure(padx=2, pady=2)

        # --- Review hub tab ---
        review_tab = tk.Frame(sidebar_notebook, bg="#FFFFFF")
        sidebar_notebook.add(review_tab, text="Review Hub")

        tk.Label(
            review_tab,
            text="Chess.com & Lichess Review",
            font=("Segoe UI", 13, "bold"),
            bg="#FFFFFF",
            fg="#1F1F1F",
        ).pack(anchor="w", pady=(0, 4))

        entry_frame = tk.Frame(review_tab, bg="#FFFFFF")
        entry_frame.pack(fill=tk.X, pady=(4, 6))

        self.review_lichess_var = tk.StringVar(value=self.lichess_username)
        self.review_chesscom_var = tk.StringVar(value=self.chesscom_username)

        tk.Label(entry_frame, text="Lichess:", font=("Segoe UI", 10), bg="#FFFFFF", fg="#555555").grid(row=0, column=0, sticky="w")
        lichess_entry = ttk.Entry(entry_frame, textvariable=self.review_lichess_var, width=22)
        lichess_entry.grid(row=0, column=1, padx=(6, 12))
        ttk.Button(entry_frame, text="Fetch", command=lambda: self.inline_fetch_games("lichess"), width=10).grid(row=0, column=2)

        tk.Label(entry_frame, text="Chess.com:", font=("Segoe UI", 10), bg="#FFFFFF", fg="#555555").grid(row=1, column=0, sticky="w", pady=(6, 0))
        chess_entry = ttk.Entry(entry_frame, textvariable=self.review_chesscom_var, width=22)
        chess_entry.grid(row=1, column=1, padx=(6, 12), pady=(6, 0))
        ttk.Button(entry_frame, text="Fetch", command=lambda: self.inline_fetch_games("chesscom"), width=10).grid(row=1, column=2, pady=(6, 0))

        for widget in entry_frame.grid_slaves():
            widget.grid_configure(padx=2)

        self.review_status_label = tk.Label(
            review_tab,
            text="Choose a platform to pull your recent games.",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#666666",
        )
        self.review_status_label.pack(fill=tk.X, pady=(0, 6))

        tree_frame = tk.Frame(review_tab, bg="#FFFFFF")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("platform", "players", "result", "date")
        self.review_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        self.review_tree.heading("platform", text="Platform")
        self.review_tree.heading("players", text="Players")
        self.review_tree.heading("result", text="Result")
        self.review_tree.heading("date", text="Date")
        self.review_tree.column("platform", width=90, anchor="center")
        self.review_tree.column("players", width=200, anchor="w")
        self.review_tree.column("result", width=100, anchor="center")
        self.review_tree.column("date", width=120, anchor="center")

        review_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.review_tree.yview)
        self.review_tree.configure(yscrollcommand=review_scroll.set)
        self.review_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        review_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.review_tree.bind("<Double-1>", lambda _e: self.load_selected_inline_review_game())

        review_buttons = tk.Frame(review_tab, bg="#FFFFFF")
        review_buttons.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(review_buttons, text="Load Selected", command=self.load_selected_inline_review_game, width=16).pack(side=tk.LEFT, padx=4)
        ttk.Button(review_buttons, text="Open Review Browser", command=self.open_review_menu, width=20).pack(side=tk.LEFT, padx=4)
        ttk.Button(review_buttons, text="Import PGN", command=self.load_game, width=14).pack(side=tk.LEFT, padx=4)

        # Bottom control tray spanning full width
        bottom_frame = tk.Frame(self.root, bg="#F5F5F5")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=(0, 16))

        settings_frame = tk.Frame(bottom_frame, bg="#F5F5F5")
        settings_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            settings_frame,
            text="Play as:",
            font=("Segoe UI", 10),
            bg="#F5F5F5",
        ).pack(side=tk.LEFT, padx=5)
        self.color_var = tk.StringVar(value="white")
        tk.Radiobutton(
            settings_frame,
            text="White",
            variable=self.color_var,
            value="white",
            command=self.change_player_color,
            font=("Segoe UI", 10),
            bg="#F5F5F5",
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            settings_frame,
            text="Black",
            variable=self.color_var,
            value="black",
            command=self.change_player_color,
            font=("Segoe UI", 10),
            bg="#F5F5F5",
        ).pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(
            settings_frame,
            text="AI time per move:",
            font=("Segoe UI", 10),
            bg="#F5F5F5",
        ).pack(side=tk.LEFT, padx=(0, 6))
        self.time_var = tk.StringVar(value="1.0")
        time_spinner = ttk.Spinbox(
            settings_frame,
            from_=0.5,
            to=10.0,
            increment=0.5,
            textvariable=self.time_var,
            width=5,
            justify="center",
        )
        time_spinner.pack(side=tk.LEFT)
        tk.Label(
            settings_frame,
            text="sec",
            font=("Segoe UI", 10),
            bg="#F5F5F5",
        ).pack(side=tk.LEFT, padx=(4, 0))

        button_row1 = tk.Frame(bottom_frame, bg="#F5F5F5")
        button_row1.pack(fill=tk.X)
        for text, command in [
            ("New Game", self.new_game),
            ("Undo Move", self.undo_move),
            ("Hint", self.toggle_hint),
            ("Save PGN", self.save_game),
        ]:
            tk.Button(
                button_row1,
                text=text,
                command=command,
                font=("Segoe UI", 10),
                width=12,
                bg="#E3F2FD",
                activebackground="#BBDEFB",
                relief=tk.RAISED,
                bd=1,
            ).pack(side=tk.LEFT, padx=4, pady=3)

        button_row2 = tk.Frame(bottom_frame, bg="#F5F5F5")
        button_row2.pack(fill=tk.X)
        for text, command in [
            ("Load PGN", self.load_game),
            ("âš™ï¸ Accounts", self.open_settings),
            ("Review", self.open_review_menu),
            ("Moves", self.show_move_history),
        ]:
            tk.Button(
                button_row2,
                text=text,
                command=command,
                font=("Segoe UI", 10),
                width=12,
                bg="#E8F5E9",
                activebackground="#C8E6C9",
                relief=tk.RAISED,
                bd=1,
            ).pack(side=tk.LEFT, padx=4, pady=3)

        button_row3 = tk.Frame(bottom_frame, bg="#F5F5F5")
        button_row3.pack(fill=tk.X)
        for text, command, bg_color, active_color in [
            ("Theme", self.open_theme_selector, "#FFFDE7", "#FFF9C4"),
            ("Piece Set", self.open_piece_selector, "#FFFDE7", "#FFF9C4"),
        ]:
            tk.Button(
                button_row3,
                text=text,
                command=command,
                font=("Segoe UI", 10, "bold"),
                width=14,
                bg=bg_color,
                activebackground=active_color,
                relief=tk.RAISED,
                bd=2,
            ).pack(side=tk.LEFT, padx=4, pady=3)
    
    def analyze_full_game(self):
        """Analyze all moves in the game and find mistakes."""
        if not self.engine:
            messagebox.showwarning("No Engine", "Stockfish required for analysis!")
            return
        
        self.review_analysis_text.delete(1.0, tk.END)
        self.review_analysis_text.insert(tk.END, "Analyzing game... Please wait...\n\n")
        
        def analyze():
            try:
                analysis_text = "=== Game Analysis ===\n\n"
                board = chess.Board()
                total_moves = len(self.review_moves)
                
                for move_num, move in enumerate(self.review_moves):
                    # Update progress
                    progress = f"Analyzing move {move_num + 1}/{total_moves}...\n"
                    self.root.after(0, lambda p=progress: self.review_analysis_text.insert(tk.END, p))
                    
                    # Get eval before move with reduced time for speed
                    with self.engine_lock:
                        info = self.engine.analyse(board, chess.engine.Limit(time=0.2))
                    score_before = info.get("score")
                    eval_before = 0.0
                    
                    if score_before:
                        if score_before.is_mate():
                            mate = score_before.relative.mate()
                            eval_before = 100.0 if mate > 0 else -100.0
                        elif score_before.relative.score():
                            eval_before = score_before.relative.score() / 100.0
                    
                    # Make move
                    san_move = board.san(move)
                    board.push(move)
                    
                    # Get eval after move
                    with self.engine_lock:
                        info = self.engine.analyse(board, chess.engine.Limit(time=0.2))
                    score_after = info.get("score")
                    eval_after = 0.0
                    
                    if score_after:
                        if score_after.is_mate():
                            mate = score_after.relative.mate()
                            eval_after = 100.0 if mate > 0 else -100.0
                        elif score_after.relative.score():
                            eval_after = score_after.relative.score() / 100.0
                    
                    # Calculate eval change (from player's perspective)
                    eval_change = -(eval_after - eval_before)  # Negative because turn switched
                    
                    # Classify move
                    move_quality = ""
                    if abs(eval_before) > 50 or abs(eval_after) > 50:
                        move_quality = "OK"  # Skip quality for mate positions
                    elif eval_change < -2.0:
                        move_quality = "BLUNDER"
                    elif eval_change < -1.0:
                        move_quality = "Mistake"
                    elif eval_change < -0.5:
                        move_quality = "?! Inaccuracy"
                    elif eval_change > 0.5:
                        move_quality = "Good"
                    else:
                        move_quality = "="
                    
                    turn = "White" if move_num % 2 == 0 else "Black"
                    move_line = f"{move_num + 1}. {san_move} ({turn}) - {move_quality}\n"
                    move_line += f"   Eval: {eval_before:+.2f} -> {eval_after:+.2f}"
                    
                    if eval_change < -0.5:
                        move_line += f" (Loss: {eval_change:.2f})"
                    
                    move_line += "\n\n"
                    analysis_text += move_line
                
                analysis_text += "\n=== Analysis Complete ===\n"
                
                self.root.after(0, lambda: self.review_analysis_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_analysis_text.insert(tk.END, analysis_text))
                
            except Exception as e:
                error_text = f"\n\nError during analysis: {str(e)}\n"
                self.root.after(0, lambda: self.review_analysis_text.insert(tk.END, error_text))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def exit_review_mode(self, window):
        """Exit review mode and return to normal play."""
        self.review_mode = False
        # Cancel any pending scheduled/ongoing analysis
        try:
            if getattr(self, '_review_after_id', None):
                self.root.after_cancel(self._review_after_id)
        except Exception:
            pass
        self._review_after_id = None
        self._review_slider_dragging = False
        self.review_board = None
        self.review_moves = []
        self.review_move_index = 0
        self.top_move_arrows = []
        self.review_ply_sans = []
        self.review_pair_rows = []
        self.review_engine_token += 1  # Invalidate any in-flight analysis
        self.review_window = None
        self.review_analysis_text = None
        self.review_eval_value_label = None
        self.review_engine_info_var = None
        self.review_move_label = None
        self.review_slider = None
        self.review_move_table = None
        self.review_row_ids = []
        self.board = chess.Board()
        self.draw_board()
        try:
            if window and window.winfo_exists():
                window.destroy()
        except Exception:
            pass
    
    def draw_review_board_canvas(self):
        """Draw the embedded review board canvas with arrows."""
        if not hasattr(self, 'review_canvas'):
            return
        c = self.review_canvas
        c.delete("all")
        size = self.REVIEW_SQUARE_SIZE
        theme = self.THEMES[self.current_theme]
        piece_set = self.PIECE_SETS[self.piece_style]
        # Squares
        for row in range(8):
            for col in range(8):
                x1 = col * size
                y1 = row * size
                x2 = x1 + size
                y2 = y1 + size
                color = theme['light'] if (row + col) % 2 == 0 else theme['dark']
                c.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        # Pieces
        for square in chess.SQUARES:
            piece = self.review_board.piece_at(square)
            if piece:
                row = 7 - (square // 8)
                col = square % 8
                x = col * size + size // 2
                y = row * size + size // 2
                symbol = piece_set.get(piece.symbol(), piece.symbol())
                piece_color = theme['white_piece'] if piece.color == chess.WHITE else theme['black_piece']
                c.create_text(x+1, y+1, text=symbol, font=("Arial", int(size*0.65), "bold"), fill="#808080")
                c.create_text(x, y, text=symbol, font=("Arial", int(size*0.65), "bold"), fill=piece_color)
        # Arrows
        try:
            if hasattr(self, 'top_move_arrows') and self.top_move_arrows and self.show_top_moves_var.get():
                for move, rank in self.top_move_arrows:
                    from_sq = move.from_square
                    to_sq = move.to_square
                    fr = 7 - (from_sq // 8)
                    fc = from_sq % 8
                    tr = 7 - (to_sq // 8)
                    tc = to_sq % 8
                    x1 = fc * size + size // 2
                    y1 = fr * size + size // 2
                    x2 = tc * size + size // 2
                    y2 = tr * size + size // 2
                    colors = {1: '#34C759', 2: '#0A84FF', 3: '#FF9F0A', 4: '#AF52DE', 5: '#FF3B30'}
                    width = max(2, 6 - rank)
                    arrow_shape = (12, 16, 6)
                    c.create_line(x1, y1, x2, y2, fill=colors.get(rank, '#34C759'), width=width, arrow=tk.LAST, arrowshape=arrow_shape)
        except Exception:
            pass

    def draw_review_eval_bar(self, evaluation=0.0):
        """Draw evaluation bar for the review canvas."""
        if not hasattr(self, 'review_eval_canvas'):
            return
        c = self.review_eval_canvas
        c.delete("all")
        bar_width = 40
        bar_height = self.REVIEW_SQUARE_SIZE * 8
        eval_clamped = max(-10, min(10, evaluation))
        white_height = int((bar_height / 2) * (1 + eval_clamped / 10))
        black_height = bar_height - white_height
        c.create_rectangle(0, 0, bar_width, black_height, fill="#2C2C2C", outline="")
        c.create_rectangle(0, black_height, bar_width, bar_height, fill="#FFFFFF", outline="")
        center_y = bar_height // 2
        c.create_line(0, center_y, bar_width, center_y, fill="#FF0000", width=2)
    
    def open_settings(self):
        """Open settings dialog for account configuration and engine settings."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x350")
        settings_window.resizable(False, False)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Account Settings Tab
        account_tab = tk.Frame(notebook)
        notebook.add(account_tab, text="Accounts")
        
        tk.Label(account_tab, text="Lichess Username:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        lichess_entry = tk.Entry(account_tab, width=30)
        lichess_entry.insert(0, self.lichess_username)
        lichess_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(account_tab, text="Chess.com Username:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        chesscom_entry = tk.Entry(account_tab, width=30)
        chesscom_entry.insert(0, self.chesscom_username)
        chesscom_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Engine Settings Tab
        engine_tab = tk.Frame(notebook)
        notebook.add(engine_tab, text="Engine")
        
        tk.Label(engine_tab, text="AI Thinking Time (seconds):", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        thinking_time_var = tk.StringVar(value=self.time_var.get())
        thinking_time_spin = tk.Spinbox(engine_tab, from_=0.1, to=10.0, increment=0.1, textvariable=thinking_time_var, width=10)
        thinking_time_spin.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        tk.Label(engine_tab, text="Engine Skill Level:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        skill_var = tk.IntVar(value=getattr(self, 'skill_level', 20))
        skill_scale = tk.Scale(engine_tab, from_=1, to=20, orient=tk.HORIZONTAL, variable=skill_var, length=200)
        skill_scale.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        tk.Label(engine_tab, text="(1=Beginner, 20=Maximum)", font=("Arial", 8), fg="gray").grid(row=2, column=1, padx=10, sticky="w")
        
        tk.Label(engine_tab, text="MultiPV (Top Moves):", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        multipv_var = tk.IntVar(value=getattr(self, 'multipv_count', 3))
        multipv_spin = tk.Spinbox(engine_tab, from_=1, to=5, textvariable=multipv_var, width=10)
        multipv_spin.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        tk.Label(engine_tab, text="(Number of best moves to show)", font=("Arial", 8), fg="gray").grid(row=4, column=1, padx=10, sticky="w")
        
        # Appearance Settings Tab
        appearance_tab = tk.Frame(notebook)
        notebook.add(appearance_tab, text="Appearance")
        
        tk.Label(appearance_tab, text="Board Theme:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(appearance_tab, textvariable=theme_var, values=list(self.THEMES.keys()), width=20, state="readonly")
        theme_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        tk.Label(appearance_tab, text="Piece Style:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        piece_var = tk.StringVar(value=self.piece_style)
        piece_combo = ttk.Combobox(appearance_tab, textvariable=piece_var, values=list(self.PIECE_SETS.keys()), width=20, state="readonly")
        piece_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        def save_and_close():
            # Save account settings
            self.lichess_username = lichess_entry.get().strip()
            self.chesscom_username = chesscom_entry.get().strip()
            
            # Save engine settings
            try:
                self.time_var.set(thinking_time_var.get())
                self.skill_level = skill_var.get()
                self.multipv_count = multipv_var.get()

                if hasattr(self, 'engine_skill_value'):
                    self.engine_skill_value.config(text=str(self.skill_level))
                if hasattr(self, 'engine_multipv_value'):
                    self.engine_multipv_value.config(text=str(self.multipv_count))
                
                # Apply skill level to engine
                if self.engine and hasattr(self.engine, 'configure'):
                    try:
                        self.engine.configure({"Skill Level": self.skill_level})
                    except:
                        pass  # Not all engines support skill level
            except:
                pass
            
            # Save appearance settings
            self.current_theme = theme_var.get()
            self.piece_style = piece_var.get()
            
            self.save_settings()
            messagebox.showinfo("Saved", "Settings saved!")
            self.draw_board()  # Redraw with new theme
            settings_window.destroy()
        
        button_frame = tk.Frame(settings_window)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Save", command=save_and_close, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=settings_window.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def open_review_menu(self):
        """Open game review menu."""
        if not self.lichess_username and not self.chesscom_username:
            messagebox.showwarning("No Accounts", "Please configure your accounts in Settings first!")
            return
        
        if self.review_browser_window and self.review_browser_window.winfo_exists():
            self.review_browser_window.focus_set()
            return

        review_window = tk.Toplevel(self.root)
        self.review_browser_window = review_window  # keep reference
        review_window.title("Game Review")
        review_window.geometry("600x450")
        review_window.protocol("WM_DELETE_WINDOW", lambda: self._close_review_browser(review_window))
        
        tk.Label(review_window, text="Select Platform:", font=("Arial", 12, "bold")).pack(pady=10)
        
        button_frame = tk.Frame(review_window)
        button_frame.pack(pady=10)
        
        if self.lichess_username:
            tk.Button(
                button_frame,
                text=f"Lichess ({self.lichess_username})",
                command=lambda: self.fetch_lichess_games(review_window),
                width=25,
                height=2
            ).pack(pady=5)
        
        if self.chesscom_username:
            tk.Button(
                button_frame,
                text=f"Chess.com ({self.chesscom_username})",
                command=lambda: self.fetch_chesscom_games(review_window),
                width=25,
                height=2
            ).pack(pady=5)
        
        # Results area split: list on left, details on right
        results_frame = tk.Frame(review_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # List of games
        list_frame = tk.Frame(results_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(list_frame, text="Recent Games", font=("Arial", 11, "bold")).pack(anchor="w")
        self.review_list = tk.Listbox(list_frame, width=40, height=15)
        self.review_list.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.review_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.review_list.config(yscrollcommand=scrollbar.set)

        # Bind double-click to load
        self.review_list.bind('<Double-1>', lambda e: self.load_selected_review_game())

        # Details panel
        detail_frame = tk.Frame(results_frame)
        detail_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0))
        self.review_text = scrolledtext.ScrolledText(detail_frame, width=60, height=15, wrap=tk.WORD)
        self.review_text.pack(fill=tk.BOTH, expand=True)

        # Action buttons
        actions = tk.Frame(review_window)
        actions.pack(pady=(0,10))
        tk.Button(actions, text="Load Selected", command=self.load_selected_review_game, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text="Close", command=lambda: self._close_review_browser(review_window), width=10).pack(side=tk.LEFT, padx=5)

        # Storage for fetched games: list of dicts with {label, pgn}
        self.review_games = []

    def _close_review_browser(self, window):
        """Close the review browser pop-up and clear reference."""
        try:
            if window and window.winfo_exists():
                window.destroy()
        finally:
            self.review_browser_window = None

    def _prepare_review_data(self):
        """Compute SAN notation and paired moves for the current review game."""
        self.review_ply_sans = []
        self.review_pair_rows = []
        board = chess.Board()

        for idx in range(0, len(self.review_moves), 2):
            white_move = self.review_moves[idx]
            try:
                white_san = board.san(white_move)
            except ValueError:
                white_san = white_move.uci()
            self.review_ply_sans.append(white_san)
            board.push(white_move)

            black_san = ""
            if idx + 1 < len(self.review_moves):
                black_move = self.review_moves[idx + 1]
                try:
                    black_san = board.san(black_move)
                except ValueError:
                    black_san = black_move.uci()
                self.review_ply_sans.append(black_san)
                board.push(black_move)

            self.review_pair_rows.append((idx // 2 + 1, white_san, black_san))

    def open_review_window(self):
        """Launch the interactive review workspace."""
        if not self.review_moves:
            messagebox.showinfo("No Game", "Load or fetch a game before starting a review.")
            return

        if self.review_window and self.review_window.winfo_exists():
            try:
                self.review_window.focus_set()
            except tk.TclError:
                pass
            self.update_review_position()
            return

        if not self.review_board:
            self.review_board = chess.Board()
        else:
            self.review_board.reset()

        self.top_move_arrows = []
        self._prepare_review_data()

        review_window = tk.Toplevel(self.root)
        self.review_window = review_window
        review_window.title("Interactive Review")
        review_window.geometry("960x640")
        review_window.minsize(900, 620)
        review_window.configure(bg="#F4F5F7")
        review_window.protocol("WM_DELETE_WINDOW", lambda: self.exit_review_mode(review_window))

        container = tk.Frame(review_window, bg="#F4F5F7")
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        # Left panel: board, evaluation, controls
        board_size = self.REVIEW_SQUARE_SIZE * 8
        left_width = board_size + 64  # board + 12px padding + 52px eval area
        left_panel = tk.Frame(container, bg="#F4F5F7", width=left_width)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        try:
            left_panel.pack_propagate(False)
        except Exception:
            pass

        board_frame = tk.Frame(left_panel, bg="#F4F5F7", width=left_width, height=board_size)
        board_frame.pack()
        try:
            board_frame.pack_propagate(False)
        except Exception:
            pass

        self.review_canvas = tk.Canvas(
            board_frame,
            width=board_size,
            height=board_size,
            highlightthickness=0,
            bg="#F4F5F7",
        )
        self.review_canvas.pack(side=tk.LEFT)

        eval_frame = tk.Frame(board_frame, bg="#F4F5F7", height=board_size, width=52)
        eval_frame.pack(side=tk.LEFT, padx=(12, 0), fill=tk.Y)
        try:
            eval_frame.pack_propagate(False)
        except Exception:
            pass

        self.review_eval_canvas = tk.Canvas(
            eval_frame,
            width=40,
            height=board_size,
            highlightthickness=0,
            bg="#F4F5F7",
        )
        self.review_eval_canvas.pack()
        self.review_eval_value_label = tk.Label(
            eval_frame,
            text="Evaluation: ...",
            font=("Segoe UI", 11, "bold"),
            bg="#F4F5F7",
            fg="#1F1F1F",
        )
        self.review_eval_value_label.pack(pady=(10, 0))

        self.review_engine_info_var = tk.StringVar(value="Engine lines will appear here once analysis runs.")
        engine_info = tk.Label(
            left_panel,
            textvariable=self.review_engine_info_var,
            font=("Segoe UI", 9),
            bg="#F4F5F7",
            fg="#4A4A4A",
            justify="left",
            wraplength=left_width,
        )
        engine_info.pack(fill=tk.X, pady=(12, 0))

        controls_frame = tk.Frame(left_panel, bg="#F4F5F7")
        controls_frame.pack(fill=tk.X, pady=(12, 4))
        self.review_move_label = tk.Label(
            controls_frame,
            text="Move 0/0 | Start position",
            font=("Segoe UI", 12, "bold"),
            bg="#F4F5F7",
            fg="#1F1F1F",
            wraplength=left_width - 16,
        )
        self.review_move_label.pack(anchor="w")

        nav_frame = tk.Frame(left_panel, bg="#F4F5F7")
        nav_frame.pack(fill=tk.X, pady=(4, 0))
        ttk.Button(nav_frame, text="<< Start", width=10, command=lambda: self.review_jump_to(0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="< Prev", width=10, command=lambda: self.review_step(-1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Next >", width=10, command=lambda: self.review_step(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="End >>", width=10, command=lambda: self.review_jump_to(len(self.review_moves))).pack(side=tk.LEFT, padx=2)

        slider_frame = tk.Frame(left_panel, bg="#F4F5F7")
        slider_frame.pack(fill=tk.X, pady=(8, 0))
        self.review_slider = ttk.Scale(
            slider_frame,
            from_=0,
            to=max(len(self.review_moves), 1),
            orient=tk.HORIZONTAL,
            command=self.on_review_slider_move,
        )
        self.review_slider.pack(fill=tk.X, expand=True)
        # Defer analysis while dragging the slider to avoid flicker/lag
        self.review_slider.bind("<ButtonPress-1>", lambda _e: self._on_review_slider_press())
        self.review_slider.bind("<ButtonRelease-1>", lambda _e: self._on_review_slider_release())
        tk.Label(
            slider_frame,
            text="Use the slider or arrow keys to navigate moves.",
            font=("Segoe UI", 8),
            bg="#F4F5F7",
            fg="#666666",
        ).pack(anchor="w", pady=(4, 0))

        action_frame = tk.Frame(left_panel, bg="#F4F5F7")
        action_frame.pack(fill=tk.X, pady=(12, 0))
        ttk.Button(action_frame, text="Run Full Analysis", command=self.analyze_full_game).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Copy PGN", command=self.copy_review_pgn_to_clipboard).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Exit Review", command=lambda: self.exit_review_mode(review_window)).pack(side=tk.RIGHT, padx=2)

        # Right panel: move list and analysis
        right_panel = tk.Frame(container, bg="#FFFFFF", bd=1, relief=tk.GROOVE)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 0))

        tk.Label(
            right_panel,
            text="Move List",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#1F1F1F",
        ).pack(anchor="w", padx=12, pady=(12, 4))

        move_table_frame = tk.Frame(right_panel, bg="#FFFFFF")
        move_table_frame.pack(fill=tk.BOTH, expand=True, padx=12)

        columns = ("move", "white", "black")
        self.review_move_table = ttk.Treeview(move_table_frame, columns=columns, show="headings", height=14)
        self.review_move_table.heading("move", text="#")
        self.review_move_table.heading("white", text="White")
        self.review_move_table.heading("black", text="Black")
        self.review_move_table.column("move", width=50, anchor="center")
        self.review_move_table.column("white", width=180, anchor="w")
        self.review_move_table.column("black", width=180, anchor="w")
        self.review_move_table.tag_configure("current", background="#FFF3CD")
        self.review_move_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        move_scroll = ttk.Scrollbar(move_table_frame, orient=tk.VERTICAL, command=self.review_move_table.yview)
        move_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.review_move_table.configure(yscrollcommand=move_scroll.set)
        self.review_move_table.bind("<ButtonRelease-1>", self.on_review_table_click)

        tk.Label(
            right_panel,
            text="Engine Commentary",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#1F1F1F",
        ).pack(anchor="w", padx=12, pady=(8, 4))

        # Review options: Best-only toggle
        opts_frame = tk.Frame(right_panel, bg="#FFFFFF")
        opts_frame.pack(fill=tk.X, padx=12, pady=(0, 4))
        self.review_best_only_var = getattr(self, 'review_best_only_var', None)
        if self.review_best_only_var is None:
            self.review_best_only_var = tk.BooleanVar(value=False)
        def _toggle_best():
            # Re-analyze current position with new multipv setting
            self.schedule_review_engine_analysis()
        tk.Checkbutton(
            opts_frame,
            text="Best line only",
            variable=self.review_best_only_var,
            command=_toggle_best,
            bg="#FFFFFF",
            anchor="w",
        ).pack(side=tk.LEFT)

        analysis_frame = tk.Frame(right_panel, bg="#FFFFFF")
        analysis_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.review_analysis_text = scrolledtext.ScrolledText(
            analysis_frame,
            width=50,
            height=10,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
        )
        self.review_analysis_text.pack(fill=tk.BOTH, expand=True)

        # Populate UI with data and hooks
        self._populate_review_table()
        self.review_move_index = min(self.review_move_index, len(self.review_moves))
        self.update_review_position()

        review_window.bind("<Left>", lambda _e: self.review_step(-1))
        review_window.bind("<Right>", lambda _e: self.review_step(1))
        review_window.bind("<Home>", lambda _e: self.review_jump_to(0))
        review_window.bind("<End>", lambda _e: self.review_jump_to(len(self.review_moves)))

    def _populate_review_table(self):
        """Render the move list table from precomputed SAN data."""
        if not self.review_move_table:
            return

        for row_id in self.review_move_table.get_children():
            self.review_move_table.delete(row_id)

        self.review_row_ids = []
        for move_no, white_san, black_san in self.review_pair_rows:
            row_id = self.review_move_table.insert("", tk.END, values=(move_no, white_san, black_san))
            self.review_row_ids.append(row_id)

    def update_review_position(self):
        """Sync the review board, indicators, and engine hints."""
        if not self.review_board:
            return

        # Rebuild board to selected ply
        self.review_board.reset()
        for move in self.review_moves[: self.review_move_index]:
            self.review_board.push(move)

        side_to_move = "White" if self.review_board.turn == chess.WHITE else "Black"

        # Update summary label
        total = len(self.review_moves)
        if self.review_move_index == 0:
            detail = "Start position"
        else:
            try:
                last_san = self.review_ply_sans[self.review_move_index - 1]
            except IndexError:
                last_san = "(unknown)"
            move_no = (self.review_move_index + 1) // 2
            mover = "White" if (self.review_move_index - 1) % 2 == 0 else "Black"
            detail = f"Last: {mover} {last_san} (move {move_no})"

        if self.review_move_label:
            self.review_move_label.config(
                text=f"Move {self.review_move_index}/{total} | {detail} | {side_to_move} to move"
            )

        # Update slider without triggering feedback loop
        if self.review_slider:
            self._updating_review_slider = True
            self.review_slider.configure(to=max(total, 1))
            self.review_slider.set(self.review_move_index)
            self._updating_review_slider = False

        # Redraw board and evaluation placeholders
        self.top_move_arrows = []
        self.draw_review_board_canvas()
        self.draw_review_eval_bar(0.0)
        if self.review_eval_value_label:
            self.review_eval_value_label.config(text="Evaluation: ...")
        # Keep left-side status concise and push detailed lines to the right panel box
        if self.review_engine_info_var:
            self.review_engine_info_var.set("Analyzing position...")

        self._highlight_review_table()
        # Skip scheduling while slider is being dragged; run when released
        if not self._review_slider_dragging:
            self.schedule_review_engine_analysis()

    def review_step(self, delta):
        """Move forward or backward by a single ply."""
        if not self.review_moves:
            return
        self.review_jump_to(self.review_move_index + delta)

    def review_jump_to(self, index):
        """Jump to a specific half-move index."""
        if not self.review_moves and index != 0:
            return
        clamped = max(0, min(index, len(self.review_moves)))
        if clamped == self.review_move_index:
            return
        self.review_move_index = clamped
        self.update_review_position()

    def on_review_slider_move(self, value):
        """Handle slider drag events for navigating the game."""
        if self._updating_review_slider:
            return
        try:
            index = int(float(value) + 0.5)
        except (TypeError, ValueError):
            return
        self.review_jump_to(index)

    def on_review_table_click(self, event):
        """Jump to a move when the user clicks the move list."""
        if not self.review_move_table:
            return
        item_id = self.review_move_table.identify_row(event.y)
        if not item_id:
            return

        values = self.review_move_table.item(item_id, "values")
        if not values:
            return

        try:
            move_no = int(values[0])
        except (TypeError, ValueError):
            return

        column = self.review_move_table.identify_column(event.x)
        base_index = (move_no - 1) * 2
        if column == "#1":  # Move number clicked
            target = base_index
        elif column == "#2":  # White move column
            target = base_index + 1
        else:  # Black column
            target = base_index + 2

        self.review_jump_to(target)

    def _highlight_review_table(self):
        """Highlight the current move row in the table."""
        if not self.review_move_table:
            return

        for row_id in self.review_row_ids:
            self.review_move_table.item(row_id, tags=())
        self.review_move_table.selection_remove(self.review_move_table.selection())

        if self.review_move_index == 0 or not self.review_row_ids:
            return

        row_idx = (self.review_move_index - 1) // 2
        if row_idx < 0 or row_idx >= len(self.review_row_ids):
            return

        row_id = self.review_row_ids[row_idx]
        self.review_move_table.selection_set(row_id)
        self.review_move_table.see(row_id)
        self.review_move_table.item(row_id, tags=("current",))

    def schedule_review_engine_analysis(self):
        """Debounce review engine analysis requests during scrubbing."""
        if not self.review_window or not self.review_window.winfo_exists():
            return
        if self._review_slider_dragging:
            return
        # Cancel any pending call
        if self._review_after_id is not None:
            try:
                self.root.after_cancel(self._review_after_id)
            except Exception:
                pass
            self._review_after_id = None

        def _do():
            self._review_after_id = None
            self._request_review_engine_analysis()

        self._review_after_id = self.root.after(self._review_debounce_ms, _do)

    def _on_review_slider_press(self):
        self._review_slider_dragging = True
        # Cancel any pending scheduled analysis to avoid burst runs after drag
        if self._review_after_id is not None:
            try:
                self.root.after_cancel(self._review_after_id)
            except Exception:
                pass
            self._review_after_id = None

    def _on_review_slider_release(self):
        self._review_slider_dragging = False
        # Now that the user released, schedule analysis for the current position
        self.schedule_review_engine_analysis()

    def _request_review_engine_analysis(self):
        """Ask Stockfish for evaluation and principal variations."""
        if not self.review_window or not self.review_window.winfo_exists():
            return
        if not self.engine or not self.review_board:
            if self.review_engine_info_var:
                self.review_engine_info_var.set("Engine not available. Configure Stockfish to see suggestions.")
            return

        # Cache key per position+settings to avoid recomputation during scrubbing
        try:
            think_time = float(self.time_var.get())
        except (TypeError, ValueError):
            think_time = 0.5
        # Use a shorter time in review to keep UI responsive
        think_time = max(0.15, min(think_time, 2.0)) * 0.6

        # Honor Best-only toggle
        if getattr(self, 'review_best_only_var', None) and self.review_best_only_var.get():
            multipv = 1
        else:
            multipv = max(1, int(self.multipv_count))
        fen_snapshot = self.review_board.fen()
        ply_snapshot = self.review_move_index
        cache_key = (fen_snapshot, multipv)

        # Fast path: cached result exists
        cached = self.review_analysis_cache.get(cache_key)
        if cached is not None:
            evaluation, label, arrows, lines = cached
            self._apply_review_engine_result(self.review_engine_token, ply_snapshot, evaluation, label, arrows, lines)
            return

        # Otherwise, compute asynchronously
        self.review_engine_token += 1
        token = self.review_engine_token

        def worker():
            board = chess.Board(fen_snapshot)
            try:
                with self.engine_lock:
                    info = self.engine.analyse(board, chess.engine.Limit(time=think_time), multipv=multipv)
            except Exception as exc:
                self.root.after(0, lambda: self._apply_review_engine_error(token, ply_snapshot, str(exc)))
                return

            infos = info if isinstance(info, list) else [info]
            arrows = []
            lines = []
            evaluation = 0.0
            label = "+0.00"

            # Shorter PVs when analysis time is low to keep UI snappy
            pv_limit = 4 if think_time < 0.35 else 6

            for idx, entry in enumerate(infos, start=1):
                pv = entry.get("pv") or []
                if not pv:
                    continue

                move = pv[0]
                arrows.append((move, idx))

                eval_value, eval_label = self._convert_score_to_eval(entry.get("score"))
                if idx == 1:
                    evaluation = eval_value
                    label = eval_label

                pv_board = chess.Board(fen_snapshot)
                san_moves = []
                for pv_move in pv[:pv_limit]:
                    try:
                        san_moves.append(pv_board.san(pv_move))
                        pv_board.push(pv_move)
                    except ValueError:
                        break

                pv_text = " ".join(san_moves) if san_moves else move.uci()
                depth = entry.get("depth")
                depth_str = f" (d{depth})" if depth else ""
                prefix = "Best" if idx == 1 else f"#{idx}"
                lines.append(f"{prefix}: {eval_label}{depth_str} - {pv_text}")

            if not lines:
                lines.append("Engine did not return a principal variation.")

            # Optional: classify last played move vs best (skip in quick mode)
            if think_time >= 0.35:
                try:
                    last_move = self.review_moves[ply_snapshot - 1] if ply_snapshot > 0 else None
                    if last_move is not None:
                        base_board = chess.Board(fen_snapshot)
                        # Undo last move to compare from same turn
                        history = list(self.review_moves[:ply_snapshot])
                        base_board.reset()
                        for m in history[:-1]:
                            base_board.push(m)
                        # Get eval before and after last move
                        with self.engine_lock:
                            pre_info = self.engine.analyse(base_board, chess.engine.Limit(time=max(0.1, think_time * 0.5)))
                        pre_eval, pre_label = self._convert_score_to_eval(pre_info.get("score"))
                        base_board.push(last_move)
                        with self.engine_lock:
                            post_info = self.engine.analyse(base_board, chess.engine.Limit(time=max(0.1, think_time * 0.5)))
                        post_eval, post_label = self._convert_score_to_eval(post_info.get("score"))
                        delta = post_eval - pre_eval
                        verdict = "=" if abs(delta) < 0.5 else ("Good" if delta > 0.5 else ("Inaccuracy" if delta > -1.0 else ("Mistake" if delta > -2.0 else "Blunder")))
                        icon = {"Good": "Good", "Inaccuracy": "?!", "Mistake": "Mistake", "Blunder": "Blunder", "=": "="}[verdict]
                        lines.insert(0, f"{icon} - Last move impact: {delta:+.2f} (from {pre_label} to {post_label}) - {verdict}")
                except Exception:
                    pass

            # Store in cache (with simple LRU eviction)
            self.review_analysis_cache[cache_key] = (evaluation, label, arrows, lines)
            self._review_cache_order.append(cache_key)
            if len(self._review_cache_order) > self._review_cache_max:
                old_key = self._review_cache_order.pop(0)
                self.review_analysis_cache.pop(old_key, None)

            self.root.after(
                0,
                lambda: self._apply_review_engine_result(token, ply_snapshot, evaluation, label, arrows, lines),
            )

        threading.Thread(target=worker, daemon=True).start()

    def _convert_score_to_eval(self, score):
        """Convert a python-chess score to (float evaluation, label)."""
        if not score:
            return 0.0, "+0.00"

        relative = score.relative
        if score.is_mate():
            mate = relative.mate()
            if mate is None:
                return 0.0, "#?"
            label = f"#{mate}" if mate > 0 else f"#-{abs(mate)}"
            value = 100.0 if mate > 0 else -100.0
            return value, label

        cp = relative.score()
        if cp is None:
            return 0.0, "+0.00"
        pawns = cp / 100.0
        return pawns, f"{pawns:+.2f}"

    def _apply_review_engine_result(self, token, ply_index, evaluation, label, arrows, lines):
        """Update the UI when engine analysis completes."""
        if token != self.review_engine_token or ply_index != self.review_move_index:
            return

        self.top_move_arrows = arrows
        self.draw_review_board_canvas()
        self.draw_review_eval_bar(evaluation)

        if self.review_eval_value_label:
            self.review_eval_value_label.config(text=f"Evaluation: {label}")
        # Write full commentary to the right panel box
        if hasattr(self, "review_analysis_text") and self.review_analysis_text:
            try:
                self.review_analysis_text.config(state=tk.NORMAL)
                self.review_analysis_text.delete(1.0, tk.END)
                self.review_analysis_text.insert(tk.END, "\n".join(lines) + "\n")
                self.review_analysis_text.config(state=tk.DISABLED)
            except Exception:
                pass
        # Keep the left label short
        if self.review_engine_info_var:
            self.review_engine_info_var.set("Suggestions updated.")

    def _apply_review_engine_error(self, token, ply_index, message):
        """Handle engine failures gracefully."""
        if token != self.review_engine_token or ply_index != self.review_move_index:
            return

        self.top_move_arrows = []
        self.draw_review_board_canvas()
        self.draw_review_eval_bar(0.0)

        if self.review_eval_value_label:
            self.review_eval_value_label.config(text="Evaluation: engine error")
        # Show error message in the right panel box
        if hasattr(self, "review_analysis_text") and self.review_analysis_text:
            try:
                short_msg = (message or "Unknown error").splitlines()[0]
                self.review_analysis_text.config(state=tk.NORMAL)
                self.review_analysis_text.delete(1.0, tk.END)
                self.review_analysis_text.insert(tk.END, f"Engine error: {short_msg}\n")
                self.review_analysis_text.config(state=tk.DISABLED)
            except Exception:
                pass
        # Keep left label short
        if self.review_engine_info_var:
            short_msg = (message or "Unknown error").splitlines()[0][:160]
            self.review_engine_info_var.set("Engine error.")

    def copy_review_pgn_to_clipboard(self):
        """Copy the current review game to the clipboard as PGN."""
        if not self.review_moves:
            messagebox.showinfo("No Game", "Nothing to copy yet.")
            return

        game = chess.pgn.Game()
        node = game
        for move in self.review_moves:
            node = node.add_variation(move)

        pgn_text = str(game)
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(pgn_text)
            messagebox.showinfo("Copied", "Game PGN copied to clipboard.")
        except tk.TclError:
            messagebox.showerror("Clipboard Error", "Unable to access clipboard on this system.")

    def fetch_lichess_games(self, parent_window):
        """Fetch recent games from Lichess."""
        self.review_text.delete(1.0, tk.END)
        self.review_text.insert(tk.END, "Fetching games from Lichess...\n\n")
        
        def fetch():
            try:
                # Add headers to mimic a browser request
                headers = {
                    'User-Agent': 'Chess Analyser App/1.0',
                    'Accept': 'application/x-ndjson'
                }
                
                url = f"https://lichess.org/api/games/user/{self.lichess_username}"
                params = {"max": 10, "pgnInJson": "true"}
                
                max_retries = 3
                response = None
                
                for attempt in range(max_retries):
                    try:
                        response = requests.get(url, params=params, headers=headers, stream=True, timeout=15)
                        response.raise_for_status()
                        break
                    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                        if attempt == max_retries - 1:
                            raise
                        self.root.after(0, lambda a=attempt: self.review_text.insert(
                            tk.END, f"Connection attempt {a+1} failed, retrying...\n"))
                        import time
                        time.sleep(2)
                
                games_text = "Recent Lichess Games:\n" + "="*50 + "\n\n"
                count = 0
                collected = []  # to populate selection list
                
                for line in response.iter_lines():
                    if line:
                        try:
                            game_data = json.loads(line.decode('utf-8'))
                            count += 1
                            games_text += f"Game #{count}:\n"
                            games_text += f"White: {game_data.get('players', {}).get('white', {}).get('user', {}).get('name', 'Unknown')}\n"
                            games_text += f"Black: {game_data.get('players', {}).get('black', {}).get('user', {}).get('name', 'Unknown')}\n"
                            games_text += f"Result: {game_data.get('status', 'Unknown')}\n"
                            games_text += f"Winner: {game_data.get('winner', 'Draw/Unknown')}\n"
                            
                            # Add game URL if available
                            game_id = game_data.get('id', '')
                            if game_id:
                                games_text += f"URL: https://lichess.org/{game_id}\n"
                            
                            games_text += "-"*50 + "\n\n"
                            
                            # Build a label and store PGN if present
                            white = game_data.get('players', {}).get('white', {}).get('user', {}).get('name', 'White')
                            black = game_data.get('players', {}).get('black', {}).get('user', {}).get('name', 'Black')
                            label = f"{count}. {white} vs {black}"
                            pgn = game_data.get('pgn', None)
                            if pgn:
                                collected.append({"label": label, "pgn": pgn})
                            
                            if count >= 10:
                                break
                        except json.JSONDecodeError:
                            continue
                
                if count == 0:
                    games_text += "No recent games found.\nPlease check the username is correct.\n"
                
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, games_text))
                # Populate listbox
                def update_list():
                    self.review_list.delete(0, tk.END)
                    self.review_games = collected
                    for g in collected:
                        self.review_list.insert(tk.END, g["label"])
                self.root.after(0, update_list)
                
            except requests.exceptions.ConnectionError as e:
                error_msg = f"Connection Error: Unable to reach Lichess API.\n"
                error_msg += "Please check your internet connection and try again.\n"
                error_msg += f"Details: {str(e)[:100]}\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
            except requests.exceptions.Timeout:
                error_msg = "Request Timeout: Lichess API is taking too long to respond.\n"
                error_msg += "Please try again later.\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
            except requests.exceptions.HTTPError as e:
                error_msg = f"HTTP Error: {e}\n"
                error_msg += "The username may be incorrect or the API is unavailable.\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
            except Exception as e:
                error_msg = f"Unexpected Error: {type(e).__name__}\n"
                error_msg += f"Details: {str(e)[:200]}\n"
                error_msg += "\nTroubleshooting:\n"
                error_msg += "1. Verify your Lichess username is correct\n"
                error_msg += "2. Check your internet connection\n"
                error_msg += "3. Try again in a few moments\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def fetch_chesscom_games(self, parent_window):
        """Fetch recent games from Chess.com."""
        self.review_text.delete(1.0, tk.END)
        self.review_text.insert(tk.END, "Fetching games from Chess.com...\n\n")
        
        def fetch():
            try:
                # Validate username first
                if not self.chesscom_username or self.chesscom_username.strip() == "":
                    error_msg = "Chess.com username is not set!\n"
                    error_msg += "Please go to âš™ï¸ Accounts and enter your username.\n"
                    self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                    self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
                    return
                
                # Add headers to mimic a browser request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US,en;q=0.9'
                }
                
                # Normalize username (Chess.com converts to lowercase)
                username = self.chesscom_username.lower().strip()
                
                self.root.after(0, lambda: self.review_text.insert(
                    tk.END, f"Looking for user: {username}\n\n"))
                
                # First, verify the user exists
                profile_url = f"https://api.chess.com/pub/player/{username}"
                max_retries = 3
                
                for attempt in range(max_retries):
                    try:
                        profile_response = requests.get(profile_url, headers=headers, timeout=20)
                        if profile_response.status_code == 404:
                            error_msg = f"User '{username}' not found on Chess.com!\n"
                            error_msg += "Please check your username spelling.\n"
                            self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                            self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
                            return
                        profile_response.raise_for_status()
                        break
                    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                        if attempt == max_retries - 1:
                            raise
                        self.root.after(0, lambda a=attempt: self.review_text.insert(
                            tk.END, f"Connection attempt {a+1} failed, retrying...\n"))
                        import time
                        time.sleep(2)
                
                # Get game archives
                url = f"https://api.chess.com/pub/player/{username}/games/archives"
                
                for attempt in range(max_retries):
                    try:
                        response = requests.get(url, headers=headers, timeout=20)
                        response.raise_for_status()
                        archives = response.json()
                        break
                    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                        if attempt == max_retries - 1:
                            raise
                        self.root.after(0, lambda a=attempt: self.review_text.insert(
                            tk.END, f"Archive fetch attempt {a+1} failed, retrying...\n"))
                        import time
                        time.sleep(2)
                
                if 'archives' in archives and archives['archives']:
                    # Get latest month
                    latest_archive = archives['archives'][-1]
                    
                    self.root.after(0, lambda: self.review_text.insert(
                        tk.END, f"Found {len(archives['archives'])} months of games.\n"))
                    self.root.after(0, lambda: self.review_text.insert(
                        tk.END, f"Fetching latest month: {latest_archive}\n\n"))
                    
                    # Retry for games as well
                    for attempt in range(max_retries):
                        try:
                            games_response = requests.get(latest_archive, headers=headers, timeout=20)
                            games_response.raise_for_status()
                            games_data = games_response.json()
                            break
                        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                            if attempt == max_retries - 1:
                                raise
                            self.root.after(0, lambda a=attempt: self.review_text.insert(
                                tk.END, f"Games fetch attempt {a+1} failed, retrying...\n"))
                            import time
                            time.sleep(3)
                    
                    games_text = "Recent Chess.com Games:\n" + "="*50 + "\n\n"
                    collected = []
                    
                    games = games_data.get('games', [])[-10:]  # Last 10 games
                    if not games:
                        games_text += "No recent games found in the latest month.\n"
                        games_text += "This account may not have played recently.\n"
                    else:
                        for i, game in enumerate(reversed(games), 1):
                            games_text += f"Game #{i}:\n"
                            games_text += f"White: {game.get('white', {}).get('username', 'Unknown')}\n"
                            games_text += f"Black: {game.get('black', {}).get('username', 'Unknown')}\n"
                            games_text += f"Result: {game.get('white', {}).get('result', 'Unknown')} - {game.get('black', {}).get('result', 'Unknown')}\n"
                            games_text += f"Time Control: {game.get('time_control', 'Unknown')}\n"
                            
                            # Add link to analyze
                            if 'url' in game:
                                games_text += f"URL: {game['url']}\n"
                            
                            games_text += "-"*50 + "\n\n"
                            # Try to fetch PGN link if available
                            white = game.get('white', {}).get('username', 'White')
                            black = game.get('black', {}).get('username', 'Black')
                            label = f"{i}. {white} vs {black}"
                            pgn_text = game.get('pgn') if 'pgn' in game else None
                            # Some chess.com game endpoints include 'pgn', otherwise skip
                            if pgn_text:
                                collected.append({"label": label, "pgn": pgn_text})
                    
                    self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                    self.root.after(0, lambda: self.review_text.insert(tk.END, games_text))
                    # Populate listbox
                    def update_list():
                        self.review_list.delete(0, tk.END)
                        self.review_games = collected
                        for g in collected:
                            self.review_list.insert(tk.END, g["label"])
                    self.root.after(0, update_list)
                else:
                    error_msg = "No games found for this user.\nPlease check the username is correct.\n"
                    self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                    self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
                    
            except requests.exceptions.ConnectionError as e:
                error_msg = f"Connection Error: Unable to reach Chess.com API.\n"
                error_msg += "Please check your internet connection and try again.\n"
                error_msg += f"Details: {str(e)[:100]}\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
            except requests.exceptions.Timeout:
                error_msg = "Request Timeout: Chess.com API is taking too long to respond.\n"
                error_msg += "Please try again later.\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
            except requests.exceptions.HTTPError as e:
                error_msg = f"HTTP Error: {e}\n"
                error_msg += "The username may be incorrect or the API is unavailable.\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
            except Exception as e:
                error_msg = f"Unexpected Error: {type(e).__name__}\n"
                error_msg += f"Details: {str(e)[:200]}\n"
                error_msg += "\nTroubleshooting:\n"
                error_msg += "1. Verify your Chess.com username is correct\n"
                error_msg += "2. Check your internet connection\n"
                error_msg += "3. Try again in a few moments\n"
                self.root.after(0, lambda: self.review_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.review_text.insert(tk.END, error_msg))
        
        threading.Thread(target=fetch, daemon=True).start()

    def _collect_recent_lichess_games(self, username, limit=12):
        """Return a list of recent Lichess games with PGNs for inline review."""
        headers = {
            "User-Agent": "Chess Analyser App/1.0",
            "Accept": "application/x-ndjson",
        }
        params = {"max": limit, "pgnInJson": "true"}
        url = f"https://lichess.org/api/games/user/{username}"

        response = requests.get(url, params=params, headers=headers, stream=True, timeout=20)
        response.raise_for_status()

        games = []
        for line in response.iter_lines():
            if not line:
                continue
            try:
                game_data = json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                continue

            white = (
                game_data.get("players", {})
                .get("white", {})
                .get("user", {})
                .get("name")
                or "White"
            )
            black = (
                game_data.get("players", {})
                .get("black", {})
                .get("user", {})
                .get("name")
                or "Black"
            )

            winner = game_data.get("winner")
            if winner == "white":
                result = "1-0"
            elif winner == "black":
                result = "0-1"
            elif winner == "draw":
                result = "1/2-1/2"
            else:
                result = game_data.get("status", "?")

            created_ms = game_data.get("createdAt")
            if created_ms:
                date_str = datetime.fromtimestamp(created_ms / 1000).strftime("%Y-%m-%d")
            else:
                date_str = "Unknown"

            games.append(
                {
                    "platform": "Lichess",
                    "players": f"{white} vs {black}",
                    "result": result,
                    "date": date_str,
                    "pgn": game_data.get("pgn"),
                }
            )

            if len(games) >= limit:
                break

        return games

    def _collect_recent_chesscom_games(self, username, limit=12):
        """Return a list of recent Chess.com games with PGNs for inline review."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }

        normalized = username.lower()
        profile_url = f"https://api.chess.com/pub/player/{normalized}"
        profile_response = requests.get(profile_url, headers=headers, timeout=20)
        if profile_response.status_code == 404:
            raise ValueError(f"Chess.com user '{username}' not found")
        profile_response.raise_for_status()

        archives_url = f"https://api.chess.com/pub/player/{normalized}/games/archives"
        archives_response = requests.get(archives_url, headers=headers, timeout=20)
        archives_response.raise_for_status()
        archives = archives_response.json().get("archives", [])
        if not archives:
            return []

        games = []
        # Iterate most recent archives until we fill the limit
        for archive_url in reversed(archives):
            month_response = requests.get(archive_url, headers=headers, timeout=20)
            month_response.raise_for_status()
            month_games = month_response.json().get("games", [])
            for game in reversed(month_games):
                white = game.get("white", {}).get("username", "White")
                black = game.get("black", {}).get("username", "Black")

                white_res = game.get("white", {}).get("result", "?")
                black_res = game.get("black", {}).get("result", "?")
                if white_res == "win":
                    result = "1-0"
                elif black_res == "win":
                    result = "0-1"
                elif "draw" in (white_res, black_res):
                    result = "1/2-1/2"
                else:
                    result = f"{white_res}-{black_res}"

                end_time = game.get("end_time")
                if end_time:
                    date_str = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d")
                else:
                    date_str = "Unknown"

                games.append(
                    {
                        "platform": "Chess.com",
                        "players": f"{white} vs {black}",
                        "result": result,
                        "date": date_str,
                        "pgn": game.get("pgn"),
                    }
                )

                if len(games) >= limit:
                    return games

        return games

    def inline_fetch_games(self, platform):
        """Populate the inline review table with recent games from the chosen platform."""
        platform = platform.lower()
        if platform not in {"lichess", "chesscom"}:
            self.review_status_label.config(text="Unsupported platform request.")
            return

        if platform == "lichess":
            username = (self.review_lichess_var.get() or self.lichess_username or "").strip()
            if not username:
                self.review_status_label.config(text="Set your Lichess username in Settings first.")
                return
            status_prefix = f"Lichess | {username}"
        else:
            username = (self.review_chesscom_var.get() or self.chesscom_username or "").strip()
            if not username:
                self.review_status_label.config(text="Set your Chess.com username in Settings first.")
                return
            status_prefix = f"Chess.com | {username}"

        self.review_status_label.config(text=f"{status_prefix}: fetching games...")

        def worker():
            try:
                if platform == "lichess":
                    games = self._collect_recent_lichess_games(username)
                else:
                    games = self._collect_recent_chesscom_games(username)

                def update_ui():
                    self.inline_review_games = games
                    for row in self.review_tree.get_children():
                        self.review_tree.delete(row)
                    for game in games:
                        self.review_tree.insert(
                            "",
                            tk.END,
                            values=(game["platform"], game["players"], game["result"], game["date"]),
                        )
                    if games:
                        self.review_status_label.config(
                            text=f"{status_prefix}: loaded {len(games)} games. Double-click to review."
                        )
                    else:
                        self.review_status_label.config(
                            text=f"{status_prefix}: no recent games found."
                        )

                self.root.after(0, update_ui)
            except requests.exceptions.RequestException as req_err:
                self.root.after(
                    0,
                    lambda: self.review_status_label.config(
                        text=f"{status_prefix}: network error ({req_err.__class__.__name__})."
                    ),
                )
            except Exception as exc:
                self.root.after(
                    0,
                    lambda: self.review_status_label.config(
                        text=f"{status_prefix}: failed to load games ({exc})."
                    ),
                )

        threading.Thread(target=worker, daemon=True).start()

    def load_selected_inline_review_game(self):
        """Load a game selected in the inline review table."""
        if not self.inline_review_games:
            messagebox.showinfo("No Games", "Fetch games before starting a review.")
            return

        selection = self.review_tree.selection()
        if not selection:
            messagebox.showinfo("Select a Game", "Highlight a game in the table before loading.")
            return

        index = self.review_tree.index(selection[0])
        if index >= len(self.inline_review_games):
            messagebox.showerror("Selection Error", "Unable to locate selected game details.")
            return

        game_entry = self.inline_review_games[index]
        pgn_text = game_entry.get("pgn")
        if not pgn_text:
            messagebox.showwarning(
                "PGN Missing",
                "This game does not include a PGN from the API. Try another entry or open in browser.",
            )
            return

        try:
            game = chess.pgn.read_game(StringIO(pgn_text))
            if not game:
                raise ValueError("PGN parsing returned no game")
        except Exception as exc:
            messagebox.showerror("PGN Error", f"Could not parse this PGN: {exc}")
            return

        self.review_mode = True
        self.review_board = chess.Board()
        self.review_moves = list(game.mainline_moves())
        self.review_move_index = 0
        self.open_review_window()

    def load_selected_review_game(self):
        """Load the selected game from the review list and open the review window."""
        try:
            if not hasattr(self, 'review_games') or not self.review_games:
                messagebox.showinfo("No Games", "No games available to load.")
                return
            sel = self.review_list.curselection()
            if not sel:
                messagebox.showinfo("Select a Game", "Please select a game from the list.")
                return
            idx = sel[0]
            game_entry = self.review_games[idx]
            pgn_text = game_entry.get('pgn')
            if not pgn_text:
                messagebox.showwarning("PGN Missing", "This game has no PGN available from the API.")
                return
            # Parse PGN
            game = chess.pgn.read_game(StringIO(pgn_text))
            if not game:
                messagebox.showerror("PGN Error", "Failed to parse PGN from the selected game.")
                return
            # Enter review mode
            self.review_mode = True
            self.review_board = chess.Board()
            self.review_moves = list(game.mainline_moves())
            self.review_move_index = 0
            # Open review window
            self.open_review_window()
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load selected game: {e}")
    
    def show_move_history(self):
        """Display move history in a new window."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Move History")
        history_window.geometry("350x400")
        
        tk.Label(history_window, text="Move History", font=("Arial", 14, "bold")).pack(pady=10)
        
        text_widget = scrolledtext.ScrolledText(history_window, width=45, height=25, wrap=tk.WORD, font=("Courier", 10))
        text_widget.pack(padx=10, pady=10)
        
        # Format moves in two columns
        board = chess.Board()
        move_text = ""
        for i, move in enumerate(self.move_history):
            if i % 2 == 0:
                move_text += f"{i//2 + 1}. {board.san(move)} "
            else:
                move_text += f"{board.san(move)}\n"
            board.push(move)
        
        text_widget.insert(tk.END, move_text if move_text else "No moves yet.")
        text_widget.config(state=tk.DISABLED)
    
    def open_theme_selector(self):
        """Open theme selection dialog."""
        theme_window = tk.Toplevel(self.root)
        theme_window.title("Select Board Theme")
        theme_window.geometry("500x400")
        theme_window.resizable(False, False)
        
        tk.Label(theme_window, text="Choose a Board Theme", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create preview canvas
        preview_frame = tk.Frame(theme_window)
        preview_frame.pack(pady=10)
        
        preview_canvas = tk.Canvas(preview_frame, width=320, height=320, highlightthickness=2, highlightbackground="#000000")
        preview_canvas.pack()
        
        current_preview_theme = [self.current_theme]  # Mutable container for closure
        
        def draw_preview(theme_name):
            """Draw a preview of the selected theme."""
            preview_canvas.delete("all")
            theme = self.THEMES[theme_name]
            square_size = 40
            
            # Draw checkerboard
            for row in range(8):
                for col in range(8):
                    x1 = col * square_size
                    y1 = row * square_size
                    x2 = x1 + square_size
                    y2 = y1 + square_size
                    
                    color = theme['light'] if (row + col) % 2 == 0 else theme['dark']
                    preview_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            
            # Draw some sample pieces
            sample_pieces = [
                (0, 0, '♜', 'black'), (1, 0, '♞', 'black'), (6, 0, '♞', 'black'), (7, 0, '♜', 'black'),
                (3, 0, '♛', 'black'), (4, 0, '♚', 'black'),
                (0, 1, '♟', 'black'), (1, 1, '♟', 'black'), (6, 1, '♟', 'black'), (7, 1, '♟', 'black'),
                (0, 6, '♙', 'white'), (1, 6, '♙', 'white'), (6, 6, '♙', 'white'), (7, 6, '♙', 'white'),
                (3, 7, '♕', 'white'), (4, 7, '♔', 'white'),
                (1, 7, '♘', 'white'), (6, 7, '♘', 'white'), (0, 7, '♖', 'white'), (7, 7, '♖', 'white'),
            ]
            
            for col, row, piece, color in sample_pieces:
                x = col * square_size + square_size // 2
                y = row * square_size + square_size // 2
                piece_color = theme['white_piece'] if color == 'white' else theme['black_piece']
                
                # Add shadow for depth (using gray)
                preview_canvas.create_text(x + 1, y + 1, text=piece, font=("Arial", 20), fill="#808080")
                preview_canvas.create_text(x, y, text=piece, font=("Arial", 20), fill=piece_color)
        
        # Theme buttons
        button_frame = tk.Frame(theme_window)
        button_frame.pack(pady=10)
        
        theme_var = tk.StringVar(value=self.current_theme)
        
        row = 0
        col = 0
        for theme_name in self.THEMES.keys():
            btn = tk.Radiobutton(
                button_frame,
                text=theme_name,
                variable=theme_var,
                value=theme_name,
                font=("Arial", 11),
                command=lambda t=theme_name: [draw_preview(t), current_preview_theme.__setitem__(0, t)],
                indicatoron=True,
                width=12
            )
            btn.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Initial preview
        draw_preview(self.current_theme)
        
        # Apply button
        def apply_theme():
            self.current_theme = theme_var.get()
            self.save_settings()
            self.draw_board()
            messagebox.showinfo("Theme Applied", f"{self.current_theme} theme applied!")
            theme_window.destroy()
        
        tk.Button(theme_window, text="Apply Theme", command=apply_theme, font=("Arial", 12), width=20, height=2).pack(pady=20)
    
    def open_piece_selector(self):
        """Open piece style selection dialog."""
        piece_window = tk.Toplevel(self.root)
        piece_window.title("Select Piece Style")
        piece_window.geometry("400x320")
        piece_window.resizable(False, False)
        
        tk.Label(piece_window, text="Choose a Piece Style", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Preview frame
        preview_frame = tk.Frame(piece_window)
        preview_frame.pack(pady=10)
        
        preview_canvas = tk.Canvas(preview_frame, width=400, height=120, bg="white")
        preview_canvas.pack()
        
        def draw_piece_preview(piece_set_name):
            """Draw a preview of the selected piece set."""
            preview_canvas.delete("all")
            piece_set = self.PIECE_SETS[piece_set_name]
            
            # Draw sample pieces
            pieces = ['K', 'Q', 'R', 'B', 'N', 'P', 'p', 'n']
            x_offset = 20
            for i, piece_symbol in enumerate(pieces):
                x = x_offset + i * 45
                y = 60
                
                # Draw piece
                preview_canvas.create_text(
                    x, y,
                    text=piece_set.get(piece_symbol, piece_symbol),
                    font=("Arial", 32, "bold"),
                    fill="#000000"
                )
        
        # Piece style buttons
        button_frame = tk.Frame(piece_window)
        button_frame.pack(pady=20)
        
        piece_var = tk.StringVar(value=self.piece_style)
        
        row, col = 0, 0
        for piece_name in self.PIECE_SETS.keys():
            rb = tk.Radiobutton(
                button_frame,
                text=piece_name,
                variable=piece_var,
                value=piece_name,
                font=("Arial", 11),
                command=lambda p=piece_name: draw_piece_preview(p),
                indicatoron=True,
                width=15
            )
            rb.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Draw initial preview
        draw_piece_preview(self.piece_style)
        
        # Apply button
        def apply_piece_style():
            self.piece_style = piece_var.get()
            self.save_settings()
            self.draw_board()
            messagebox.showinfo("Piece Style Applied", f"{self.piece_style} style applied!")
            piece_window.destroy()
        
        tk.Button(piece_window, text="Apply Piece Style", command=apply_piece_style, font=("Arial", 12), width=20, height=2).pack(pady=20)
    
    def draw_evaluation_bar(self, evaluation=0.0):
        """Draw the evaluation bar showing position advantage."""
        self.eval_canvas.delete("all")
        
        bar_width = 40
        bar_height = self.SQUARE_SIZE * 8
        
        # Clamp evaluation between -10 and +10
        eval_clamped = max(-10, min(10, evaluation))
        
        # Calculate the split point (0 is in the middle)
        # Positive = white advantage (top), Negative = black advantage (bottom)
        white_height = int((bar_height / 2) * (1 + eval_clamped / 10))
        black_height = bar_height - white_height
        
        # Draw black advantage area (top)
        self.eval_canvas.create_rectangle(
            0, 0, bar_width, black_height,
            fill="#2C2C2C",
            outline=""
        )
        
        # Draw white advantage area (bottom)
        self.eval_canvas.create_rectangle(
            0, black_height, bar_width, bar_height,
            fill="#ECECEC",
            outline=""
        )
        
        # Draw center line (equality)
        center_y = bar_height // 2
        self.eval_canvas.create_line(
            0, center_y, bar_width, center_y,
            fill="#FF0000",
            width=2
        )
        
        # Update label
        if abs(evaluation) > 5:
            eval_text = "Â±âˆž" if evaluation > 0 else "âˆ“âˆž"
        else:
            eval_text = f"{evaluation:+.1f}"
        
        self.eval_label.config(text=eval_text)
    
    def get_position_evaluation(self):
        """Get evaluation of current position from Stockfish."""
        if not self.engine:
            return 0.0
        
        try:
            with self.engine_lock:
                info = self.engine.analyse(self.board, chess.engine.Limit(time=0.3))
            score = info.get("score")
            
            if score:
                # Convert to pawn advantage
                if score.is_mate():
                    # Mate detected
                    mate_in = score.relative.mate()
                    return 100.0 if mate_in > 0 else -100.0
                else:
                    # Centipawn to pawn conversion
                    cp = score.relative.score()
                    return cp / 100.0 if cp else 0.0
            
            return 0.0
        except Exception as e:
            print(f"Evaluation error: {e}")
            return 0.0
    
    def analyze_current_position(self):
        """Analyze current position and update evaluation bar."""
        if not self.engine:
            return
        if getattr(self, 'eval_pause_on_ai', None) and self.eval_pause_on_ai.get() and self.ai_thinking:
            return
        
        def analyze():
            eval_score = self.get_position_evaluation()
            self.current_evaluation = eval_score
            self.root.after(0, lambda: self.draw_evaluation_bar(eval_score))
        
        threading.Thread(target=analyze, daemon=True).start()

    def animate_move(self, move, steps=8, duration_ms=140):
        """Simple tween animation to slide a piece from from_square to to_square."""
        try:
            from_sq = move.from_square
            to_sq = move.to_square

            def rc(sq):
                return (7 - (sq // 8), sq % 8)

            fr, fc = rc(from_sq)
            tr, tc = rc(to_sq)
            if self.board_flipped:
                fr, fc = (7 - fr, 7 - fc)
                tr, tc = (7 - tr, 7 - tc)

            x1 = fc * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            y1 = fr * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            x2 = tc * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            y2 = tr * self.SQUARE_SIZE + self.SQUARE_SIZE // 2

            piece = self.board.piece_at(from_sq)
            if not piece:
                return
            symbol = (self.PIECE_SETS.get(self.piece_style) or self.PIECES).get(piece.symbol(), piece.symbol())
            theme = self.THEMES.get(self.current_theme, list(self.THEMES.values())[0])
            color = theme['white_piece'] if piece.color == chess.WHITE else theme['black_piece']

            steps = max(1, int(steps))
            delay = max(10, int(duration_ms / steps))
            for i in range(1, steps + 1):
                t = i / steps
                x = int(x1 + (x2 - x1) * t)
                y = int(y1 + (y2 - y1) * t)
                self.draw_board()
                self.canvas.create_text(x, y, text=symbol, font=("Arial", self.piece_size, "bold"), fill=color)
                self.canvas.update_idletasks()
                self.canvas.after(delay)
        except Exception:
            pass

    def schedule_evaluation(self):
        """Debounce evaluation requests to reduce engine load while repainting."""
        if not getattr(self, 'live_eval_var', None) or not self.live_eval_var.get():
            return
        if self.ai_thinking or self.review_mode:
            return
        import time
        now_ms = int(time.time() * 1000)
        elapsed = now_ms - (self._last_eval_ms or 0)
        if self._eval_after_id is not None:
            try:
                self.root.after_cancel(self._eval_after_id)
            except Exception:
                pass
            self._eval_after_id = None
        delay = 50 if elapsed > self._eval_interval_ms else (self._eval_interval_ms - elapsed)
        def _run():
            self._last_eval_ms = int(time.time() * 1000)
            self.analyze_current_position()
            self._eval_after_id = None
        self._eval_after_id = self.root.after(delay, _run)
    
    def draw_board(self):
        """Draw the chess board and pieces."""
        self.canvas.delete("all")
        theme = self.THEMES[self.current_theme] if hasattr(self, 'current_theme') and self.current_theme in self.THEMES else list(self.THEMES.values())[0]
        piece_set = self.PIECE_SETS[self.piece_style] if hasattr(self, 'piece_style') and self.piece_style in self.PIECE_SETS else list(self.PIECE_SETS.values())[0]
        
        # Draw border
        self.canvas.create_rectangle(
            0, 0,
            self.SQUARE_SIZE * 8, self.SQUARE_SIZE * 8,
            outline=theme['border'],
            width=3
        )
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                # Flip coordinates if board is flipped
                display_row = row if not self.board_flipped else (7 - row)
                display_col = col if not self.board_flipped else (7 - col)
                
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                # Determine square color
                if (row + col) % 2 == 0:
                    color = theme['light']
                else:
                    color = theme['dark']
                
                square_index = (7 - display_row) * 8 + display_col
                
                # Priority order: Select > Hint > Last Move > Legal moves
                # Show last opponent's move
                if self.selected_square == square_index:
                    color = theme['select']
                elif self.show_hint and self.hint_move and \
                     (square_index == self.hint_move.from_square or square_index == self.hint_move.to_square):
                    # Hint gets priority over legal moves and last move
                    color = theme['hint']
                elif self.last_move and \
                     (square_index == self.last_move.from_square or square_index == self.last_move.to_square):
                    # Last move highlight (opponent's or your last move)
                    color = self.LAST_MOVE_COLOR
                elif square_index in [move.to_square for move in self.legal_moves]:
                    color = theme['highlight']
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=""
                )
                
                # Draw rank and file labels with better styling
                rank_label = str(8 - display_row) if not self.board_flipped else str(display_row + 1)
                file_label = chr(97 + display_col) if not self.board_flipped else chr(97 + (7 - display_col))
                
                if col == 0:
                    self.canvas.create_text(
                        x1 + 8, y1 + 8,
                        text=rank_label,
                        font=("Arial", 11, "bold"),
                        fill=theme['coord'],
                        anchor="nw"
                    )
                if row == 7:
                    self.canvas.create_text(
                        x2 - 8, y2 - 8,
                        text=file_label,
                        font=("Arial", 11, "bold"),
                        fill=theme['coord'],
                        anchor="se"
                    )
        
        # Draw pieces with shadows for depth
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                board_row = 7 - (square // 8)
                board_col = square % 8
                
                # Apply flip transformation
                display_row = board_row if not self.board_flipped else (7 - board_row)
                display_col = board_col if not self.board_flipped else (7 - board_col)
                
                x = display_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                y = display_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                
                symbol = piece_set.get(piece.symbol(), piece.symbol())
                piece_color = theme['white_piece'] if piece.color == chess.WHITE else theme['black_piece']
                
                # Draw shadow for depth effect (using gray instead of alpha)
                shadow_offset = 2
                self.canvas.create_text(
                    x + shadow_offset, y + shadow_offset,
                    text=symbol,
                    font=("Arial", self.piece_size, "bold"),
                    fill="#808080"
                )
                
                # Draw main piece
                self.canvas.create_text(
                    x, y,
                    text=symbol,
                    font=("Arial", self.piece_size, "bold"),
                    fill=piece_color
                )
        
        # Draw top move arrows (review mode)
        try:
            if hasattr(self, 'top_move_arrows') and self.top_move_arrows and self.review_mode:
                for move, rank in self.top_move_arrows:
                    from_sq = move.from_square
                    to_sq = move.to_square
                    from_row = 7 - (from_sq // 8)
                    from_col = from_sq % 8
                    to_row = 7 - (to_sq // 8)
                    to_col = to_sq % 8
                    x1 = from_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    y1 = from_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    x2 = to_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    y2 = to_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    # Color and width by rank
                    colors = {1: '#34C759', 2: '#0A84FF', 3: '#FF9F0A', 4: '#AF52DE', 5: '#FF3B30'}
                    width = max(2, 6 - rank)
                    arrow_shape = (16, 20, 6)
                    self.canvas.create_line(x1, y1, x2, y2, fill=colors.get(rank, '#34C759'), width=width, arrow=tk.LAST, arrowshape=arrow_shape)
        except Exception:
            pass

        # Update status
        self.update_status()
        
        # Schedule evaluation bar update (debounced) if engine available
        if self.engine and not self.ai_thinking and not self.review_mode:
            self.schedule_evaluation()
    
    def get_square_from_click(self, event):
        """Convert click coordinates to square index."""
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        if 0 <= col < 8 and 0 <= row < 8:
            # Apply flip transformation
            if self.board_flipped:
                col = 7 - col
                row = 7 - row
            return (7 - row) * 8 + col
        return None
    
    def on_square_click(self, event):
        """Handle board interaction for human moves."""
        if self.review_mode:
            return
        if self.ai_thinking:
            return
        if self.board.turn != self.player_color:
            return

        square = self.get_square_from_click(event)
        if square is None:
            return

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.legal_moves = [move for move in self.board.legal_moves if move.from_square == square]
                self.draw_board()
            return

        if self.selected_square == square:
            self.selected_square = None
            self.legal_moves = []
            self.draw_board()
            return

        candidate_moves = [move for move in self.legal_moves if move.to_square == square]
        if not candidate_moves:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.legal_moves = [move for move in self.board.legal_moves if move.from_square == square]
            else:
                self.selected_square = None
                self.legal_moves = []
            self.draw_board()
            return

        move = candidate_moves[0] if len(candidate_moves) == 1 else self._choose_promotion_move(candidate_moves)
        if move is None:
            return

        self._apply_player_move(move)

    def _choose_promotion_move(self, moves):
        """Offer a dialog to pick promotion piece and return the matching move."""
        if not moves:
            return None
        # If none are promotion moves, return first
        if all(not m.promotion for m in moves):
            return moves[0]

        # Dialog to pick piece
        dialog = tk.Toplevel(self.root)
        dialog.title("Promote pawn")
        dialog.geometry("260x140")
        dialog.resizable(False, False)
        choice = {"piece": chess.QUEEN}

        def select(p):
            choice["piece"] = p
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(expand=True)
        for name, ptype in [("Queen", chess.QUEEN), ("Rook", chess.ROOK), ("Bishop", chess.BISHOP), ("Knight", chess.KNIGHT)]:
            tk.Button(btn_frame, text=name, width=8, command=lambda t=ptype: select(t)).pack(side=tk.LEFT, padx=6, pady=18)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

        # Return the move whose promotion matches selection
        for m in moves:
            if m.promotion == choice["piece"]:
                return m
        # Fallback
        return moves[0]

    def _apply_player_move(self, move):
        """Make the player's move and queue the engine response."""
        self.end_move_timer()
        # Optional animation
        if self.enable_animations.get():
            try:
                self.animate_move(move)
            except Exception:
                pass
        self.board.push(move)
        self.move_history.append(move)
        self.last_move = move
        self.selected_square = None
        self.legal_moves = []
        self.hint_move = None
        self.show_hint = False

        self.update_move_list()
        self.update_captured_pieces()

        if self.check_game_over():
            self.ai_thinking = False
            self.draw_board()
            return

        if self.engine:
            self.ai_thinking = True
        else:
            self.ai_thinking = False

        self.draw_board()

        if not self.engine:
            self.start_move_timer()
            return

        self.start_move_timer()
        threading.Thread(target=self.ai_move, daemon=True).start()

    def ai_move(self):
        """Worker executed in background to get Stockfish's move."""
        if not self.engine:
            self.root.after(0, lambda: self.apply_ai_move(None))
            return

        try:
            think_time = float(self.time_var.get())
        except (TypeError, ValueError):
            think_time = 1.0
        think_time = max(0.1, min(think_time, 10.0))

        try:
            with self.engine_lock:
                result = self.engine.play(self.board, chess.engine.Limit(time=think_time))
        except Exception as exc:
            self.root.after(0, lambda e=exc: self._handle_engine_failure(e))
            return

        move = result.move if result else None
        self.root.after(0, lambda m=move: self.apply_ai_move(m))

    def _handle_engine_failure(self, error):
        """Reset state if the engine cannot produce a move."""
        self.end_move_timer()
        self.ai_thinking = False
        if hasattr(self, "status_label"):
            self.status_label.config(text="Engine error - reload Stockfish to continue.")
        message = str(error) if error else "Unknown engine error."
        messagebox.showerror("Engine Error", f"Stockfish failed to move:\n{message}")

    def apply_ai_move(self, move):
        """Apply AI's move to the board."""
        self.end_move_timer()  # End timer for AI's thinking time
        
        if not move:
            self._handle_engine_failure("No move returned by engine")
            return
        # Optional animation
        if self.enable_animations.get():
            try:
                self.animate_move(move)
            except Exception:
                pass
        self.board.push(move)
        self.move_history.append(move)
        self.last_move = move  # Track AI's move for highlighting
        
        self.ai_thinking = False
        self.hint_move = None
        self.show_hint = False
        self.update_move_list()
        self.update_captured_pieces()
        self.draw_board()
        self.check_game_over()
        
        self.start_move_timer()  # Start timer for player's next move
    
    def update_status(self):
        """Update the status label."""
        if self.ai_thinking:
            self.status_label.config(text="AI is thinking...")
            return
        
        # Detect opening
        opening = self.detect_opening()
        
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            self.status_label.config(text=f"Checkmate! {winner} wins!")
        elif self.board.is_stalemate():
            self.status_label.config(text="Stalemate - Draw!")
        elif self.board.is_insufficient_material():
            self.status_label.config(text="Draw - Insufficient material")
        elif self.board.is_check():
            turn = "White" if self.board.turn == chess.WHITE else "Black"
            opening_text = f" | {opening}" if opening else ""
            self.status_label.config(text=f"Check! {turn} to move{opening_text}")
        else:
            turn = "White" if self.board.turn == chess.WHITE else "Black"
            opening_text = f" | {opening}" if opening else ""
            self.status_label.config(text=f"{turn} to move{opening_text}")
    
    def detect_opening(self):
        """Detect the current opening based on moves played."""
        if len(self.board.move_stack) == 0 or len(self.board.move_stack) > 15:
            return ""
        
        # Build move sequence string
        move_sequence = []
        temp_board = chess.Board()
        for move in self.board.move_stack:
            move_sequence.append(move.uci())
            temp_board.push(move)
        
        # Try to match progressively longer sequences
        best_match = ""
        for i in range(len(move_sequence), 0, -1):
            seq = " ".join(move_sequence[:i])
            if seq in self.OPENING_BOOK:
                best_match = self.OPENING_BOOK[seq]
                break
        
        if best_match:
            self.current_opening = best_match
            return best_match
        return self.current_opening  # Keep showing last detected opening
    
    def check_game_over(self):
        """Check if game is over and show message."""
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
            return True
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate - Draw!")
            return True
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Draw - Insufficient material")
            return True
        elif self.board.is_fifty_moves():
            messagebox.showinfo("Game Over", "Draw - Fifty move rule")
            return True
        elif self.board.is_repetition():
            messagebox.showinfo("Game Over", "Draw - Threefold repetition")
            return True
        return False
    
    def new_game(self):
        """Start a new game."""
        if messagebox.askyesno("New Game", "Start a new game?"):
            self.board.reset()
            self.selected_square = None
            self.legal_moves = []
            self.ai_thinking = False
            self.hint_move = None
            self.show_hint = False
            self.move_history = []
            self.last_move = None  # Clear last move highlight
            self.current_opening = ""
            self.white_time = 0
            self.black_time = 0
            self.move_start_time = None
            self.update_move_list()
            self.update_captured_pieces()
            self.draw_board()
            
            self.start_move_timer()  # Start timer for first move
            
            # If AI plays white, make its move
            if self.player_color == chess.BLACK and self.engine:
                self.ai_thinking = True
                threading.Thread(target=self.ai_move, daemon=True).start()
    
    def undo_move(self):
        """Undo the last move(s)."""
        if len(self.board.move_stack) == 0:
            return
        
        # Undo player's move
        self.board.pop()
        if self.move_history:
            self.move_history.pop()
        
        # Undo AI's move if it exists
        if len(self.board.move_stack) > 0 and not self.ai_thinking:
            self.board.pop()
            if self.move_history:
                self.move_history.pop()
        
        # Update last move to the previous move
        if len(self.move_history) > 0:
            self.last_move = self.move_history[-1]
        else:
            self.last_move = None
        
        self.selected_square = None
        self.legal_moves = []
        self.hint_move = None
        self.show_hint = False
        self.update_move_list()
        self.update_captured_pieces()
        self.draw_board()
    
    def flip_board(self):
        """Flip the board to view from opposite perspective."""
        self.board_flipped = not self.board_flipped
        self.draw_board()
    
    def update_captured_pieces(self):
        """Update the display of captured pieces with material advantage."""
        # Get all pieces on board
        pieces_on_board = []
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                pieces_on_board.append(piece.symbol())
        
        # Starting pieces for each type
        starting_pieces = {
            'p': 8, 'n': 2, 'b': 2, 'r': 2, 'q': 1, 'k': 1,
            'P': 8, 'N': 2, 'B': 2, 'R': 2, 'Q': 1, 'K': 1
        }
        
        # Count captured pieces
        self.captured_white = []  # pieces captured by white (black pieces)
        self.captured_black = []  # pieces captured by black (white pieces)
        
        piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}
        
        for piece_type in ['p', 'n', 'b', 'r', 'q']:
            # Black pieces captured
            count_black = starting_pieces[piece_type] - pieces_on_board.count(piece_type)
            self.captured_white.extend([piece_type] * count_black)
            
            # White pieces captured
            count_white = starting_pieces[piece_type.upper()] - pieces_on_board.count(piece_type.upper())
            self.captured_black.extend([piece_type.upper()] * count_white)
        
        # Calculate material advantage
        white_value = sum(piece_values[p.lower()] for p in self.captured_white)
        black_value = sum(piece_values[p.lower()] for p in self.captured_black)
        advantage = white_value - black_value
        
        piece_symbols = self.PIECE_SETS.get(self.piece_style, self.PIECE_SETS["Classic"])
        
        # Display captured by white (black pieces)
        captured_white_str = ''.join(piece_symbols.get(p, p) for p in self.captured_white)
        self.captured_white_label.config(text=captured_white_str)
        if advantage > 0:
            self.material_label_white.config(text=f"+{advantage}", fg="green")
        else:
            self.material_label_white.config(text="")
        
        # Display captured by black (white pieces)
        captured_black_str = ''.join(piece_symbols.get(p, p) for p in self.captured_black)
        self.captured_black_label.config(text=captured_black_str)
        if advantage < 0:
            self.material_label_black.config(text=f"+{abs(advantage)}", fg="green")
        else:
            self.material_label_black.config(text="")
        
        # Update timers
        self.update_timers()
    
    def update_timers(self):
        """Update the timer display for both players."""
        # Format time as minutes:seconds
        white_mins = int(self.white_time // 60)
        white_secs = int(self.white_time % 60)
        black_mins = int(self.black_time // 60)
        black_secs = int(self.black_time % 60)
        
        self.white_timer_label.config(text=f"Time {white_mins}:{white_secs:02d}")
        self.black_timer_label.config(text=f"Time {black_mins}:{black_secs:02d}")
        
        # Highlight current player's timer
        if self.board.turn == chess.WHITE:
            self.white_timer_label.config(fg="blue")
            self.black_timer_label.config(fg="black")
        else:
            self.black_timer_label.config(fg="blue")
            self.white_timer_label.config(fg="black")
    
    def start_move_timer(self):
        """Start timing the current move."""
        import time
        self.move_start_time = time.time()
    
    def end_move_timer(self):
        """End timing and add to player's total time."""
        if self.move_start_time is not None:
            import time
            elapsed = time.time() - self.move_start_time
            
            # Add to the player who just moved
            if self.board.turn == chess.BLACK:  # White just moved
                self.white_time += elapsed
            else:  # Black just moved
                self.black_time += elapsed
            
            self.move_start_time = None
    
    def update_move_list(self):
        """Update the move list display in Chess.com style."""
        self.move_list_text.config(state=tk.NORMAL)
        self.move_list_text.delete(1.0, tk.END)
        
        # Format moves in two-column layout (White | Black)
        moves = list(self.board.move_stack)
        temp_board = chess.Board()

        pending_white = None
        pending_move_no = 1
        for ply_index, move in enumerate(moves):
            try:
                san = temp_board.san(move)
            except ValueError:
                san = move.uci()
            temp_board.push(move)

            if ply_index % 2 == 0:
                pending_white = san
                pending_move_no = (ply_index // 2) + 1
            else:
                white_text = pending_white or ""
                black_text = san
                line = f"{pending_move_no:3d}. {white_text:10s} {black_text}\n"
                self.move_list_text.insert(tk.END, line)
                pending_white = None

        # If game ends on White's move, flush the last incomplete row.
        if pending_white is not None:
            line = f"{pending_move_no:3d}. {pending_white:10s}\n"
            self.move_list_text.insert(tk.END, line)
        
        self.move_list_text.config(state=tk.DISABLED)
        self.move_list_text.see(tk.END)  # Auto-scroll to latest move
    
    
    def change_player_color(self):
        """Change which color the player plays as."""
        new_color = chess.WHITE if self.color_var.get() == "white" else chess.BLACK
        
        if new_color != self.player_color:
            self.player_color = new_color
            self.new_game()
    
    def cleanup(self):
        """Clean up resources."""
        if self.engine:
            self.engine.quit()
        self.save_settings()


def main():
    """Main entry point for GUI version."""
    root = tk.Tk()
    
    # Ask for Stockfish path (optional)
    # You can add a file dialog here if needed
    app = ChessAnalyser(root)
    
    # Cleanup on close
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

