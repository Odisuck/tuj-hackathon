def get_all_rotations(shape):
    """Returns all unique rotations of a shape"""
    rotations = [shape]
    current = shape
    
    # For each possible rotation (up to 3 more for square shapes)
    for _ in range(3):
        # Rotate 90 degrees
        rotated = [[current[y][x] for y in range(len(current)-1, -1, -1)] 
                  for x in range(len(current[0]))]
        
        # Check if this rotation is new
        if not any(rotated == rot for rot in rotations):
            rotations.append(rotated)
        current = rotated
    
    return rotations

def is_unique_shape(new_shape, existing_shapes):
    """Check if new_shape is unique compared to all existing shapes"""
    new_rotations = get_all_rotations(new_shape)
    
    for existing_shape in existing_shapes:
        existing_rotations = get_all_rotations(existing_shape)
        
        # Compare all rotations of new shape against all rotations of existing shape
        for new_rot in new_rotations:
            for existing_rot in existing_rotations:
                if new_rot == existing_rot:
                    return False
    return True