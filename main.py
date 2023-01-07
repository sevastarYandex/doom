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
        pygame.display.get_window_size()
    shower = object.Shower()
    clock = pygame.time.Clock()
    weapon = object.Weapon(5, 5, '1')
    weapon.sethost(shower.player)
    while shower.isgoing():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shower.stop()
                if event.key == pygame.K_r:
                    weapon.reload()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    weapon.click(event.pos)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            shower.move(1, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            shower.move(-1, 0)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            shower.move(0, 1)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            shower.move(0, -1)
        object.bulletgroup.update()
        shower.detect()
        shower.animate()
        shower.draw(screen)
        pygame.display.flip()
        clock.tick(support.FPS)


if __name__ == "__main__":
    main()
