#!/usr/bin/env python3
"""
Verification script for Chess Analyser
Tests all components and reports status
"""

import os
import sys
import importlib.util

def check_file(filepath, description):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_module(module_name, package_name=None):
    """Check if a Python module is installed."""
    pkg = package_name or module_name
    try:
        spec = importlib.util.find_spec(module_name)
        print(f"✓ {pkg} is installed")
        return True
    except (ImportError, ModuleNotFoundError):
        print(f"✗ {pkg} is NOT installed")
        return False

def check_stockfish():
    """Check if Stockfish is available."""
    import subprocess
    
    possible_paths = [
        "stockfish\\stockfish-windows-x86-64-avx2.exe",
        "stockfish\\stockfish.exe",
        "stockfish.exe",
        "stockfish",
        "/usr/bin/stockfish",
        "/usr/local/bin/stockfish",
    ]
    
    for path in possible_paths:
        try:
            result = subprocess.run([path, "--version"], capture_output=True, timeout=2)
            if result.returncode == 0:
                print(f"✓ Stockfish found: {path}")
                return True
        except:
            pass
    
    print("✗ Stockfish NOT found - Download from https://stockfishchess.org/download/")
    return False

def main():
    print("=" * 60)
    print("CHESS ANALYSER - VERIFICATION REPORT")
    print("=" * 60)
    
    all_ok = True
    
    print("\n📁 PROJECT FILES:")
    print("-" * 60)
    all_ok &= check_file("chessy.py", "GUI Application")
    all_ok &= check_file("main.py", "CLI Application")
    all_ok &= check_file("requirements.txt", "Dependencies")
    all_ok &= check_file("chess_settings.json", "Settings")
    all_ok &= check_file(".venv", "Virtual Environment")
    all_ok &= check_file("stockfish", "Stockfish Directory")
    
    print("\n📦 PYTHON PACKAGES:")
    print("-" * 60)
    all_ok &= check_module("tkinter")
    all_ok &= check_module("chess", "python-chess")
    all_ok &= check_module("requests")
    all_ok &= check_module("json")
    all_ok &= check_module("threading")
    
    print("\n🔧 EXTERNAL TOOLS:")
    print("-" * 60)
    stockfish_ok = check_stockfish()
    
    print("\n" + "=" * 60)
    if all_ok and stockfish_ok:
        print("✅ ALL CHECKS PASSED - App is ready to use!")
        print("\nRun: python chessy.py")
        return 0
    elif all_ok:
        print("⚠️  MOST CHECKS PASSED - Missing Stockfish")
        print("\nYou can still play, but AI opponent won't be available.")
        print("Download from: https://stockfishchess.org/download/")
        print("\nRun: python chessy.py")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nRun: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
