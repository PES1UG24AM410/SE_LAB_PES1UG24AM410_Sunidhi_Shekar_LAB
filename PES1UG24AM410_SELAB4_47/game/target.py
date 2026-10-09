import math


class Target:
    def __init__(self, x, y, base_radius=40, min_radius=12, lifespan_ms=1500):
        self.x = x
        self.y = y
        self.base_radius = base_radius
        self.min_radius = min_radius
        self.lifespan_ms = lifespan_ms
        self.age_ms = 0.0

    def update(self, dt_ms):
        self.age_ms += dt_ms

    def expired(self):
        return self.age_ms >= self.lifespan_ms

    def visual_radius(self):
        # The target shrinks linearly as it ages.
        t = min(1.0, self.age_ms / self.lifespan_ms)
        return self.base_radius - (self.base_radius - self.min_radius) * t

    @property
    def radius(self):
        # Single source of truth: the integer radius that is drawn AND
        # used for hit-testing, so the two can never disagree.
        return max(1, round(self.visual_radius()))

    def contains_point(self, x, y):
        return math.hypot(self.x - x, self.y - y) <= self.radius