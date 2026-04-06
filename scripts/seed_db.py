#!/usr/bin/env python3
"""
Standalone database seeding script for the Quad-Deck card game.

Run this script to populate an empty database with default card data.
"""

import sys
import os

# Add the project root to the Python path to import from src
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.database_manager import seed_default_data

if __name__ == "__main__":
    print("Seeding database with default card data...")
    seed_default_data()
    print("Database seeded successfully. You can now run main.py.")
