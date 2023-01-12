def make_playlist():
    melodies = ['BFG_Division.mp3', 'Damnation.mp3', 'Rip_Tear.mp3', 'Skullhacker.mp3', 'The_New_Order.mp3']
    x = len(melodies)
    playl = []
    while len(playl) != x:
        new = random.choice(melodies)
        new1 = os.path.join('data/music/', new)
        playl.append(new1)
        melodies.pop(melodies.index(new))
    return playl


SONG_END = pygame.USEREVENT + 1
playlist = support.make_playlist()



pygame.mixer.music.load(playlist[0])
playlist.pop(0)
pygame.mixer.music.play()
pygame.mixer.music.queue(playlist[0])
playlist.pop(0)
pygame.mixer.music.set_endevent(SONG_END)




if event.type == SONG_END:
    if len(playlist) > 0:
        pygame.mixer.music.queue(playlist[0])
        playlist.pop(0)
        if len(playlist) == 0:
            playlist = make_playlist()


