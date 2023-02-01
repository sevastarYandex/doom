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
    foncx = screen.get_size()[0] / \
            support.loadImage(object.fonimg).get_size()[0]
    foncy = screen.get_size()[1] / \
            support.loadImage(object.fonimg).get_size()[1]
    gamecx = screen.get_size()[0] / \
            support.loadImage(object.gamemenuimg).get_size()[0]
    gamecy = screen.get_size()[1] / \
            support.loadImage(object.gamemenuimg).get_size()[1]
    shower = object.Shower()
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    while shower.isgoing():
        events = pygame.event.get()
        buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                shower.stop()
            if event.type == SONG_END:
                if len(playlist) > 0:
                    pygame.mixer.music.queue(playlist[0])
                    playlist.pop(0)
                    if len(playlist) == 0:
                        playlist = support.make_playlist()
        if shower.sost == support.GAMELOAD:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shower.sost = support.GAMEMENU
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        shower.tryload(event.pos)
        elif shower.sost == support.GAMEMENU:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not shower.dead:
                            shower.sost = support.GAME
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        x, y = event.pos
                        x /= gamecx
                        y /= gamecy
                        if support.GAMEMENUCONTINUE1[0] <= x <= support.GAMEMENUCONTINUE2[0] \
                            and support.GAMEMENUCONTINUE1[1] <= y <= support.GAMEMENUCONTINUE2[1]:
                            if not shower.dead:
                                shower.sost = support.GAME
                        if support.GAMEMENULOAD1[0] <= x <= support.GAMEMENULOAD2[0] \
                            and support.GAMEMENULOAD1[1] <= y <= support.GAMEMENULOAD2[1]:
                            shower.sost = support.GAMELOAD
                        if support.GAMEMENUSAVE1[0] <= x <= support.GAMEMENUSAVE2[0] \
                            and support.GAMEMENUSAVE1[1] <= y <= support.GAMEMENUSAVE2[1]:
                            if not shower.dead:
                                shower.savegame()
                                shower.sost = support.GAME
                        if support.GAMEMENUBACK1[0] <= x <= support.GAMEMENUBACK2[0] \
                            and support.GAMEMENUBACK1[1] <= y <= support.GAMEMENUBACK2[1]:
                            shower.back()
        elif shower.sost == support.RULE:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shower.sost = support.MENU
        elif shower.sost == support.SAVE:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shower.sost = support.MENU
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        shower.tryload(event.pos)
        elif shower.sost == support.MENU:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shower.stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        x, y = event.pos
                        x /= foncx
                        y /= foncy
                        if support.MENUNEW1[0] <= x <= support.MENUNEW2[0] and \
                            support.MENUNEW1[1] <= y <= support.MENUNEW2[1]:
                            shower.newgame()
                        if support.MENULOAD1[0] <= x <= support.MENULOAD2[0] and \
                                support.MENULOAD1[1] <= y <= support.MENULOAD2[1]:
                            shower.sost = support.SAVE
                        if support.MENURULE1[0] <= x <= support.MENURULE2[0] and \
                                support.MENURULE1[1] <= y <= support.MENURULE2[1]:
                            shower.sost = support.RULE
                        if support.MENUEXIT1[0] <= x <= support.MENUEXIT2[0] and \
                                support.MENUEXIT1[1] <= y <= support.MENUEXIT2[1]:
                            shower.stop()
        elif shower.sost == support.GAME:
            for event in events:
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
            if buttons[0]:
                shower.shoot(pygame.mouse.get_pos())
        shower.update()
        shower.draw(screen)
        pygame.display.flip()
        clock.tick(support.FPS)


if __name__ == "__main__":
    main()
