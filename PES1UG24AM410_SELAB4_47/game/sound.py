import math
from array import array

import pygame


class SoundManager:
    """Generates simple sound effects in code (no asset files needed).
    If audio is unavailable the game keeps running silently."""

    def __init__(self):
        self.sounds = {}
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(44100, -16, 1, 512)
            _, fmt, _ = pygame.mixer.get_init()
            if fmt != -16:  # we only generate signed 16-bit samples
                return
            self.sounds = {
                "hit": self._build([(880, 40), (1320, 60)], "sine", 0.35),
                "miss": self._build([(180, 140)], "square", 0.20),
                "end": self._build([(660, 180), (520, 180), (390, 180), (260, 380)], "sine", 0.35),
            }
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def _build(self, notes, wave, volume):
        rate, _, channels = pygame.mixer.get_init()
        samples = array("h")
        for freq, ms in notes:
            n = int(rate * ms / 1000)
            attack = max(1, int(rate * 0.005))  # 5 ms fade-in avoids clicks
            for i in range(n):
                s = math.sin(2 * math.pi * freq * i / rate)
                if wave == "square":
                    s = 1.0 if s >= 0 else -1.0
                env = min(1.0, i / attack) * (1 - i / n)  # fade-out
                v = int(32767 * volume * s * env)
                for _ in range(channels):
                    samples.append(v)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name):
        if self.enabled:
            self.sounds[name].play()