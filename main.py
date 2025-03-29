import pygame, pygame.gfxdraw
import random
import sys
import time

# Initialize pygame
pygame.init()

clock = pygame.time.Clock()
running = True
dt = 0

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Colors
GREEN = (53, 101, 77)  # Felt green
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont('Arial', 24)
large_font = pygame.font.SysFont('Arial', 36)

# Table elements dimensions
DEALER_AREA = pygame.Rect(100, 50, 600, 150)
PLAYER_AREA = pygame.Rect(100, 350, 600, 150)
BETTING_CIRCLE = pygame.Rect(350, 250, 100, 100)
TABLE_EDGE = pygame.Rect(50, 25, 700, 550)

def draw_table():
    # Draw table edge
    pygame.draw.rect(screen, BLACK, TABLE_EDGE, border_radius=20)
    pygame.draw.rect(screen, GREEN, TABLE_EDGE.inflate(-10, -10), border_radius=15)
    
    # Draw dealer and player areas
    pygame.draw.rect(screen, WHITE, DEALER_AREA, 2, border_radius=10)
    pygame.draw.rect(screen, WHITE, PLAYER_AREA, 2, border_radius=10)
    
    # Draw betting circle
    pygame.draw.circle(screen, WHITE, BETTING_CIRCLE.center, BETTING_CIRCLE.width//2, 2)
    
    # Draw decorative elements
    pygame.draw.arc(screen, GOLD, pygame.Rect(200, 200, 400, 200), 0, 3.14, 2)
    
    # Draw labels
    dealer_text = large_font.render("DEALER", True, WHITE)
    player_text = large_font.render("PLAYER", True, WHITE)
    screen.blit(dealer_text, (DEALER_AREA.centerx - dealer_text.get_width()//2, DEALER_AREA.top - 40))
    screen.blit(player_text, (PLAYER_AREA.centerx - player_text.get_width()//2, PLAYER_AREA.bottom + 10))
    
    # Draw chip rack (simplified)
    pygame.draw.rect(screen, BLACK, (50, 500, 700, 50), border_radius=5)
    pygame.draw.rect(screen, (100, 100, 100), (50, 500, 700, 50), 2, border_radius=5)
    
    # Draw some decorative chips
    pygame.draw.circle(screen, RED, (100, 525), 15)
    pygame.draw.circle(screen, WHITE, (150, 525), 15)
    pygame.draw.circle(screen, GOLD, (200, 525), 15)
    pygame.draw.circle(screen, BLUE, (250, 525), 15)
    pygame.draw.circle(screen, GREEN, (300, 525), 15)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)  # Background (will be covered by table)
    
    # Draw the table
    draw_table()
    
    # Display some sample cards (for visualization)
    pygame.draw.rect(screen, WHITE, (DEALER_AREA.x + 20, DEALER_AREA.y + 15, 80, 120), border_radius=5)
    pygame.draw.rect(screen, WHITE, (DEALER_AREA.x + 120, DEALER_AREA.y + 15, 80, 120), border_radius=5)
    
    pygame.draw.rect(screen, WHITE, (PLAYER_AREA.x + 20, PLAYER_AREA.y + 15, 80, 120), border_radius=5)
    pygame.draw.rect(screen, WHITE, (PLAYER_AREA.x + 120, PLAYER_AREA.y + 15, 80, 120), border_radius=5)
    pygame.draw.rect(screen, WHITE, (PLAYER_AREA.x + 220, PLAYER_AREA.y + 15, 80, 120), border_radius=5)
    
    # Draw a sample bet in the betting circle
    bet_text = font.render("$100", True, GOLD)
    screen.blit(bet_text, (BETTING_CIRCLE.centerx - bet_text.get_width()//2, 
                          BETTING_CIRCLE.centery - bet_text.get_height()//2))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()