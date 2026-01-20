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
            ("♟️ Accounts", self.open_settings),
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
