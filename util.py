import math

def move_towards(current, target, speed, dt):
    cx, cy = current
    tx, ty = target

    dx = tx - cx
    dy = ty - cy
    distance = math.hypot(dx, dy)  # entspricht sqrt(dx**2 + dy**2)

    if distance == 0:
        return current

    step = speed * dt

    if step >= distance:
        return (tx, ty)  # Ziel erreicht, nicht überschießen

    # Richtung normalisieren und Schritt anwenden
    nx = dx / distance
    ny = dy / distance

    return (cx + nx * step, cy + ny * step)

def distance(A:tuple,B:tuple):
    return math.hypot(A[0]-B[0],A[1]-B[1])

def direction_to(a, b):
    delta = [bi - ai for ai, bi in zip(a, b)]
    length = math.sqrt(sum(d * d for d in delta))
    if length == 0:
        return delta
    return [d / length for d in delta]

def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n