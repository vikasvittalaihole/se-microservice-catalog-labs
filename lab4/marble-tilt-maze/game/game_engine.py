import math
import pygame
from .marble import Marble
from .wall import Wall
from .sounds import Sounds

# Game Engine

WHITE = (255, 255, 255)
DARK = (40, 40, 50)
WALL_COLOR = (90, 90, 110)
GOAL_COLOR = (60, 200, 120)

class GameEngine:
    DIFFICULTY = {
        "Easy":   {"tilt": 0.8, "friction": 0.03, "time": 60000},
        "Medium": {"tilt": 0.6, "friction": 0.02, "time": 45000},
        "Hard":   {"tilt": 0.5, "friction": 0.01, "time": 30000},
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.marble = Marble(50, 50)
        self.tilt_strength = 0.6
        self.friction = 0.02
        self.max_speed = 9

        self.walls = self._build_maze()
        self.goal_x, self.goal_y, self.goal_radius = width - 60, height - 60, 22

        self.time_limit_ms = 45000
        self.start_ticks = pygame.time.get_ticks()

        self.font = pygame.font.SysFont("Arial", 26)
        self.big_font = pygame.font.SysFont("Arial", 48)
        self.game_over = False
        self.result = None  # "solved" or "timeout"
        self.finish_time_ms = None

        self.sounds = Sounds()
        self.last_wall_sound = 0

        # end-screen buttons: Easy / Medium / Hard / Exit
        self.buttons = {}
        labels = ["Easy", "Medium", "Hard", "Exit"]
        gap = 12
        bw = min(100, (width - 40 - gap * (len(labels) - 1)) // len(labels))
        bh = 44
        x0 = (width - (len(labels) * bw + gap * (len(labels) - 1))) // 2
        for i, label in enumerate(labels):
            self.buttons[label] = pygame.Rect(x0 + i * (bw + gap), height // 2 + 90, bw, bh)

    def _build_maze(self):
        walls = []
        t = 16  # wall thickness

        # outer boundary
        walls.append(Wall(0, 0, self.width, t))
        walls.append(Wall(0, self.height - t, self.width, t))
        walls.append(Wall(0, 0, t, self.height))
        walls.append(Wall(self.width - t, 0, t, self.height))

        # a few internal walls forming a simple winding path
        walls.append(Wall(0, 140, self.width - 140, t))
        walls.append(Wall(140, 260, self.width - 140, t))
        walls.append(Wall(0, 380, self.width - 140, t))

        return walls

    def start_game(self, level):
        s = self.DIFFICULTY[level]
        self.marble = Marble(50, 50)
        self.tilt_strength = s["tilt"]
        self.friction = s["friction"]
        self.time_limit_ms = s["time"]
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.result = None
        self.finish_time_ms = None

    def handle_event(self, event):
        if self.game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for label, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    if label == "Exit":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    else:
                        self.start_game(label)

    def handle_input(self):
        if self.game_over:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.width // 2
        dy = mouse_y - self.height // 2
        dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        ax = (dx / dist) * self.tilt_strength
        ay = (dy / dist) * self.tilt_strength
        self.marble.vx += ax
        self.marble.vy += ay

    def update(self):
        if self.game_over:
            return

        elapsed = pygame.time.get_ticks() - self.start_ticks
        if elapsed >= self.time_limit_ms:
            self.game_over = True
            self.result = "timeout"
            self.sounds.play("timeout")
            return

        self.marble.vx *= (1 - self.friction)
        self.marble.vy *= (1 - self.friction)

        speed = (self.marble.vx ** 2 + self.marble.vy ** 2) ** 0.5
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.marble.vx *= scale
            self.marble.vy *= scale

        self.marble.x += self.marble.vx
        self.marble.y += self.marble.vy

        self._resolve_wall_collisions()

        gx = self.goal_x - self.marble.x
        gy = self.goal_y - self.marble.y
        if (gx ** 2 + gy ** 2) ** 0.5 <= self.goal_radius:
            self.game_over = True
            self.result = "solved"
            self.finish_time_ms = elapsed
            self.sounds.play("goal")

    def _resolve_wall_collisions(self):
        m = self.marble
        for wall in self.walls:
            r = wall.rect()

            # closest point on the wall rect to the marble's center
            cx = max(r.left, min(m.x, r.right))
            cy = max(r.top, min(m.y, r.bottom))
            dx, dy = m.x - cx, m.y - cy
            dist_sq = dx * dx + dy * dy

            # only collide when the circle itself touches the wall
            if dist_sq >= m.radius * m.radius:
                continue

            if dist_sq == 0:
                # center is inside the wall: push out the shortest way
                l, rt = m.x - r.left, r.right - m.x
                t, b = m.y - r.top, r.bottom - m.y
                low = min(l, rt, t, b)
                if low == l:    nx, ny, depth = -1, 0, l + m.radius
                elif low == rt: nx, ny, depth = 1, 0, rt + m.radius
                elif low == t:  nx, ny, depth = 0, -1, t + m.radius
                else:           nx, ny, depth = 0, 1, b + m.radius
            else:
                dist = math.sqrt(dist_sq)
                nx, ny = dx / dist, dy / dist
                depth = m.radius - dist

            # push the marble out of the wall
            m.x += nx * depth
            m.y += ny * depth

            # bounce only if moving into the wall
            vn = m.vx * nx + m.vy * ny
            if vn < 0:
                m.vx -= 1.3 * vn * nx
                m.vy -= 1.3 * vn * ny
                # wall sound only for real hits, not sliding along a wall
                now = pygame.time.get_ticks()
                if vn < -1.5 and now - self.last_wall_sound > 80:
                    self.sounds.play("wall")
                    self.last_wall_sound = now

    def render(self, screen):
        screen.fill(DARK)

        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall.rect())

        pygame.draw.circle(screen, GOAL_COLOR, (self.goal_x, self.goal_y), self.goal_radius)
        pygame.draw.circle(screen, WHITE, (int(self.marble.x), int(self.marble.y)), self.marble.radius)

        elapsed = pygame.time.get_ticks() - self.start_ticks
        seconds_left = max(0, (self.time_limit_ms - elapsed) // 1000)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (10, 10))

        if self.game_over:
            self._draw_end_screen(screen)

    def _draw_end_screen(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        if self.result == "solved":
            title, color = "You solved it!", GOAL_COLOR
            sub = f"Finish time: {self.finish_time_ms / 1000:.1f}s"
        else:
            title, color = "Time's up!", (220, 80, 80)
            sub = "The maze was not solved."

        cx, cy = self.width // 2, self.height // 2
        t = self.big_font.render(title, True, color)
        s = self.font.render(sub, True, WHITE)
        h = self.font.render("Play again:", True, WHITE)
        screen.blit(t, t.get_rect(center=(cx, cy - 50)))
        screen.blit(s, s.get_rect(center=(cx, cy + 5)))
        screen.blit(h, h.get_rect(center=(cx, cy + 55)))

        for label, rect in self.buttons.items():
            pygame.draw.rect(screen, WALL_COLOR, rect, border_radius=8)
            txt = self.font.render(label, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))
