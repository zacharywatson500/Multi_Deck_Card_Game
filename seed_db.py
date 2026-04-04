#!/usr/bin/env python3
"""
Standalone database seeding script for the Tri-Deck card game.

Run this script to populate an empty database with default card data.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database_manager import seed_default_data

if __name__ == "__main__":
    print("Seeding database with default card data...")
    seed_default_data()
    print("Database seeded successfully. You can now run main.py.")
