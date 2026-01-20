#!/usr/bin/env python3
"""
Launcher script for Chess Analyser
Automatically detects environment and runs the app
"""

import sys
import os
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Import and run the app
    try:
        from chessy import ChessAnalyser
        import tkinter as tk
        
        root = tk.Tk()
        app = ChessAnalyser(root)
        root.mainloop()
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running Chess Analyser: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
