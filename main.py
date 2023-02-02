import sys
import pygame
import object
import support

# здесь запускаем игру
def main():
    pygame.init()
    action()
    pygame.quit()
    sys.exit()


def action():
    # создаём плейлист и начинаем его проигрывать
    SONG_END = pygame.USEREVENT + 1
    playlist = support.make_playlist()
    pygame.mixer.music.load(playlist[0])
    playlist.pop(0)
    pygame.mixer.music.play()
    pygame.mixer.music.queue(playlist[0])
    playlist.pop(0)
    pygame.mixer.music.set_endevent(SONG_END)
    # настраиваем окно игры
    screen = pygame.display.set_mode()
    pygame.display.set_caption('DOOM: SARATOV EDITION')
    # определяем некоторые константы
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
    # создаём shower для удобного показа и управления событиями в игре
    shower = object.Shower()
    # создаём clock для управления частотой обновления событий в игре (60ФПС)
    clock = pygame.time.Clock()
    # главный игровой цикл
    while shower.isgoing():
        # получаем события и зажатые клавиши клавиатуры/кнопки мыши
        events = pygame.event.get()
        buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        # сначала проверяем события для всех состояний игры
        for event in events:
            if event.type == pygame.QUIT:
                shower.stop()
            if event.type == SONG_END:
                # переключаем песню после окончания предыдущей
                if len(playlist) > 0:
                    pygame.mixer.music.queue(playlist[0])
                    playlist.pop(0)
                    if len(playlist) == 0:
                        playlist = support.make_playlist()
        # теперь рассматриваем события в зависимости от состояния игры
        # (какое окно открыто внутри неё)
        if shower.sost == support.GAMELOAD:
            # экран загрузки с выбором сохранений, пока
            # игра "на паузе"
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # возвращаемся в меню, пока игра "заморожена"
                        shower.sost = support.GAMEMENU
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        # пытаемся загрузить выбранное сохранение
                        shower.tryload(event.pos)
        elif shower.sost == support.GAMEMENU:
            # меню, пока игра "заморожена" (сам игровой процесс)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # если игрок не жив, возвращаемся в игру
                        if not shower.dead:
                            shower.sost = support.GAME
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        # смотрим, на какую кнопку в меню нажал игрок
                        x, y = event.pos
                        x /= gamecx
                        y /= gamecy
                        if support.GAMEMENUCONTINUE1[0] <= x <= support.GAMEMENUCONTINUE2[0] \
                            and support.GAMEMENUCONTINUE1[1] <= y <= support.GAMEMENUCONTINUE2[1]:
                            if not shower.dead:
                                # кнопка "продолжить"
                                shower.sost = support.GAME
                        if support.GAMEMENULOAD1[0] <= x <= support.GAMEMENULOAD2[0] \
                            and support.GAMEMENULOAD1[1] <= y <= support.GAMEMENULOAD2[1]:
                            # кнопка "загрузить", т.е. загрузка с выбором того или иного сохранения
                            shower.sost = support.GAMELOAD
                        if support.GAMEMENUSAVE1[0] <= x <= support.GAMEMENUSAVE2[0] \
                            and support.GAMEMENUSAVE1[1] <= y <= support.GAMEMENUSAVE2[1]:
                            if not shower.dead:
                                # кнопка "сохраниться" - сохраняем текущую игру и продолжаем играть
                                shower.savegame()
                                shower.sost = support.GAME
                        if support.GAMEMENUBACK1[0] <= x <= support.GAMEMENUBACK2[0] \
                            and support.GAMEMENUBACK1[1] <= y <= support.GAMEMENUBACK2[1]:
                            # уходим в главное меню
                            shower.back()
        elif shower.sost == support.RULE:
            # правила в главном меню игры
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # через esc выходим в главное меню
                        shower.sost = support.MENU
        elif shower.sost == support.SAVE:
            # выбор для игрока, какое сохранение загрузить
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # через esc выходим в главное меню
                        shower.sost = support.MENU
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        # пытаемся загрузить выбранное пользователем сохранение
                        shower.tryload(event.pos)
        elif shower.sost == support.MENU:
            # главное меню игры
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # через esc выход из игры
                        shower.stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        # смотрим, на какую кнопку нажал игрок
                        x, y = event.pos
                        x /= foncx
                        y /= foncy
                        if support.MENUNEW1[0] <= x <= support.MENUNEW2[0] and \
                            support.MENUNEW1[1] <= y <= support.MENUNEW2[1]:
                            # кнопка "новая игра" - начинаем игровой процесс (с нуля)
                            shower.newgame()
                        if support.MENULOAD1[0] <= x <= support.MENULOAD2[0] and \
                                support.MENULOAD1[1] <= y <= support.MENULOAD2[1]:
                            # кнопка "загрузить" - переходим в окно для выбора сохранения
                            shower.sost = support.SAVE
                        if support.MENURULE1[0] <= x <= support.MENURULE2[0] and \
                                support.MENURULE1[1] <= y <= support.MENURULE2[1]:
                            # кнопка "правила" - открываются правила игры
                            shower.sost = support.RULE
                        if support.MENUEXIT1[0] <= x <= support.MENUEXIT2[0] and \
                                support.MENUEXIT1[1] <= y <= support.MENUEXIT2[1]:
                            # выход из игры
                            shower.stop()
        elif shower.sost == support.GAME:
            # игровой процесс
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # замораживаем игровой процесс
                        shower.sost = support.GAMEMENU
                    if event.key == pygame.K_s and \
                        pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # сохраняем текущий прогресс (для последующей загрузки)
                        shower.savegame()
                    if event.key == pygame.K_e:
                        # игрок пытается подобрать оружие с земли на кнопку "e"
                        shower.take()
                    # здесь переключение между слотами оружия игрока
                    if event.key == pygame.K_1:
                        shower.change(support.DUKE)
                    if event.key == pygame.K_2:
                        shower.change(support.PISTOL)
                    if event.key == pygame.K_3:
                        shower.change(support.AUTOMAT)
                    if event.key == pygame.K_4:
                        shower.change(support.SHOTGUN)
            # далее обработка нажатия на клавиши для движения игрока
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                shower.move(1, 0)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                shower.move(-1, 0)
            if keys[pygame.K_DOWN] or (keys[pygame.K_s] and not
            (pygame.key.get_mods() & pygame.KMOD_CTRL)):
                shower.move(0, 1)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                shower.move(0, -1)
            # перезарядка оружия
            if keys[pygame.K_r]:
                shower.reload()
            # стрельба на левую кнопку мыши
            if buttons[0]:
                shower.shoot(pygame.mouse.get_pos())
        # обновляем игровые объекты через shower
        shower.update()
        # отрисовываем игру
        shower.draw(screen)
        pygame.display.flip()
        # задаём фпс
        clock.tick(support.FPS)


if __name__ == "__main__":
    main()
