def shortest_path(A: list, B: list) -> list:
    """
    Returns the shortest path from point A to point B on a grid as a list of steps.
    
    Args:
        A : A list [a1, a2] representing the coordinates of point A.
        B : A list [b1, b2] representing the coordinates of point B.

    Returns:
        steps: List containing the steps to move from A to B.
    """
    a1, a2 = A
    b1, b2 = B
    steps = []
    
    # Calculate steps required horizontally (Based on the numerical value setup in Gym Env)
    if b1 > a1:
        steps.extend([0] * (b1 - a1)) #right
    elif b1 < a1:
        steps.extend([2] * (a1 - b1)) #left
    
    # Calculate steps required vertically
    if b2 > a2:
        steps.extend([1] * (b2 - a2)) #down
    elif b2 < a2:
        steps.extend([3] * (a2 - b2)) #up
    
    return steps
