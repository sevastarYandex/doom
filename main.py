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
    SONG_END = pygame.USEREVENT + 1
    playlist = support.make_playlist()
    pygame.mixer.music.load(playlist[0])
    playlist.pop(0)
    pygame.mixer.music.play()
    pygame.mixer.music.queue(playlist[0])
    playlist.pop(0)
    pygame.mixer.music.set_endevent(SONG_END)
    screen = pygame.display.set_mode()
    pygame.display.set_caption('DOOM: SARATOV EDITION')
    support.WINDOWWIDTH, support.WINDOWHEIGHT = \
        screen.get_size()
    shower = object.Shower()
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    while shower.isgoing():
        for event in pygame.event.get():
            if event.type == SONG_END:
                if len(playlist) > 0:
                    pygame.mixer.music.queue(playlist[0])
                    playlist.pop(0)
                    if len(playlist) == 0:
                        playlist = support.make_playlist()
        if shower.sost == support.MENU:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        print(event.pos)
        elif shower.sost == support.GAME:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shower.sost = support.GAMEMENU
                    if event.key == pygame.K_s and \
                        pygame.key.get_mods() & pygame.KMOD_CTRL:
                        shower.savegame()
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
            if keys[pygame.K_DOWN] or (keys[pygame.K_s] and not
            (pygame.key.get_mods() & pygame.KMOD_CTRL)):
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
