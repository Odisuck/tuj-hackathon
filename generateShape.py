import random

def generate_connected_shape(score):
    while True:
        # Determine grid size based on score
        if score < 500:
            size = 3
        elif score < 1000:
            size = 4
        elif score < 1500:
            size = 5
        else:
            size = 6

        # Generate grid with higher density for smaller sizes
        density = 0.4 + (0.1 * size)
        grid = [[1 if random.random() < density else 0 for _ in range(size)] 
               for _ in range(size)]
        
        # Remove isolated blocks
        changed = True
        while changed:
            changed = False
            for y in range(size):
                for x in range(size):
                    if grid[y][x] == 1:
                        has_neighbor = False
                        if y > 0 and grid[y-1][x] == 1: has_neighbor = True
                        if y < size-1 and grid[y+1][x] == 1: has_neighbor = True
                        if x > 0 and grid[y][x-1] == 1: has_neighbor = True
                        if x < size-1 and grid[y][x+1] == 1: has_neighbor = True
                        
                        if not has_neighbor:
                            grid[y][x] = 0
                            changed = True
        
        # Flood fill to check connectivity
        def flood(y, x, visited):
            if (y, x) in visited or y < 0 or y >= size or x < 0 or x >= size or grid[y][x] != 1:
                return
            visited.add((y, x))
            flood(y-1, x, visited)
            flood(y+1, x, visited)
            flood(y, x-1, visited)
            flood(y, x+1, visited)
        
        blocks = [(y, x) for y in range(size) for x in range(size) if grid[y][x] == 1]
        
        if not blocks:
            continue
            
        visited = set()
        flood(blocks[0][0], blocks[0][1], visited)
        
        if len(visited) == len(blocks) and len(blocks) >= 2:
            return grid

# Example usage with the exact format you need
shape = generate_connected_shape(600)
print("[")
for row in shape:
    print(f"    {row},")
print("]")