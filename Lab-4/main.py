import pygame

# Must run BEFORE pygame.init() so the mixer uses the format our sounds are generated in.
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

from game.game_engine import GameEngine  # noqa: E402

WIDTH, HEIGHT = 700, 500
DARK_GRAY = (35, 35, 40)
FPS = 60


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Target Aim Trainer - Pygame Version")
    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT)

    running = True
    while running:
        screen.fill(DARK_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            engine.handle_event(event)

        engine.handle_input()
        engine.update(clock.get_time())  # real ms since previous frame
        engine.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()