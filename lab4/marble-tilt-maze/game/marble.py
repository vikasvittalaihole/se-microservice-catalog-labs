import math
import pygame

class Marble:
    def __init__(self, x, y, radius=12):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def resolve_wall(self, wall_rect, bounce=0.6):
        cx = max(wall_rect.left, min(self.x, wall_rect.right))
        cy = max(wall_rect.top, min(self.y, wall_rect.bottom))
        dx, dy = self.x - cx, self.y - cy
        dist_sq = dx * dx + dy * dy
        if dist_sq >= self.radius * self.radius:
            return False
        if dist_sq == 0:
            l, r = self.x - wall_rect.left, wall_rect.right - self.x
            t, b = self.y - wall_rect.top, wall_rect.bottom - self.y
            m = min(l, r, t, b)
            if m == l:   nx, ny, depth = -1, 0, l + self.radius
            elif m == r: nx, ny, depth = 1, 0, r + self.radius
            elif m == t: nx, ny, depth = 0, -1, t + self.radius
            else:        nx, ny, depth = 0, 1, b + self.radius
        else:
            dist = math.sqrt(dist_sq)
            nx, ny, depth = dx / dist, dy / dist, self.radius - dist
        self.x += nx * depth
        self.y += ny * depth
        vn = self.vx * nx + self.vy * ny
        if vn < 0:
            self.vx -= (1 + bounce) * vn * nx
            self.vy -= (1 + bounce) * vn * ny
        return True
