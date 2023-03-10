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
    player = object.generatelevel(support.loadLevel(1))
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
        object.allgroup.update()
        object.allgroup.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
