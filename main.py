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
    support.WINDOWWIDTH, support.WINDOWHEIGHT = pygame.display.get_window_size()
    shower = object.Shower()
    while shower.isshow():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shower.stop()
        shower.update()
        shower.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
