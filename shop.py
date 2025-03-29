# shop.py
import pygame
from pygame.locals import *

# Font (you can use the same font as in main.py)
font = None

def init_shop(font_path):
    global font
    font = pygame.font.Font(font_path, 20)

class Shop:
    def __init__(self):
        self.items = [
            {"name": "Expand Grid +1", "cost": 500, "description": "Increases both width and height by 1"},
            # Add more items as needed
        ]
        self.visible = False
        self.selected_item = 0

    def draw(self, screen, score, screen_width, screen_height):

        if not self.visible:
            return
        
        # Darken the background
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Draw shop window
        shop_rect = pygame.Rect(
            screen_width // 4,
            screen_height // 4,
            screen_width // 2,
            screen_height // 2
        )
        pygame.draw.rect(screen, (20, 50, 80), shop_rect)
        pygame.draw.rect(screen, (100, 100, 100), shop_rect, 3)
        
        # Draw title
        title = font.render("SHOP", True, (255, 255, 255))
        screen.blit(title, (shop_rect.centerx - title.get_width() // 2, shop_rect.y + 20))
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (shop_rect.centerx - score_text.get_width() // 2, shop_rect.y + 50))
        
        # Draw items
        for i, item in enumerate(self.items):
            color = (200, 200, 255) if i == self.selected_item else (150, 150, 200)
            
            # Item name and cost
            item_text = font.render(f"{item['name']} - {item['cost']} pts", True, color)
            screen.blit(item_text, (shop_rect.x + 30, shop_rect.y + 100 + i * 60))
            
            # Item description
            desc_text = font.render(item['description'], True, (200, 200, 200))
            screen.blit(desc_text, (shop_rect.x + 30, shop_rect.y + 130 + i * 60))
        
        # Draw instructions
            instructions = [
                "UP/DOWN: Select",
                "ENTER: Buy",
                "ESC: Close"
            ]
            for i, line in enumerate(instructions):
                text = font.render(line, True, (200, 200, 200))
                screen.blit(
                    text, (shop_rect.centerx - text.get_width() // 2, 
                    shop_rect.bottom - 60 + i * 25)
                )

    def handle_input(self, event):
        if not self.visible:
            return False
        
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.items)
                return True
            elif event.key == K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.items)
                return True
            elif event.key == K_RETURN:
                return "buy"
            elif event.key == K_ESCAPE:
                self.visible = False
                return True
        return False

    def purchase(self, score):
        item = self.items[self.selected_item]
        if score >= item["cost"]:
            # Handle the purchase
            if item["name"] == "Expand Grid +1":
                # Return the cost and the grid expansion
                return item["cost"], True
        return 0, False