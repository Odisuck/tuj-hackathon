import pygame
import random
import colorsys

# Initialize pygame
pygame.init()

# Font
font = pygame.font.Font('assets/PKMN_font.ttf', 20)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Game settings
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * (GRID_WIDTH + 6) + 50
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
GAME_AREA_LEFT = CELL_SIZE

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
pygame.display.set_caption("Tetris with Random Colors")

clock = pygame.time.Clock()
held_tetrimino = None
hold_used = False


COLOR_ASSIGN = {}  # Maps shape_idx to color

def get_random_color():
    # Generate a random color in RGB format
    return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

class Tetrimino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        
        # Get or create color for this shape index
        if self.shape_idx not in COLOR_ASSIGN:
            COLOR_ASSIGN[self.shape_idx] = get_random_color()
        self.color = COLOR_ASSIGN[self.shape_idx]  # Always assign color
        
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        # Transpose and reverse rows to rotate 90 degrees
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
                pygame.draw.rect(screen, grid[y][x], rect)  # Use stored color
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

def main():
    grid = create_grid()
    current_tetrimino = Tetrimino()
    next_tetrimino = Tetrimino()
    fall_time = 0
    fall_speed = 0.5  # seconds
    run = True
    score = 0
    global held_tetrimino, hold_used

    while run:
        fall_time += clock.get_rawtime() / 1000  # Convert to seconds
        clock.tick()

        if fall_time >= fall_speed:
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
                hold_used = False  # ✅ reset here
                current_tetrimino = next_tetrimino
                next_tetrimino = Tetrimino()
                if check_lost(grid):
                    run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

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
                    # Hard drop
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
        draw_tetrimino(current_tetrimino)
        draw_next_shape(next_tetrimino)
        draw_held_shape(held_tetrimino)

        # Display score
        label = font.render(f"Score: {score}", 1, WHITE)
        screen.blit(label, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 10, 10))

        pygame.display.update()

    # Game over message
    label = font.render("GAME OVER", 1, WHITE)
    screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - label.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)  # Wait 2 seconds before closing

if __name__ == "__main__":
    main()
    pygame.quit()