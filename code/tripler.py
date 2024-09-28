import pygame, sys, time, itertools
from pygame import mixer
from random import randint

# ----------------------------------MUSIC RUNNER--------------------------------------
mixer.init()
gameend = mixer.Sound(r"assets\gameover.mp3")
clock = pygame.time.Clock()
jumpnoise = mixer.Sound(r"assets\coin1.mp3")
menumusic = mixer.music.load(r"assets/bgmusic.mp3")
explosion = mixer.Sound(r"assets/explosion.mp3")
# ---------------------------------MUSIC RUNNER---------------------------------------
musicon = True
scorecheck = True
char_ymovement = 0
char_xmovement = 0
game_active = True
isjump = False
m = 6
v = 4
mass = 6
vel = 4
score = 0
high_score = 0
g = 1
a = 1
b = 0
c = 0
d = 0
show = True
choice = 0
scr = 0
cloud_speed = 2
tile_speed = 2
bomb_speed = 2
bg_speed = 2
level = 1
cloudfreq = 1000
bombfreq = 2000
tilefreq = 550
delay = 90
left_movement = 3
right_movement = 3
black = "#ffffff"
check = 0
chk = 0
centerx = 0
centery = 0
grey = "#3f4a54"
bgchoice = 0
caption = pygame.display.set_caption("triple-r")
bg_y_pos = 0
highscore = []
volume = 0.314


def getscore(txtfile, score=0):
    filehandler = open(txtfile, "rt")
    txt = filehandler.readlines()
    filehandler.close()
    scores = txt[0]
    scores = eval("[" + scores + "]")
    return max(scores)  # can sort and use for getting highscore


def addscores(txtfile, score=0):  # rewrite the file for scores
    filehandler = open(txtfile, "r")
    txt = filehandler.readlines()
    filehandler.close()
    fs = open(txtfile, "w")
    txt += "," + str(score)
    fs.writelines(txt)
    fs.close()


def newgame():
    global mass, vel, game_active, char_xmovement, char_ymovement, scr, tile_list, start, stop, char_rect

    game_active = True
    cloud_list.clear()
    tile_list.clear()
    bomb_list.clear()
    char_rect.center = (250, 400)
    char_xmovement = 0
    char_ymovement = 0
    mass = m
    vel = v
    scr = 0
    start = stop


def create_cloud():
    x = randint(0, 500)
    new_cloud = cloud.get_rect(center=(x, 0))
    return new_cloud


def create_tile():
    x = randint(0, 500)
    new_tile = tile.get_rect(center=(x, 0))
    return new_tile


def create_basic(x, y):
    tile = pygame.image.load("assets/tile.png")
    tile1 = pygame.transform.scale(tile, (150, 20))
    ew = tile1.get_rect(center=(x, y))
    screen1.blit(tile1, ew)


def create_bomb():
    x = randint(0, 500)
    new_bomb = bomb.get_rect(center=(x, 0))
    return new_bomb


def move_clouds(clouds):
    for c in clouds:
        c.centery += cloud_speed
    return clouds


def move_tiles(tiles):
    for t in tiles:
        t.centery += tile_speed
    return tiles


def move_bombs(bombs):
    for b in bombs:
        b.centery += bomb_speed
    return bombs


def draw_clouds(clouds):
    for c in clouds:
        screen.blit(cloud, c)


def draw_tiles(tiles):
    for t in tiles:
        screen.blit(tile, t)


def draw_bombs(bombs):
    for b in bombs:
        screen.blit(bomb, b)


def check_collision(tile_list):
    global char_ymovement, isjump, mass, vel, centery, centerx, char_rect, choice
    for t in tile_list:
        if char_rect.colliderect(t):
            isjump = True
            if choice == 0:
                char1_rect = char1.get_rect(center=(centerx, centery))
                screen.blit(char1, char1_rect)
            if choice == 1:
                char1_rect = char1.get_rect(center=(centerx, centery))
                screen.blit(char1, char1_rect)
            if choice == 2:
                char2_rect = char2.get_rect(center=(centerx, centery))
                screen.blit(char2, char2_rect)
            if choice == 3:
                char3_rect = char3.get_rect(center=(centerx, centery))
                screen.blit(char3, char3_rect)
    if isjump == True:
        mixer.Sound.set_volume(jumpnoise, 0.05)
        mixer.Sound.play(jumpnoise)
        F = vel
        char_ymovement -= F

        vel -= 0.1

        if vel < 0:
            isjump = False

            vel = v
            mass = m

    if gravity == True:
        char_ymovement += g


def game_over():
    global centerx, centery
    if char_rect.top >= 700:
        mixer.Sound.set_volume(gameend, 0.314)
        mixer.Sound.play(gameend)
        return False
    if level == 5:
        for b in bomb_list:
            if char_rect.colliderect(b):
                ex = pygame.image.load("assets/exaaaplossshion.png").convert_alpha()
                ex = pygame.transform.scale(ex, (300, 300))
                exrect = ex.get_rect(center=(centerx, centery))
                screen1.blit(ex, exrect)
                pygame.display.update(exrect)
                mixer.Sound.set_volume(explosion, 0.5)
                mixer.Sound.play(explosion)
                pygame.time.wait(1000)

                return False

    return True


def pause():
    global check
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_m:
                    check = 1
                    menu.make_menu(250, 180, "pause")
                elif event.key == pygame.K_l:
                    pygame.quit()
                    sys.exit()

        menu.text(30, "PAUSED", 250, 270, 200, 200, 200, "normal", "game")
        menu.text(
            22, "press SPACE to continue", (250), (300), 200, 200, 200, "normal", "semi"
        )
        menu.text(
            22, "press M to see menu", (250), (630), 200, 200, 200, "normal", "semi"
        )
        menu.text(
            22, "press L to leave game", (250), (670), 200, 200, 200, "normal", "semi"
        )
        pygame.display.update()
        clock.tick(90)


class menu:
    global musicon, mute, volume

    def __init__(self):
        pass

    def music(musicon):
        if musicon == False:
            mixer.music.pause()

        else:
            mixer.music.unpause()

    @classmethod
    def change_char(self, x, y):
        global check
        change = pygame.image.load(r"assets\change.webp").convert_alpha()
        change = pygame.transform.scale(change, (60, 60))
        pic = change.get_rect(center=(x, y))
        screen1.blit(change, pic)

    @classmethod
    def change_bg(self):
        global bgchoice, check
        bg_surf2 = pygame.image.load(r"assets/white.png").convert()
        bg_surf2 = pygame.transform.scale(bg_surf2, (500, 700))
        screen4.blit(bg_surf2, (0, 0))
        bruh = pygame.Rect(50 - 10, 70, 429, 70)
        pygame.draw.rect(screen2, (0, 225, 0), bruh, 1)
        menu.text(40, "CHOOSE BACKGROUND", 250, 100, 0, 0, 0, "change", "semi")

        while True:
            change3 = pygame.image.load(r"assets\whiteborder.png").convert_alpha()
            change1 = pygame.image.load(r"assets\grey.png").convert_alpha()
            change2 = pygame.image.load(r"assets\electricblue.jpg").convert_alpha()

            change3 = pygame.transform.scale(change3, (80, 80))
            change1 = pygame.transform.scale(change1, (90, 90))
            change2 = pygame.transform.scale(change2, (90, 90))

            pic3 = change3.get_rect(center=(250 + 100 + 80, 300 - 40 + 15))
            pic1 = change1.get_rect(center=(250 + 100 + 80, 422 - 40 + 5 + 10))
            pic2 = change2.get_rect(
                center=(250 + 100 + 80, 530 - 40 + 5 + 10 + 10 + 10)
            )

            screen4.blit(change3, pic3)
            screen4.blit(change1, pic1)
            screen4.blit(change2, pic2)

            menu.text(20, "press 1 -->", 110, 270, 0, 0, 0, "bg", "semi")
            menu.text(20, "press 2 -->", 110, 392, 0, 0, 0, "bg", "semi")
            menu.text(20, "press 3 -->", 110, 512, 0, 0, 0, "bg", "semi")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        bgchoice = 1
                        menu.setting()
                    if event.key == pygame.K_2:
                        bgchoice = 2
                        menu.setting()
                    if event.key == pygame.K_3:
                        bgchoice = 3
                        menu.setting()

            pygame.display.update()
            clock.tick(90)

    @classmethod
    def setting(self, x=250, y=180):
        global choice, check, musicon, mute, volume
        settingsscreen = pygame.display.set_mode((500, 700))

        bg_surf2 = pygame.image.load(r"assets/grey.jpg").convert()
        bg_surf2 = pygame.transform.scale(bg_surf2, (500, 700))
        settingsscreen.blit(bg_surf2, (0, 0))

        while True:
            tex = menu.text(56, "settings", x, y - 30, 250, 0, 0, "settings", "semi")
            create_basic(250, 210)
            create_basic(250, 100)
            button1 = pygame.Rect(140, 279, 220, 40)
            button2 = pygame.Rect(140, 344, 220, 40)
            button3 = pygame.Rect(140, 401, 220, 40)
            button4 = pygame.Rect(140, 460, 220, 40)

            pygame.draw.rect(settingsscreen, (250, 0, 0), button1, 1)
            pygame.draw.rect(settingsscreen, (250, 0, 0), button2, 1)
            pygame.draw.rect(settingsscreen, (250, 0, 0), button3, 1)
            pygame.draw.rect(settingsscreen, (250, 0, 0), button4, 1)

            vup = pygame.image.load(r"assets\vup.png")
            vdown = pygame.image.load(r"assets\vdown.png")

            vup = pygame.transform.scale(vup, (30, 30))
            vdown = pygame.transform.scale(vdown, (30, 30))

            vuprect = vup.get_rect(center=(230, 420))
            vdownrect = vdown.get_rect(center=(270, 420))

            settingsscreen.blit(vup, vuprect)
            settingsscreen.blit(vdown, vdownrect)

            menu.text(19, "LEAVE SETTINGS", (250), (480), 0, 0, 0, "settings", "semi")
            menu.text(19, "CHANGE CHARACTER", (250), (299), 0, 0, 0, "settings", "semi")
            menu.text(
                19, "CHANGE BACKGROUND", (250), (363), 0, 0, 0, "settings", "semi"
            )

            menu.text(
                18,
                "press C to change character",
                (250),
                (595),
                0,
                0,
                0,
                "normal",
                "semi",
            )
            menu.text(
                18,
                "press B to change background",
                (250),
                (560),
                0,
                0,
                0,
                "normal",
                "semi",
            )
            menu.text(
                18, "press M to mute/unmute", (250), (631), 0, 0, 0, "normal", "semi"
            )
            menu.text(
                18,
                "press BACKSPACE to go to menu",
                (250),
                (666),
                0,
                0,
                0,
                "normal",
                "semi",
            )

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        menu.make_menu(250, 180, "pause")
                    if event.key == pygame.K_c:
                        menu.change_menu()
                    if event.key == pygame.K_b:
                        menu.change_bg()
                    if event.key == pygame.K_m:
                        musicon = not (musicon)
                        menu.music(musicon)
                    if event.key == pygame.K_UP:
                        volume += 0.05
                        mixer.music.set_volume(volume)
                    if event.key == pygame.K_DOWN:
                        volume -= 0.05
                        mixer.music.set_volume(volume)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 140 <= mouse[0] <= 360 and 279 <= mouse[1] <= 319:
                        menu.change_menu()
                    if 140 <= mouse[0] <= 360 and 344 <= mouse[1] <= 384:
                        menu.change_bg()
                    if 140 <= mouse[0] <= 360 and 460 <= mouse[1] <= 500:
                        menu.make_menu(250, 180)
                    if vuprect.collidepoint(mouse):
                        volume += 0.05
                        mixer.music.set_volume(volume)
                    if vdownrect.collidepoint(mouse):
                        volume -= 0.05
                        mixer.music.set_volume(volume)

            pygame.display.update()
            clock.tick(90)

    @classmethod
    def change_menu(self):
        global choice, check
        bg_surf2 = pygame.image.load(r"assets/white.png").convert()
        bg_surf2 = pygame.transform.scale(bg_surf2, (500, 700))
        screen2.blit(bg_surf2, (0, 0))
        bruh = pygame.Rect(50 - 10, 70, 429, 70)
        pygame.draw.rect(screen2, (0, 225, 0), bruh, 1)
        menu.text(40, "CHOOSE CHARACTER", 250, 100, 0, 0, 0, "change", "semi")

        while True:
            change3 = pygame.image.load(r"assets\player.png").convert_alpha()
            change1 = pygame.image.load(r"assets\nezuko-0.png").convert_alpha()
            change2 = pygame.image.load(r"assets\tanjiro-0.png").convert_alpha()

            change3 = pygame.transform.scale(change3, (80, 80))
            change1 = pygame.transform.scale(change1, (80, 80))
            change2 = pygame.transform.scale(change2, (80, 80))

            pic3 = change3.get_rect(center=(250 + 100 + 80, 275))
            pic1 = change1.get_rect(center=(250 + 100 + 80, 397))
            pic2 = change2.get_rect(center=(250 + 100 + 80, 517))

            screen2.blit(change3, pic3)
            screen2.blit(change1, pic1)
            screen2.blit(change2, pic2)

            menu.text(20, "press 1 -->", 110, 270, 0, 0, 0, "change", "semi")
            menu.text(20, "press 2 -->", 110, 392, 0, 0, 0, "change", "semi")
            menu.text(20, "press 3 -->", 110, 512, 0, 0, 0, "change", "semi")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        choice = 1

                        menu.setting()
                    if event.key == pygame.K_2:
                        choice = 2
                        menu.setting()
                    if event.key == pygame.K_3:
                        choice = 3
                        menu.setting()

            pygame.display.update()
            clock.tick(90)

    @classmethod
    def text(self, size, text1, x, y, z, a, n, arg, type):

        if type == "semi":
            font = pygame.font.Font(r"assets\SourceCodePro-Semibold.ttf", size)
        if type == "game":
            font = pygame.font.Font(r"assets\gamecuben.ttf", size)
        if type == "ver":
            font = pygame.font.Font(r"assets\verdana.ttf", size)
        text = font.render(text1, True, (z, a, n))
        self.txt = text.get_rect(center=(x, y))
        if arg == "normal":
            screen1.blit(text, self.txt)
        elif arg == "change":
            screen2.blit(text, self.txt)
        elif arg == "bg":
            screen4.blit(text, self.txt)
        elif arg == "settings":
            settingsscreen.blit(text, self.txt)
        elif arg == "info":
            info_char.blit(text, self.txt)

    @classmethod
    def make_menu(cls, x, y, pausecheck="main"):
        global highscore, start, check
        click = False
        chck = True

        screen2 = pygame.display.set_mode((500, 700))

        bg_surface1 = pygame.image.load("assets/bgpaper2.jpg").convert()
        screen1.blit(bg_surface1, (0, 0))

        pygame.display.flip()
        while True:
            tex = menu.text(56, "triple-r", x, y - 30 - 30, 250, 0, 0, "normal", "semi")
            if int(getscore("save\highscores.txt")) != 0:
                scoretxt = "Highscore : " + str(
                    int(getscore("save\highscores.txt"))
                )
            else:
                scoretxt = "Highscore : " + 'Not played yet'

            hscores = menu.text(
                24, scoretxt, x, y + 25 + 37, 255, 255, 255, "normal", "semi"
            )

            create_basic(250, 210 - 30)
            create_basic(250, 100 - 30)
            button1 = pygame.Rect(140, 279 + 20, 220, 40)
            button2 = pygame.Rect(140, 360 + 30 - 30 - 5 + 20, 220, 40)
            button4 = pygame.Rect(140, 470 - 20 - 30 + 5 + 20, 220, 40)

            pygame.draw.rect(screen1, (250, 0, 0), button1, 1)
            pygame.draw.rect(screen1, (250, 0, 0), button2, 1)
            pygame.draw.rect(screen1, (250, 0, 0), button4, 1)
            if pausecheck == "pause":
                menu.text(
                    19,
                    "CONTINUE",
                    (250),
                    (299 + 1 - 2 + 20),
                    225,
                    225,
                    225,
                    "normal",
                    "semi",
                )
            else:
                menu.text(
                    19,
                    "PLAY",
                    (247),
                    (299 + 1 - 2 + 20),
                    225,
                    225,
                    225,
                    "normal",
                    "semi",
                )

            menu.text(
                19,
                "LEAVE",
                (250),
                (462 + 40 - 10 - 12 - 20 - 6 - 12 + 20),
                225,
                225,
                225,
                "normal",
                "semi",
            )

            menu.text(
                19,
                "SETTINGS",
                (250),
                (480 - 9 - 19 - 15 - 4 - 10 - 20 - 30 + 20),
                225,
                225,
                225,
                "normal",
                "semi",
            )
            if pausecheck == "pause":
                menu.text(
                    18,
                    "press P to continue",
                    (250),
                    (560 + 4 + 10 + 12 + 10),
                    255,
                    225,
                    225,
                    "normal",
                    "semi",
                )
            else:
                menu.text(
                    18,
                    "press P to play",
                    (250),
                    (560 + 4 + 10 + 12 + 10),
                    255,
                    225,
                    225,
                    "normal",
                    "semi",
                )
            menu.text(
                18,
                "press S for settings",
                (250),
                (560),
                255,
                225,
                225,
                "normal",
                "semi",
            )
            menu.text(
                18,
                "press L to leave",
                (250),
                (600 + 5 + 26),
                255,
                225,
                225,
                "normal",
                "semi",
            )

            click = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                pygame.draw.rect(screen1, (250, 0, 0), button1)
                if chk == 0:
                    start = time.time()
                game_loop()

            if keys[pygame.K_l]:
                sys.exit()

            if keys[pygame.K_s]:
                menu.setting()

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 140 <= mouse[0] <= 360 and 299 <= mouse[1] <= 339:
                        pygame.draw.rect(screen1, (250, 0, 0), button1)
                        if chk == 0:
                            start = time.time()
                        game_loop()
                    if 140 <= mouse[0] <= 360 and 375 <= mouse[1] <= 415:
                        menu.setting()
                    if 140 <= mouse[0] <= 360 and 445 <= mouse[1] <= 485:
                        sys.exit()
            score = 0
            high_score = 0

            pygame.display.update()
            clock.tick(10)


def info():
    global volume
    info_char = pygame.display.set_mode((500, 700))
    i = 200 - 20 - 10
    info_screen = pygame.image.load(r"assets\black.png").convert()
    pygame.draw.rect(info_char, (225, 0, 0), (10, 30, 490 - 10, 600 - 125 + 10), 1)

    ui = 0
    while True:
        mixer.music.load("assets/bgmusic.mp3")
        mixer.music.set_volume(volume)
        mixer.music.play(loops=-1)

        keys = pygame.key.get_pressed()

        menu.text(40, " welcome to triple-r ", (250), 90, 225, 225, 225, "info", "ver")
        menu.text(15, " press SPACE ", (400 - 5), 110 + 20, 225, 0, 0, "info", "ver")
        menu.text(15, " press L to leave ", (120), 110 + 20, 225, 0, 0, "info", "ver")

        # time.sleep(3.0)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ui += 1

        if ui == 1:
            menu.text(18, "the game is simple.", 250, i, 225, 225, 225, "info", "ver")
        elif ui == 2:
            menu.text(
                16,
                "use the <- and -> keys to move left and right",
                250,
                i + 50,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 3:
            menu.text(
                16,
                "the character of your choice will move upwards ",
                250,
                i + 100,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 4:
            menu.text(
                16,
                "while constantly being pulled down by gravity",
                250,
                i + 120,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 5:
            menu.text(
                16,
                "keep the character above the bottom of the screen",
                250,
                i + 170,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 6:
            menu.text(
                16,
                "hit the booster points to boost up",
                250,
                i + 190 + 10,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 7:
            menu.text(
                16,
                "each level's difficulty will keep increasing",
                250,
                i + 200 + 20 + 10 + 15,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 8:
            menu.text(
                16,
                "the game is key-oriented",
                250,
                i + 240 + 20 + 10 + 10,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 9:
            menu.text(
                16,
                "follow the instructions to navigate through the game",
                250,
                i + 260 + 20 + 20,
                225,
                225,
                225,
                "info",
                "ver",
            )
        elif ui == 10:
            pygame.draw.rect(
                info_char, (0, 0, 225), (10, 650 - 35, 490 - 10, 47 + 22 + 5), 1
            )

            menu.text(17, "CREDITS", 250, 650 - 10 - 5, 225, 225, 225, "info", "semi")
            menu.text(
                15, "akshath raghav r", 250, 680 - 10, 225, 225, 225, "info", "semi"
            )
            menu.text(15, "kinshuk kalia", 400, 680 - 10, 225, 225, 225, "info", "semi")
            menu.text(15, "sujal yatin v", 100, 680 - 10, 225, 225, 225, "info", "semi")

        elif ui == 11:
            pygame.draw.rect(
                info_char, (225, 0, 0), (10, 600 - 60 + 3, 490 - 10, 40), 1
            )

            menu.text(
                20,
                "press ENTER to continue",
                250,
                580 - 20 + 3,
                225,
                225,
                225,
                "info",
                "semi",
            )

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            menu.make_menu(250, 180)
        if keys[pygame.K_l]:
            pygame.quit()
            sys.exit()
        pygame.display.update()
        clock.tick(10)


def score_display(game_state):
    global highscore
    if game_state == "main_game":
        score_surface = game_font.render(f"Score: {int(score)}", True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(60, 15))
        screen3.blit(score_surface, score_rect)
    if game_state == "game_over":
        # EXPLANATION 2 - here i have just added the score in the var to a list which i importd from another file
        # highscore += [high_score]
        score_surface = game_font.render(f"Score: {int(score)}", True, (0, 0, 0))
        highscore_surface = game_font.render(
            f"High Score: {int(high_score)}", True, (0, 0, 0)
        )
        score_rect = score_surface.get_rect(center=(250, 330))
        highscore_rect = highscore_surface.get_rect(center=(250, 380))
        screen3.blit(score_surface, score_rect)
        screen3.blit(highscore_surface, highscore_rect)
        menu.text(22, "press M to return", (250), (450), 0, 0, 0, "normal", "game")
        menu.text(24, "press R to replay", (250), (250), 0, 0, 0, "normal", "game")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            screen1.fill(black)
            screen1.blit(bg_surface, (0, 0))
            menu.make_menu(250, 180)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def level_2():
    global g, level, a, b

    level = 2
    newgame()
    g = 1.3
    a = 2
    b = 1


def level_3():
    global g, level, b, c

    level = 3
    newgame()
    g = 1.3
    b = 2
    c = 1


def level_4():
    global g, level, left_movement, right_movement, c, d

    level = 4
    newgame()
    g = 1.3
    left_movement = -3
    right_movement = -3
    c = 2
    d = 1


def level_5():
    global g, level, left_movement, right_movement, d

    level = 5
    newgame()
    g = 1.3
    d = 2

    start = stop
    left_movement = 3
    right_movement = 3


def re():
    global g, start, level, left_movement, right_movement, d

    newgame()
    g = 1
    start = time.time() - 1
    score = 0
    high_score = 0
    level = 1
    a = 1
    b = 0
    c = 0
    left_movement = 3
    right_movement = 3


# ----------------------------------------------------------Game Screens----------------------------------------------------


pygame.init()
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/SourceCodePro-Semibold.ttf", 20)
screen1 = pygame.display.set_mode((500, 700))
screen2 = pygame.display.set_mode((500, 700))
screen3 = pygame.display.set_mode((500, 700))
screen4 = pygame.display.set_mode((500, 700))
settingsscreen = pygame.display.set_mode((500, 700))
# Game Variables

if bgchoice == 1:
    bg_surface = pygame.image.load("assets/white.png").convert()
    bg_surface = pygame.transform.scale(bg_surface, (500, 700))
elif bgchoice == 0:
    bg_surface = pygame.image.load("assets/blue.png").convert()
    bg_surface = pygame.transform.rotate(bg_surface, 90.0)
    bg_surface = pygame.transform.scale(bg_surface, (500, 700))
elif bgchoice == 2:
    bg_surface = pygame.image.load("assets/grey.png").convert()

    bg_surface = pygame.transform.rotate(bg_surface, 90.0)
    bg_surface.fill(grey)
    bg_surface = pygame.transform.scale(bg_surface, (500, 700))
elif bgchoice == 3:
    bg_surface = pygame.image.load("assets/electricblue.jpg").convert()
    bg_surface = pygame.transform.rotate(bg_surface, 90.0)
    bg_surface = pygame.transform.scale(bg_surface, (500, 700))

if choice == 2:
    char = pygame.image.load("assets/nezuko-0.png").convert_alpha()
    char = pygame.transform.scale(char, (40, 40))
if choice == 1:
    char = pygame.image.load("assets/player.png").convert_alpha()
    char = pygame.transform.scale(char, (40, 40))
if choice == 0:
    char = pygame.image.load("assets/player.png").convert_alpha()
    char = pygame.transform.scale(char, (40, 40))
if choice == 3:
    char = pygame.image.load("assets/tanjiro-0.png").convert_alpha()
    char = pygame.transform.scale(char, (40, 40))

char1 = pygame.image.load("assets/char1.png").convert_alpha()
char1 = pygame.transform.scale(char1, (70, 70))
char2 = pygame.image.load("assets/char2.png").convert_alpha()
char2 = pygame.transform.scale(char2, (70, 70))
char3 = pygame.image.load("assets/char3.png").convert_alpha()
char3 = pygame.transform.scale(char3, (70, 70))

char_rect = char.get_rect(center=(250, 400))

game_icon = pygame.image.load("assets/player.png")
pygame.display.set_icon(game_icon)

cloud = pygame.image.load("assets/cloud.png")
cloud = pygame.transform.scale(cloud, (110, 50))

tile = pygame.image.load("assets/lightning.png").convert_alpha()
tile = pygame.transform.scale(tile, (40 - 5, 40 - 5))

bomb = pygame.image.load("assets/bomb.png")
bomb = pygame.transform.scale(bomb, (60, 60))  # Resize

chunkiness = 8000

cloud_list = []
SPAWNCLOUD = pygame.USEREVENT
pygame.time.set_timer(SPAWNCLOUD, cloudfreq)
tile_list = []

SPAWNTILE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNTILE, tilefreq)

bomb_list = []
SPAWNBOMB = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNBOMB, bombfreq)


def game_loop():
    global chk, char_rect, change_time, chunkiness, mass, cloud_list, bomb_list, bgchoice, tile_list, vel, game_active, char_xmovement, check, centery, centerx, char_ymovement, g, scr, tile_list, start, stop, show, level, char_rect, char_xpos, bg_y_pos, start, game_active, isjump, score, m, g, h, v, high_score, choice, level, gravity, scr, a, b, c, d, left_movement, right_movement
    t = True
    chk = 1
    if choice == 2:
        char = pygame.image.load("assets/nezuko-0.png").convert_alpha()
        char = pygame.transform.scale(char, (50, 50))
    if choice == 1:
        char = pygame.image.load("assets/player.png").convert_alpha()
        char = pygame.transform.scale(char, (40, 40))
    if choice == 0:
        char = pygame.image.load("assets/player.png").convert_alpha()
        char = pygame.transform.scale(char, (40, 40))
    if choice == 3:
        char = pygame.image.load("assets/tanjiro-0.png").convert_alpha()
        char = pygame.transform.scale(char, (50, 50))
    if check == 0:
        char_rect = char.get_rect(center=(250, 400))
    elif check == 1:
        char_rect = char.get_rect(center=(centerx, centery))

    if bgchoice == 1:
        bg_surface = pygame.image.load("assets/white.png").convert()
        bg_surface = pygame.transform.scale(bg_surface, (500, 700))
    elif bgchoice == 0:
        bg_surface = pygame.image.load("assets/blue.png").convert()
        bg_surface = pygame.transform.rotate(bg_surface, 90.0)
        bg_surface = pygame.transform.scale(bg_surface, (500, 700))
    elif bgchoice == 2:
        bg_surface = pygame.image.load("assets/grey.png").convert()
        bg_surface = pygame.transform.rotate(bg_surface, 90.0)
        bg_surface.fill(grey)
        bg_surface = pygame.transform.scale(bg_surface, (500, 700))
    elif bgchoice == 3:
        bg_surface = pygame.image.load("assets/electricblue.jpg").convert()
        bg_surface = pygame.transform.rotate(bg_surface, 90.0)
        bg_surface = pygame.transform.scale(bg_surface, (500, 700))
    scorecheck = True

    while True:  # game loop

        stop = time.time()
        if stop >= start + 2.2:
            gravity = True
        else:
            gravity = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    char_xmovement = 0
                    char_xmovement -= left_movement

                if event.key == pygame.K_SPACE:
                    centerx = char_rect.centerx
                    centery = char_rect.centery
                    dim_screen = pygame.Surface(screen.get_size()).convert_alpha()
                    dim_screen.fill((0, 0, 0, 180))
                    screen1.blit(dim_screen, (0, 0))

                    pause()

                if event.key == pygame.K_RIGHT:
                    char_xmovement = 0
                    char_xmovement += right_movement
            if event.type == SPAWNCLOUD:
                cloud_list.append(create_cloud())
            if event.type == SPAWNTILE:
                tile_list.append(create_tile())
            if event.type == SPAWNBOMB:
                bomb_list.append(create_bomb())

        screen.blit(bg_surface, (0, 0))

        if scr <= 500:
            if game_active == True:

                bg_y_pos += bg_speed
                screen.blit(bg_surface, (0, bg_y_pos))
                screen.blit(bg_surface, (0, bg_y_pos - 700))
                if bg_y_pos >= 700:
                    bg_y_pos = 0

                cloud_list = move_clouds(cloud_list)
                draw_clouds(cloud_list)

                char_rect.centery += char_ymovement

                char_rect.centerx += char_xmovement
                game_active = game_over()

                screen.blit(char, char_rect)

                if level == 3:
                    current_time = pygame.time.get_ticks()
                    tile_list = move_tiles(tile_list)
                    if current_time >= change_time:
                        draw_tiles(tile_list)
                        change_time = current_time + delay
                        show = not show
                else:
                    tile_list = move_tiles(tile_list)
                    draw_tiles(tile_list)
                char_ymovement = 0
                centerx = char_rect.centerx
                centery = char_rect.centery
                if level == 5:
                    bomb_list = move_bombs(bomb_list)
                    draw_bombs(bomb_list)
                    game_over()

                check_collision(tile_list)
                if level < 5:
                    scr += 0.1
                score += 0.1

                score_display("main_game")

            else:
                high_score = update_score(score, high_score)

                score_display("game_over")

        if game_active == False:
            keys = pygame.key.get_pressed()
            if scorecheck:
                addscores("save\highscores.txt", score)
                scorecheck = False
            high_score = getscore("save\highscores.txt")
            if keys[pygame.K_r]:
                game_active = True
                cloud_list.clear()
                tile_list.clear()
                bomb_list.clear()
                char_rect.center = (250, 400)
                char_xmovement = 0
                char_ymovement = 0
                mass = m
                vel = v
                g = 1
                scr = 0
                start = time.time()
                score = 0
                level = 1
                a = 1
                b = 0
                c = 0
                left_movement = 3
                right_movement = 3
                centerx = 0
                centery = 0
                scorecheck = True

        if scr >= 500:

            if a == 1:
                level = 2
                menu.text(20, "Level 2", 250, 250, 0, 0, 0, "normal", "semi")
                menu.text(
                    20,
                    "double press ENTER to continue",
                    250,
                    450,
                    0,
                    0,
                    0,
                    "normal",
                    "semi",
                )
                menu.text(
                    15, "press M to exit round", 250, 670, 0, 0, 0, "normal", "semi"
                )
                menu.text(
                    15, "press L to exit game", 250, 690, 0, 0, 0, "normal", "semi")
                menu.text(20, "Saturn", 250, 350, 0, 0, 0, "normal", "game")

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_RETURN:
                            level_2()
                        if event.key == pygame.K_m:
                            menu.make_menu(250, 180)
                        if event.key == pygame.K_l:
                            pygame.quit()
                            sys.exit()



            elif b == 1:
                level = 3
                menu.text(20, "Level 3", 250, 250 - 50, 0, 0, 0, "normal", "semi")
                menu.text(
                    20,
                    "double press ENTER to continue",
                    250,
                    450 - 50,
                    0,
                    0,
                    0,
                    "normal",
                    "semi",
                )
                menu.text(20, "Flash", 250, 350 - 50, 0, 0, 0, "normal", "game")
                menu.text(
                    15, "press M to exit round", 250, 670, 0, 0, 0, "normal", "semi"
                )
                menu.text(
                    15, "press L to exit game", 250, 690, 0, 0, 0, "normal", "semi"
                )
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_RETURN:
                            level_3()
                        if event.key == pygame.K_m:
                            menu.make_menu(250, 180)
                        if event.key == pygame.K_l:
                            pygame.quit()
                            sys.exit()
                current_time = pygame.time.get_ticks()
                change_time = current_time + delay

            elif c == 1:
                level = 4
                menu.text(20, "Level 4", 250, 250 - 50, 0, 0, 0, "normal", "semi")
                menu.text(
                    20,
                    "double press ENTER to continue",
                    250,
                    450 - 50,
                    0,
                    0,
                    0,
                    "normal",
                    "semi",
                )
                menu.text(20, "Invert", 250, 350 - 50, 0, 0, 0, "normal", "game")
                menu.text(
                    15, "press M to exit round", 250, 670, 0, 0, 0, "normal", "semi"
                )
                menu.text(
                    15, "press L to exit game", 250, 690, 0, 0, 0, "normal", "semi"
                )
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            level_4()
                        if event.key == pygame.K_m:
                            menu.make_menu(250, 180)
                        if event.key == pygame.K_l:
                            pygame.quit()
                            sys.exit()

            elif d == 1:
                level = 5
                menu.text(20, "Level 5", 250, 250 - 50, 0, 0, 0, "normal", "semi")
                menu.text(
                    20,
                    "double press ENTER to continue",
                    250,
                    450 - 50,
                    0,
                    0,
                    0,
                    "normal",
                    "semi",
                )
                menu.text(20, "Bombs", 250, 350 - 50, 0, 0, 0, "normal", "game")
                menu.text(
                    15, "press M to exit round", 250, 670, 0, 0, 0, "normal", "semi"
                )
                menu.text(
                    15, "press L to exit game", 250, 690, 0, 0, 0, "normal", "semi"
                )

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            level_5()
                        if event.key == pygame.K_m:
                            menu.make_menu(250, 180)
                        if event.key == pygame.K_l:
                            pygame.quit()
                            sys.exit()

        if char_rect.left < 0:
            current_time = pygame.time.get_ticks()
            # bor()
            char_rect.left = 0
        if char_rect.right > 500:
            current_time = pygame.time.get_ticks()
            # bor()
            char_rect.right = 500
        if char_rect.top < 0:
            current_time = pygame.time.get_ticks()
            # bor()
            char_rect.top = 0

        pygame.display.update()
        clock.tick(140)


info_char = pygame.display.set_mode((500, 700))

info()
menu = menu()
