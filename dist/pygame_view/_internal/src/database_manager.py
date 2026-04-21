"""Database manager module for the Tri-Deck card game."""

import sqlite3
import os
import random
from typing import List, Tuple, Optional


def initialize_database() -> None:
    """
    Initialize the SQLite database structure.
    
    Creates game_data.db in the root directory if it doesn't exist
    and creates the cards table. Does NOT seed data - use seed_default_data().
    """
    # Get the path to the root directory (where main.py is located)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "game_data.db")
    
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the cards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            deck_type TEXT NOT NULL,
            value INTEGER NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        )
    """)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print(f"Database initialized successfully at: {db_path}")


def seed_default_data() -> None:
    """
    Seed the database with default card data.
    
    Should be called explicitly to populate an empty database with initial card data.
    """
    # Get the path to the root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "game_data.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if database already has cards
    cursor.execute("SELECT COUNT(*) FROM cards")
    count = cursor.fetchone()[0]
    
    # Only seed the database if it's empty
    if count == 0:
        # Seed the database with the current card data
        card_data = [
            # Main deck cards
            ("Fireball", "Main", 3, "Attack", "Deal 3 damage to enemy"),
            ("Sword Strike", "Main", 2, "Attack", "Deal 2 damage to enemy"),
            ("Lightning Bolt", "Main", 4, "Attack", "Deal 4 damage to enemy"),
            ("Ice Shard", "Main", 2, "Attack", "Deal 2 damage to enemy"),
            ("Arrow Shot", "Main", 1, "Attack", "Deal 1 damage to enemy"),
            ("Healing Potion", "Main", 3, "Healing", "Restore 3 health"),
            ("Regeneration", "Main", 2, "Healing", "Restore 2 health"),
            
            # Resource deck cards
            ("Energy Crystal", "Resource", 1, "Resource", "Gain 1 energy"),
            ("Mana Potion", "Resource", 2, "Resource", "Gain 2 energy"),
            ("Power Gem", "Resource", 3, "Resource", "Gain 3 energy"),
            ("Focus Charm", "Resource", 1, "Resource", "Gain 1 energy"),
            ("Meditation", "Resource", 2, "Resource", "Gain 2 energy"),
            
            # Encounter deck cards
            ("Goblin", "Encounter", 2, "Attack", "Enemy with 2 health"),
            ("Orc", "Encounter", 4, "Attack", "Enemy with 4 health"),
            ("Dragon", "Encounter", 8, "Attack", "Enemy with 8 health"),
            ("Skeleton", "Encounter", 1, "Attack", "Enemy with 1 health"),
            ("Troll", "Encounter", 6, "Attack", "Enemy with 6 health")
        ]
        
        # Insert all card data
        cursor.executemany("""
            INSERT INTO cards (name, deck_type, value, category, description)
            VALUES (?, ?, ?, ?, ?)
        """, card_data)
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        
        print(f"Database seeded with {len(card_data)} default cards")
    else:
        # Close the connection
        conn.close()
        print(f"Database already contains {count} cards - skipping seeding")


def get_all_cards() -> List[Tuple[str, str, int, str, str]]:
    """
    Retrieve all cards from the database.
    
    Returns:
        List[Tuple[str, str, int, str, str]]: List of card tuples containing
        (name, deck_type, value, category, description)
    """
    # Get the path to the root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "game_data.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Retrieve all cards
    cursor.execute("SELECT name, deck_type, value, category, description FROM cards ORDER BY deck_type, name")
    cards = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return cards


def get_random_cards(deck_type: str, count: int, exclude_names: List[str] = None) -> List[Tuple[str, str, int, str, str]]:
    """
    Retrieve random cards from the database for a specific deck type.
    
    Args:
        deck_type (str): The deck type to filter by ("Main", "Resource", "Encounter").
        count (int): Number of random cards to retrieve.
        exclude_names (List[str], optional): Card names to exclude from selection.
        
    Returns:
        List[Tuple[str, str, int, str, str]]: List of card tuples containing
        (name, deck_type, value, category, description)
    """
    # Get the path to the root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "game_data.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Build the query
    query = "SELECT name, deck_type, value, category, description FROM cards WHERE deck_type = ?"
    params = [deck_type]
    
    # Add exclusion clause if provided
    if exclude_names:
        placeholders = ','.join(['?' for _ in exclude_names])
        query += f" AND name NOT IN ({placeholders})"
        params.extend(exclude_names)
    
    cursor.execute(query, params)
    cards = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Return random selection
    if len(cards) <= count:
        return cards
    else:
        return random.sample(cards, count)


def get_card_by_name(card_name: str) -> Optional[Tuple[str, str, int, str, str]]:
    """
    Retrieve a specific card by name from the database.
    
    Args:
        card_name (str): The name of the card to retrieve.
        
    Returns:
        Optional[Tuple[str, str, int, str, str]]: Card tuple containing
        (name, deck_type, value, category, description) or None if not found
    """
    # Get the path to the root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(root_dir, "game_data.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Retrieve the specific card
    cursor.execute("SELECT name, deck_type, value, category, description FROM cards WHERE name = ?", (card_name,))
    card = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    return card


if __name__ == "__main__":
    # Test the database initialization
    initialize_database()
    
    # Test retrieving cards
    cards = get_all_cards()
    print(f"Retrieved {len(cards)} cards from database:")
    for card in cards:
        print(f"  {card}")
