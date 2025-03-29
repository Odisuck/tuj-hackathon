import random

def generate_connected_4x4():
    while True:
        # Step 1: Generate a random 4x4 grid (50% chance of 1)
        grid = [[1 if random.random() > 0.5 else 0 for _ in range(4)] for _ in range(4)]
        
        # Step 2: Remove isolated 1s
        changed = True
        while changed:
            changed = False
            for y in range(4):
                for x in range(4):
                    if grid[y][x] == 1:
                        # Check adjacent cells (up, down, left, right)
                        adjacent = []
                        if y > 0: adjacent.append(grid[y-1][x])
                        if y < 3: adjacent.append(grid[y+1][x])
                        if x > 0: adjacent.append(grid[y][x-1])
                        if x < 3: adjacent.append(grid[y][x+1])
                        
                        # If no adjacent 1s, remove this 1
                        if 1 not in adjacent:
                            grid[y][x] = 0
                            changed = True
        
        # Step 3: Ensure at least one block remains
        if any(1 in row for row in grid):
            return grid

# Example usage
shape = generate_connected_4x4()
for row in shape:
    print(row)