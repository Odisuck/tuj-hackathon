import random

def generate_connected_4x4():
    while True:
        # Generate initial 4x4 grid
        grid = [[1 if random.random() > 0.5 else 0 for _ in range(4)] for _ in range(4)]
        
        # Remove isolated 1s
        changed = True
        while changed:
            changed = False
            for y in range(4):
                for x in range(4):
                    if grid[y][x] == 1:
                        # Check orthogonally adjacent cells
                        neighbors = [
                            grid[y-1][x] if y > 0 else 0,
                            grid[y+1][x] if y < 3 else 0,
                            grid[y][x-1] if x > 0 else 0,
                            grid[y][x+1] if x < 3 else 0
                        ]
                        if 1 not in neighbors:
                            grid[y][x] = 0
                            changed = True
        
        # Check if all 1s are connected (no split shapes)
        def flood_fill(y, x, visited):
            if (y, x) in visited or y < 0 or y >= 4 or x < 0 or x >= 4 or grid[y][x] != 1:
                return
            visited.add((y, x))
            flood_fill(y-1, x, visited)
            flood_fill(y+1, x, visited)
            flood_fill(y, x-1, visited)
            flood_fill(y, x+1, visited)
        
        # Find first 1
        start = None
        for y in range(4):
            for x in range(4):
                if grid[y][x] == 1:
                    start = (y, x)
                    break
            if start:
                break
        
        # If there are any 1s, check connectivity
        if start:
            visited = set()
            flood_fill(start[0], start[1], visited)
            
            # Count total 1s and compare with visited
            total_ones = sum(sum(row) for row in grid)
            if len(visited) == total_ones and total_ones > 0:
                return grid

# Example usage
shape = generate_connected_4x4()
for row in shape:
    print(row)