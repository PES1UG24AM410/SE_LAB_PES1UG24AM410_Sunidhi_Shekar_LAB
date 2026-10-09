import math
import random

import pygame

from .target import Target

WHITE = (255, 255, 255)
RED = (220, 60, 60)

ROUND_SECONDS = 30
MAX_DT_MS = 50  # clamp frame time so a lag spike/window drag can't eat the round


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60
        self.target = None
        self.target = self._spawn_target()

        self.time_left_ms = ROUND_SECONDS * 1000

        self.hits = 0
        self.misses = 0
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 26)
        self.game_over = False

    def _spawn_target(self):
        prev = self.target
        for _ in range(10):  # avoid respawning right on top of the old target
            x = random.randint(self.margin, self.width - self.margin)
            y = random.randint(self.margin + self.hud_height, self.height - self.margin)
            if prev is None or math.hypot(x - prev.x, y - prev.y) >= 100:
                break
        return Target(x, y)

    def handle_event(self, event):
        if self.game_over:
            return
        # Left button only: in pygame, scroll-wheel also fires MOUSEBUTTONDOWN (4/5)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        x, y = pos
        # contains_point() now uses the same radius that render() draws.
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.target = self._spawn_target()
        else:
            self.misses += 1

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self, dt_ms=1000 / 60):
        if self.game_over:
            return
        dt_ms = min(dt_ms, MAX_DT_MS)

        self.time_left_ms -= dt_ms
        if self.time_left_ms <= 0:
            self.time_left_ms = 0
            self.game_over = True
            return

        self.target.update(dt_ms)
        if self.target.expired():
            self.misses += 1  # letting a target time out counts as a miss too
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    def render(self, screen):
        r = self.target.radius  # same value the hit-test uses
        pos = (self.target.x, self.target.y)
        pygame.draw.circle(screen, RED, pos, r)
        pygame.draw.circle(screen, WHITE, pos, r, 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        seconds_left = math.ceil(self.time_left_ms / 1000)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_text, (self.width // 2 - 90, 10))

        if self.game_over and not getattr(self, "_game_over_logged", False):
            # NOTE: no proper game-over screen yet - see Task 2 in the README.
            print(f"Time's up! Final score: {self.score}  Accuracy: {self.accuracy()}%")
            self._game_over_logged = True
