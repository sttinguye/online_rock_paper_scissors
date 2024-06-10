import pygame, sys
from network import Network
from pygame import mixer
import pickle

#/ ************INITIALIZE****************
pygame.font.init()
pygame.mixer.init()

score_font = pygame.font.SysFont('comicsans', 40)
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("rock paper scissor")
icon = pygame.image.load("rock-paper-scissors.png")
pygame.display.set_icon(icon)
background = pygame.image.load("rockpaperscissors123.jpg")
background1 = pygame.image.load("rockpaperscissors1234.jpg")
mixer.music.load("calming.wav")
mixer.music.play(-1)

# rock paper scissor
rock = pygame.image.load("cave-painting.png")
paper = pygame.image.load("parchment.png")
scissors = pygame.image.load("scissors.png")


class Button: #create button
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win): # draw rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (253, 239, 230))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2))) #draw text in the middle of the rectangle

    def click(self, pos): #collision between your mouse and button
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p, p_score_win, p_score_lose): #draw everything on the board
    win.fill((128, 128, 128)) #fill background with RGB color
    win.blit(background1, (0, 0)) #add picture to screen as background

    # score
    p_score_win = score_font.render("Win: " + str(p_score_win), 1, (0, 0, 0))
    win.blit(p_score_win, (10, 10))
    p_score_lose = score_font.render("Lose: " + str(p_score_lose), 1, (0, 0, 0))
    win.blit(p_score_lose, (width - p_score_lose.get_width()-10, 10))


    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

    else:

        font = pygame.font.SysFont("comicsans", 60)

        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (60, 220))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 220))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        user_name= font.render("User: " + playerName, 1, (0, 0, 0))
        win.blit(user_name, (230, 10))

        if game.bothWent():
            text1 = font.render(move1, 1, (255, 0, 0))
            text2 = font.render(move2, 1, (255, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (255, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (255, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (255, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (255, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))

        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)
        win.blit(rock, (80, 450))
        win.blit(scissors, (280, 450))
        win.blit(paper, (480, 450))
    pygame.display.update()


btns = [Button("Rock", 70, 455, (253, 239, 230)), Button("Scissors", 270, 455, (253, 239, 230)),
        Button("Paper", 470, 455, (253, 239, 230))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network() #connect
    player = int(n.getP()) #player 1 or 2
    print("You are player", player)
    a = 0
    b = 0



    while run:
        clock.tick(60)
        try:
            game = n.send("get") #asking the server to get the game
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player, a, b)
            pygame.time.delay(500)
            try:
                game = n.send("reset") # if both player went tell the server to reset the game to play again
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                win_sound = pygame.mixer.Sound("kids.wav")
                win_sound.play()
                text = font.render("You Won!", 1, (255, 0, 0))
                a += 1
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                lose_sound = pygame.mixer.Sound("sad.wav")
                lose_sound.play()
                text = font.render("You Lost...", 1, (255, 0, 0))
                b += 1

            win.blit(text, (width / 2 - text.get_width() / 2, (height / 2 - text.get_height() / 2)-30))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player, a, b)


def menu_screen():

    run = True
    clock = pygame.time.Clock()
    #####################
    base_font = pygame.font.Font(None, 32)
    user_text = 'Enter your name: '
    input_rect = pygame.Rect(50, 50, 250, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive

    active = False
    #####################
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        win.blit(background, (0, 0))
        # ##################################
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    active = not active
            if event.type == pygame.KEYDOWN:
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(win, color, input_rect, 2)
        text_surface = base_font.render(user_text, True, (0,0,0))
        win.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)
        # ###################################
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (220, 100))
        global playerName
        playerName = user_text[17:]
        pygame.display.update()

    main()


while True:
    menu_screen()