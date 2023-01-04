import sys

import pygame
pygame.init()


def main():
    action()


def action():
    screen = pygame.display.set_mode()
    show = True
    while show:
        for event in pygame.event.get():
            pass
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
