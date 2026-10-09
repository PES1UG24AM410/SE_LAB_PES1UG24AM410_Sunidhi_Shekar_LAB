import math
import random

import pygame

from .target import Target

WHITE = (255, 255, 255)
RED = (220, 60, 60)
GRAY = (170, 170, 175)
GOLD = (240, 200, 80)

PLAYING = "playing"
GAME_OVER = "game_over"

# Target size / lifespan per difficulty. "Medium" matches the original game.
DIFFICULTIES = {
    "Easy":   dict(base_radius=55, min_radius=22, lifespan_ms=2200),
    "Medium": dict(base_radius=40, min_radius=12, lifespan_ms=1500),
    "Hard":   dict(base_radius=30, min_radius=8,  lifespan_ms=900),
}
KEY_TO_DIFFICULTY = {
    pygame.K_1: "Easy", pygame.K_KP1: "Easy",
    pygame.K_2: "Medium", pygame.K_KP2: "Medium",
    pygame.K_3: "Hard", pygame.K_KP3: "Hard",
}

ROUND_SECONDS = 30
MAX_DT_MS = 50          # clamp frame time so a lag spike/window drag can't eat the round
INPUT_DELAY_MS = 600    # ignore keys right after game over (stops accidental replays)


class GameEngine:
    def __init__(self, width, height, difficulty="Medium"):
        self.width = width
        self.height = height
        self.margin = 60
        self.hud_height = 60

        self.font = pygame.font.SysFont("Arial", 26)
        self.big_font = pygame.font.SysFont("Arial", 56, bold=True)
        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 190))

        self.start_round(difficulty)

    # ---------- round lifecycle ----------
    def start_round(self, difficulty):
        self.difficulty = difficulty
        self.settings = DIFFICULTIES[difficulty]
        self.time_left_ms = ROUND_SECONDS * 1000
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.state = PLAYING
        self.game_over_at = 0
        self.target = None
        self.target = self._spawn_target()

    def _spawn_target(self):
        prev = self.target
        for _ in range(10):  # avoid respawning right on top of the old target
            x = random.randint(self.margin, self.width - self.margin)
            y = random.randint(self.margin + self.hud_height, self.height - self.margin)
            if prev is None or math.hypot(x - prev.x, y - prev.y) >= 100:
                break
        return Target(x, y, **self.settings)

    # ---------- input ----------
    def handle_event(self, event):
        if self.state == PLAYING:
            # Left button only: in pygame, scroll-wheel also fires MOUSEBUTTONDOWN (4/5)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if pygame.time.get_ticks() - self.game_over_at < INPUT_DELAY_MS:
                return
            if event.key in KEY_TO_DIFFICULTY:
                self.start_round(KEY_TO_DIFFICULTY[event.key])
            elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _handle_click(self, pos):
        if self.target.contains_point(*pos):
            self.hits += 1
            self.score += 1
            self.target = self._spawn_target()
        else:
            self._register_miss()

    def _register_miss(self):
        self.misses += 1

    def handle_input(self):
        pass  # fully mouse/event driven; nothing to poll

    # ---------- simulation ----------
    def update(self, dt_ms=1000 / 60):
        if self.state != PLAYING:
            return
        dt_ms = min(dt_ms, MAX_DT_MS)

        self.time_left_ms -= dt_ms
        if self.time_left_ms <= 0:
            self.time_left_ms = 0
            self.state = GAME_OVER
            self.game_over_at = pygame.time.get_ticks()
            return

        self.target.update(dt_ms)
        if self.target.expired():
            self._register_miss()
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        return 0.0 if total == 0 else round(100 * self.hits / total, 1)

    # ---------- drawing ----------
    def _text(self, screen, text, y, font=None, color=WHITE):
        surf = (font or self.font).render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(self.width // 2, y)))

    def render(self, screen):
        if self.state == PLAYING:
            r = self.target.radius  # same value the hit-test uses
            pos = (self.target.x, self.target.y)
            pygame.draw.circle(screen, RED, pos, r)
            pygame.draw.circle(screen, WHITE, pos, r, 2)

        screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (10, 10))
        secs = math.ceil(self.time_left_ms / 1000)
        screen.blit(self.font.render(f"Time: {secs}s", True, WHITE), (self.width - 140, 10))
        screen.blit(self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE),
                    (self.width // 2 - 90, 10))

        if self.state == GAME_OVER:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        screen.blit(self.overlay, (0, 0))
        cy = self.height // 2
        self._text(screen, "Time's Up!", cy - 150, self.big_font, GOLD)
        self._text(screen, f"Final Score: {self.score}", cy - 80)
        self._text(screen, f"Accuracy: {self.accuracy()}%", cy - 45)
        self._text(screen, f"Hits: {self.hits}   Misses: {self.misses}   ({self.difficulty})",
                   cy - 10, color=GRAY)
        self._text(screen, "Play again:", cy + 50)
        self._text(screen, "1 - Easy     2 - Medium     3 - Hard", cy + 85, color=GOLD)
        self._text(screen, "Esc / Q - Quit", cy + 130, color=GRAY)
