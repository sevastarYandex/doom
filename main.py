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
    pygame.display.set_caption('DOOM: SARATOV EDITION')
    support.WINDOWWIDTH, support.WINDOWHEIGHT = \
        screen.get_size()
    shower = object.Shower()
    clock = pygame.time.Clock()
    while shower.isgoing():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shower.stop()
                if event.key == pygame.K_e:
                    shower.take()
                if event.key == pygame.K_1:
                    shower.change(support.DUKE)
                if event.key == pygame.K_2:
                    shower.change(support.PISTOL)
                if event.key == pygame.K_3:
                    shower.change(support.AUTOMAT)
                if event.key == pygame.K_4:
                    shower.change(support.SHOTGUN)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            shower.move(1, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            shower.move(-1, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            shower.move(0, 1)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            shower.move(0, -1)
        if keys[pygame.K_r]:
            shower.reload()
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            shower.shoot(pygame.mouse.get_pos())
        shower.update()
        shower.draw(screen)
        pygame.display.flip()
        clock.tick(support.FPS)


if __name__ == "__main__":
    main()
