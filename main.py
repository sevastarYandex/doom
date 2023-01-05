import sys
import pygame
import object
import support


def main():
    pygame.init()
    action()
    pygame.quit()
    sys.exit()


def action():
    screen = pygame.display.set_mode()
    support.WINDOWWIDTH, support.WINDOWHEIGHT = \
        pygame.display.get_window_size()
    shower = object.Shower()
    clock = pygame.time.Clock()
    while shower.isgoing():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shower.stop()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            shower.move(1, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            shower.move(-1, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            shower.move(0, 1)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            shower.move(0, -1)
        shower.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
