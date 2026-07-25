import math
import sys, os
import random


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
    
def get_writable_path(filename: str) -> str:
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.abspath(".")
    return os.path.join(base, filename)


def read_highscores(path: str):
    scores = []
    if not os.path.exists(path):
        return scores

    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                scores.append(int(line))
    return scores


def write_highscores(path: str, score: int):
    with open(path, "w") as f:
        f.write(str(score))
            
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def write_highscores(path:str, score:int):
    with open(path, "w") as f:
        f.write(str(score))


def random_coordinate_on_a_ring(center, radius, width):
    angle = random.uniform(0, 2 * math.pi)

    # Sample uniformly by area within the ring [radius, radius + width]
    inner_sq = radius ** 2
    outer_sq = (radius + width) ** 2
    dist = math.sqrt(random.uniform(inner_sq, outer_sq))

    x = center[0] + dist * math.cos(angle)
    y = center[1] + dist * math.sin(angle)
    return x, y
