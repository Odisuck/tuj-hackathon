import pygame
import random
import generateShape
import colorsys
from checkUnique import *
from shop import *
from pygame.locals import *

# Initialize pygame
pygame.init()

# Font
font = pygame.font.Font('assets/PKMN_font.ttf', 20)

# Initialize shop
init_shop('assets/PKMN_font.ttf')
shop = Shop()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Game settings (now changeable through shop)
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * (GRID_WIDTH + 6) + 50
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
GAME_AREA_LEFT = CELL_SIZE

# Score
score = 0

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1]],  # Custom shape
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris with Random Colors and Shop")

clock = pygame.time.Clock()
held_tetrimino = None
hold_used = False

COLOR_ASSIGN = {}  # Maps shape_idx to color

def get_random_color():
    return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

class Tetrimino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        
        if random.randint(0, 1) < 0.5:
            attempts = 0
            max_attempts = 10
            new_shape = None
            
            while attempts < max_attempts:
                new_shape = generateShape.generate_connected_shape(score)
                if is_unique_shape(new_shape, SHAPES):
                    break
                attempts += 1
                new_shape = None
            
            if new_shape is not None:
                SHAPES.append(new_shape)
                self.shape_idx = len(SHAPES) - 1
                self.shape = new_shape
        
        if self.shape_idx not in COLOR_ASSIGN:
            COLOR_ASSIGN[self.shape_idx] = get_random_color()
        self.color = COLOR_ASSIGN[self.shape_idx]
        
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rotated = [[self.shape[y][x] for y in range(len(self.shape)-1, -1, -1)] 
                  for x in range(len(self.shape[0]))]
        return rotated

def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(GAME_AREA_LEFT + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] != 0:
                pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    GAME_AREA_LEFT + (tetrimino.x + x) * CELL_SIZE,
                    (tetrimino.y + y) * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(screen, tetrimino.color, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

def draw_held_shape(tetrimino):
    label = font.render("Held Shape:", 1, WHITE)
    sx = GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 10
    sy = SCREEN_HEIGHT - 120
    screen.blit(label, (sx, sy))

    if tetrimino:
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen, tetrimino.color, 
                        (sx + x * CELL_SIZE, sy + y * CELL_SIZE + 30, CELL_SIZE, CELL_SIZE)
                    )

def valid_space(tetrimino, grid):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetrimino.y + y >= GRID_HEIGHT or 
                    tetrimino.x + x < 0 or 
                    tetrimino.x + x >= GRID_WIDTH or 
                    grid[tetrimino.y + y][tetrimino.x + x] != 0):
                    return False
    return True

def check_lost(grid):
    return any(cell != 0 for cell in grid[0])

def clear_rows(grid):
    completed_rows = [i for i, row in enumerate(grid) if all(cell != 0 for cell in row)]
    for row_idx in completed_rows:
        del grid[row_idx]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    return len(completed_rows)

def draw_next_shape(tetrimino):
    label = font.render("Next Shape:", 1, WHITE)
    sx = GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 10
    sy = 50
    screen.blit(label, (sx, sy))

    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen, tetrimino.color, 
                    (sx + x * CELL_SIZE, sy + y * CELL_SIZE + 30, CELL_SIZE, CELL_SIZE)
                )

def draw_score(score):
    base_font_size = 25
    label_text = "Score:"
    score_text = f"{score:,}"

    score_area_x = GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE
    score_area_width = SCREEN_WIDTH - score_area_x - 10

    font_size = base_font_size
    while font_size > 10:
        font = pygame.font.Font("assets/PKMN_font.ttf", font_size)
        label_surface = font.render(label_text, True, WHITE)
        score_surface = font.render(score_text, True, WHITE)

        total_width = label_surface.get_width() + score_surface.get_width() + 10

        if total_width <= score_area_width:
            break
        font_size -= 1

    label_x = score_area_x
    score_x = score_area_x + score_area_width - score_surface.get_width()
    y_pos = 10

    screen.blit(label_surface, (label_x, y_pos))
    screen.blit(score_surface, (score_x, y_pos))

def draw_ghost_piece(tetrimino, grid):
    ghost = Tetrimino()
    ghost.shape = tetrimino.shape
    ghost.color = tuple(min(255, c + 50) for c in tetrimino.color)
    ghost.x = tetrimino.x
    ghost.y = tetrimino.y

    while valid_space(ghost, grid):
        ghost.y += 1
    ghost.y -= 1

    for y, row in enumerate(ghost.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    GAME_AREA_LEFT + (ghost.x + x) * CELL_SIZE,
                    (ghost.y + y) * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(screen, ghost.color, rect, 1)

def main():
    global GRID_WIDTH, GRID_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, screen, score
    
    grid = create_grid()
    current_tetrimino = Tetrimino()
    next_tetrimino = Tetrimino()
    fall_time = 0
    fall_speed = 0.5
    run = True
    score = 0
    held_tetrimino = None
    hold_used = False

    while run:
        fall_time += clock.get_rawtime() / 1000
        clock.tick()

        if fall_time >= fall_speed and not shop.visible:
            fall_time = 0
            current_tetrimino.y += 1
            if not valid_space(current_tetrimino, grid):
                current_tetrimino.y -= 1
                for y, row in enumerate(current_tetrimino.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            grid[current_tetrimino.y + y][current_tetrimino.x + x] = current_tetrimino.color
                rows_cleared = clear_rows(grid)
                score += rows_cleared * 100
                hold_used = False
                current_tetrimino = next_tetrimino
                next_tetrimino = Tetrimino()
                if check_lost(grid):
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            
            # Shop toggle
            if event.type == KEYDOWN and event.key == K_s:
                shop.visible = not shop.visible
            
            # Handle shop input
            shop_result = shop.handle_input(event)
            if shop_result == "buy":
                cost, grid_expanded = shop.purchase(score)
                if grid_expanded and score >= cost:
                    score -= cost
                    GRID_WIDTH += 1
                    GRID_HEIGHT += 1
                    SCREEN_WIDTH = CELL_SIZE * (GRID_WIDTH + 6) + 50
                    SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    # Create new grid with updated dimensions
                    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                    # Copy existing blocks to new grid
                    for y in range(min(GRID_HEIGHT, len(grid))):
                        for x in range(min(GRID_WIDTH, len(grid[0]))):
                            if grid[y][x] != 0:
                                new_grid[y][x] = grid[y][x]
                    grid = new_grid
            
            if shop.visible:
                continue  # Skip other input when shop is open
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetrimino.x -= 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.x += 1
                if event.key == pygame.K_RIGHT:
                    current_tetrimino.x += 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.x -= 1
                if event.key == pygame.K_DOWN:
                    current_tetrimino.y += 1
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.y -= 1
                if event.key == pygame.K_UP:
                    rotated = current_tetrimino.rotate()
                    old_shape = current_tetrimino.shape
                    current_tetrimino.shape = rotated
                    if not valid_space(current_tetrimino, grid):
                        current_tetrimino.shape = old_shape

                if event.key == pygame.K_SPACE:
                    while valid_space(current_tetrimino, grid):
                        current_tetrimino.y += 1
                    current_tetrimino.y -= 1
                    for y, row in enumerate(current_tetrimino.shape):
                        for x, cell in enumerate(row):
                            if cell:
                                grid[current_tetrimino.y + y][current_tetrimino.x + x] = current_tetrimino.color
                    rows_cleared = clear_rows(grid)
                    score += rows_cleared * 100
                    hold_used = False
                    current_tetrimino = next_tetrimino
                    next_tetrimino = Tetrimino()
                    if check_lost(grid):
                        run = False

                if event.key == pygame.K_LSHIFT:
                    if not hold_used:
                        if held_tetrimino is None:
                            held_tetrimino = current_tetrimino
                            current_tetrimino = next_tetrimino
                            next_tetrimino = Tetrimino()
                        else:
                            held_tetrimino, current_tetrimino = current_tetrimino, held_tetrimino
                            current_tetrimino.x = GRID_WIDTH // 2 - len(current_tetrimino.shape[0]) // 2
                            current_tetrimino.y = 0
                        hold_used = True

        screen.fill(BLACK)
        draw_grid(grid)
        draw_ghost_piece(current_tetrimino, grid)
        draw_tetrimino(current_tetrimino)
        draw_next_shape(next_tetrimino)
        draw_held_shape(held_tetrimino)
        draw_score(score)
        shop.draw(screen, score, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.display.update()

    label = font.render("GAME OVER", 1, WHITE)
    screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - label.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)

if __name__ == "__main__":
    main()
    pygame.quit()