"""Pygame GUI for the Quad-Deck card game - V11.0 Architecture."""

import pygame
import sys
from src.game_factory import setup_game
from src.card import Card

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Quad-Deck Prototype")

# Define color constants (V11.0 standards)
COLOR_ATTACK = (255, 85, 85)      # Red
COLOR_HEALING = (85, 255, 85)     # Green
COLOR_RESOURCE = (85, 85, 255)    # Blue
COLOR_ENCOUNTER = (51, 51, 51)    # Charcoal
COLOR_BG = (30, 30, 40)           # Dark Modern Grey
COLOR_TEXT = (255, 255, 255)      # White

# Category color mapping
CATEGORY_COLORS = {
    "Attack": COLOR_ATTACK,
    "Healing": COLOR_HEALING,
    "Resource": COLOR_RESOURCE,
    "Encounter": COLOR_ENCOUNTER
}

# Category priority for sorting (Resource -> Attack -> Healing)
CATEGORY_PRIORITY = {
    "Resource": 0,
    "Attack": 1,
    "Healing": 2
}

# UI Button definitions (centered at top)
draw_btn_rect = pygame.Rect(440, 20, 120, 40)
end_btn_rect = pygame.Rect(580, 20, 120, 40)
quit_btn_rect = pygame.Rect(720, 20, 120, 40)
COLOR_BUTTON = (68, 68, 68)  # Dark grey for buttons

# Initialize game state
state, controller = setup_game()

# Set up game loop
clock = pygame.time.Clock()
running = True

# Initialize phase state
current_phase = "COMBAT"
draft_options = []
draft_clickable_cards = []

def sort_hand_cards(hand):
    """Sort hand cards by Category (Resource -> Attack -> Healing), then by Value (Highest to Lowest)."""
    return sorted(hand, key=lambda card: (CATEGORY_PRIORITY.get(card.category, 3), -card.current_value))

def draw_hud():
    """Draw the HUD with player and enemy stats."""
    font = pygame.font.Font(None, 36)
    
    # Player stats (left side)
    player_health_text = font.render(f"Health: {state.player.life_total}", True, COLOR_TEXT)
    player_energy_text = font.render(f"Energy: {state.energy}", True, COLOR_TEXT)
    screen.blit(player_health_text, (50, 30))
    screen.blit(player_energy_text, (50, 70))
    
    # Enemy stats (right side)
    enemy_health_text = font.render(f"Enemy Health: {state.current_enemy_health}", True, COLOR_TEXT)
    screen.blit(enemy_health_text, (1280 - 250, 30))

def draw_hand():
    """Draw the player's hand as rounded rectangles at the bottom of the screen."""
    global clickable_cards
    card_width = 120
    card_height = 180
    start_y = 500
    
    # Clear clickable cards list for this frame
    clickable_cards = []
    
    # Create list of (original_index, card) tuples for sorting
    indexed_hand = [(i, card) for i, card in enumerate(state.player.hand)]
    # Sort by category and value while preserving original indices
    sorted_indexed_hand = sorted(indexed_hand, key=lambda item: (CATEGORY_PRIORITY.get(item[1].category, 3), -item[1].current_value))
    
    # Define boundaries and calculate dynamic spacing
    max_hand_width = 1180  # Leave 50px padding on each side of the 1280 window
    num_cards = len(sorted_indexed_hand)
    
    if num_cards == 0:
        return clickable_cards
    elif num_cards == 1:
        card_spacing = 0
        start_x = (1280 - card_width) // 2
    else:
        # Calculate the span available for the starting X coordinates
        span = max_hand_width - card_width
        ideal_spacing = 140
        calculated_spacing = span // (num_cards - 1)
        
        # Take the smaller spacing (so small hands don't spread too far)
        card_spacing = min(ideal_spacing, calculated_spacing)
        
        # Center the hand perfectly based on actual width
        total_width = (num_cards - 1) * card_spacing + card_width
        start_x = (1280 - total_width) // 2
    
    for i, (original_index, card) in enumerate(sorted_indexed_hand):
        card_x = start_x + (i * card_spacing)
        card_y = start_y
        
        # Get color based on card category
        card_color = CATEGORY_COLORS.get(card.category, COLOR_ENCOUNTER)
        
        # Create card rect for click detection
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        # Add to clickable cards list with original index
        clickable_cards.append((card_rect, original_index))
        
        # Draw card rectangle with rounded corners
        pygame.draw.rect(screen, card_color, card_rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_TEXT, card_rect, 2, border_radius=8)  # Border
        
        # Draw card name
        font = pygame.font.Font(None, 20)
        name_text = font.render(card.name[:12], True, COLOR_TEXT)  # Truncate long names
        name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 25))
        screen.blit(name_text, name_rect)
        
        # Draw card value
        value_font = pygame.font.Font(None, 28)
        value_text = value_font.render(str(card.current_value), True, COLOR_TEXT)
        value_rect = value_text.get_rect(center=(card_x + card_width // 2, card_y + card_height // 2))
        screen.blit(value_text, value_rect)
        
        # Draw category label
        category_font = pygame.font.Font(None, 16)
        category_text = category_font.render(card.category, True, COLOR_TEXT)
        category_rect = category_text.get_rect(center=(card_x + card_width // 2, card_y + card_height - 15))
        screen.blit(category_text, category_rect)
    
    return clickable_cards

def draw_ui_buttons():
    """Draw UI control buttons."""
    font = pygame.font.Font(None, 24)
    
    # Draw button
    pygame.draw.rect(screen, COLOR_BUTTON, draw_btn_rect, border_radius=5)
    draw_text = font.render("Draw (1 E)", True, COLOR_TEXT)
    draw_text_rect = draw_text.get_rect(center=draw_btn_rect.center)
    screen.blit(draw_text, draw_text_rect)
    
    # End turn button
    pygame.draw.rect(screen, COLOR_BUTTON, end_btn_rect, border_radius=5)
    end_text = font.render("End Turn", True, COLOR_TEXT)
    end_text_rect = end_text.get_rect(center=end_btn_rect.center)
    screen.blit(end_text, end_text_rect)
    
    # Quit button
    pygame.draw.rect(screen, COLOR_BUTTON, quit_btn_rect, border_radius=5)
    quit_text = font.render("Quit", True, COLOR_TEXT)
    quit_text_rect = quit_text.get_rect(center=quit_btn_rect.center)
    screen.blit(quit_text, quit_text_rect)

def draw_message_log():
    """Draw the last 5 messages from the state message log."""
    font = pygame.font.Font(None, 20)
    log_y = 80  # Start just below the buttons
    
    # Get the last 5 messages
    recent_logs = state.message_log[-5:]
    
    for message in recent_logs:
        # Render the message text
        text_surface = font.render(message, True, COLOR_TEXT)
        # Center horizontally at current Y position
        text_rect = text_surface.get_rect(center=(640, log_y))
        screen.blit(text_surface, text_rect)
        # Move to next line
        log_y += 25

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if current_phase == "COMBAT":
                # Check UI buttons
                if draw_btn_rect.collidepoint(mouse_pos):
                    controller.handle_draw_action()
                elif end_btn_rect.collidepoint(mouse_pos):
                    controller.resolve_enemy_turn()
                    draft_options = controller.prepare_draft_options()
                    if draft_options:
                        # Convert tuples from database into Card objects for the GUI to render
                        draft_cards = [Card(name, d_type, val, cat, desc) for name, d_type, val, cat, desc in draft_options]
                        current_phase = "DRAFT"
                    else:
                        controller.start_turn()
                elif quit_btn_rect.collidepoint(mouse_pos):
                    running = False
                else:
                    # Check cards (reverse order for overlapping cards)
                    for card_rect, original_index in reversed(clickable_cards):
                        if card_rect.collidepoint(mouse_pos):
                            if controller.can_play_card(original_index):
                                controller.resolve_card(original_index)
                            else:
                                controller.log_event("⚠️ Not enough energy!")
                            break  # Stop checking once the top card is clicked
            elif current_phase == "DRAFT":
                # Check draft cards
                for card_rect, card_name in draft_clickable_cards:
                    if card_rect.collidepoint(mouse_pos):
                        controller.add_card_to_deck(card_name)
                        current_phase = "COMBAT"
                        controller.start_turn()
                        break
    
    # Check for game over conditions
    if state.player.life_total <= 0 or state.current_enemy_health <= 0:
        current_phase = "GAME_OVER"
    
    # Rendering
    screen.fill(COLOR_BG)
    
    if current_phase == "COMBAT":
        # Draw HUD
        draw_hud()
        
        # Draw UI buttons
        draw_ui_buttons()
        
        # Draw message log
        draw_message_log()
        
        # Draw the hand
        clickable_cards = draw_hand()
        
    elif current_phase == "DRAFT":
        # Draw draft phase
        font = pygame.font.Font(None, 48)
        draft_text = font.render("DRAFT PHASE: Choose a card", True, COLOR_TEXT)
        draft_rect = draft_text.get_rect(center=(640, 100))
        screen.blit(draft_text, draft_rect)
        
        # Clear draft clickable cards list for this frame
        draft_clickable_cards = []
        
        # Draw draft options
        card_width = 150
        card_height = 200
        start_x = 340  # Center 3 cards: (1280 - 3*150 - 2*50) / 2 = 340
        start_y = 250
        card_spacing = 200
        
        for i, card in enumerate(draft_cards):
            card_x = start_x + (i * card_spacing)
            card_y = start_y
            
            # Get color based on card category
            card_color = CATEGORY_COLORS.get(card.category, COLOR_ENCOUNTER)
            
            # Create card rect for click detection
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            # Add to draft clickable cards list with card name
            draft_clickable_cards.append((card_rect, card.name))
            
            # Draw card rectangle with rounded corners
            pygame.draw.rect(screen, card_color, card_rect, border_radius=8)
            pygame.draw.rect(screen, COLOR_TEXT, card_rect, 2, border_radius=8)  # Border
            
            # Draw card name
            name_font = pygame.font.Font(None, 20)
            name_text = name_font.render(card.name[:15], True, COLOR_TEXT)  # Truncate long names
            name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 25))
            screen.blit(name_text, name_rect)
            
            # Draw card value
            value_font = pygame.font.Font(None, 32)
            value_text = value_font.render(str(card.current_value), True, COLOR_TEXT)
            value_rect = value_text.get_rect(center=(card_x + card_width // 2, card_y + card_height // 2))
            screen.blit(value_text, value_rect)
            
            # Draw category label
            category_font = pygame.font.Font(None, 18)
            category_text = category_font.render(card.category, True, COLOR_TEXT)
            category_rect = category_text.get_rect(center=(card_x + card_width // 2, card_y + card_height - 15))
            screen.blit(category_text, category_rect)
    
    elif current_phase == "GAME_OVER":
        # Draw game over screen
        font = pygame.font.Font(None, 96)
        if state.current_enemy_health <= 0:
            game_over_text = font.render("YOU WIN!", True, COLOR_HEALING)
        else:
            game_over_text = font.render("GAME OVER", True, COLOR_ATTACK)
        
        game_over_rect = game_over_text.get_rect(center=(640, 360))
        screen.blit(game_over_text, game_over_rect)
    
    # Display update
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
