import pygame
from sys import exit
from random import randint
import time

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

game_active = False
mouse_pressed = False
current_time = 0
end_time = 0
time_left = 0


class Start_Screen:
    normal_font = pygame.font.Font("8-BIT WONDER.TTF", 60)
    start_text = normal_font.render("Start Game", False, (255, 255, 255))
    start_rect = start_text.get_rect(topleft=(680, 480))
    s5_surf = normal_font.render("5", False, (255, 255, 255))
    s10_surf = normal_font.render("10", False, (255, 255, 255))
    s30_surf = normal_font.render("30", False, (255, 255, 255))
    s5_rect = s5_surf.get_rect(topleft=(700, 610))
    s10_rect = s10_surf.get_rect(topleft=(900, 610))
    s30_rect = s30_surf.get_rect(topleft=(1100, 610))
    time_set = None  # eingestellte Zeit der runde (5s, 10s, 30s)


class Score:
    score = 0
    time_font = pygame.font.Font("upheavtt.ttf", 70)
    text = time_font.render(f"Score: {score}", False, (255, 255, 255))
    high_score = time_font.render(f"High Score: {0}", False, (255, 255, 255))
    time_text = time_font.render("Time: {0:.2f}".format(end_time), False, (255, 255, 255))


class Circle:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    x = randint(50, 1800)
    y = randint(50, 1000)
    thickness = randint(20, 60)
    generate = False


def check_highscore(score):
    high_score = open("highscore.txt", "r")
    read_it = high_score.read()
    Score.high_score = Score.time_font.render(f"High Score: {read_it}", False, (255, 255, 255))
    if float(read_it) < score:
        high_score.close()
        high_score = open("highscore.txt", "w")
        high_score.write(str(score))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # immer:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    mouse_state = pygame.mouse.get_pressed()
    Score.text = Score.time_font.render(f"Score: {Score.score}", False, (255, 255, 255))  # Score Text aktualisieren
    screen.blit(Score.text, (800, 20))

    if game_active:
        # wenns Spiel läuft:
        current_time = time.time()
        time_left = end_time - current_time
        Start_Screen.time_text = Score.time_font.render("Time: {0:.2f}".format(time_left), False, (255, 255, 255))  # Time Text updaten
        screen.blit(Start_Screen.time_text, (800, 100))
        circle_1 = pygame.draw.circle(screen, (Circle.r, Circle.g, Circle.b), (Circle.x, Circle.y), Circle.thickness)  # Circle zeichnen, immer mit random Werten

        if Circle.generate:  # neuen Circle generieren (zufällige Größe, pos, Farbe, ...)
            Circle.r = randint(0, 255)
            Circle.g = randint(0, 255)
            Circle.b = randint(0, 255)
            Circle.x = randint(50, 1800)
            Circle.y = randint(50, 1000)
            Circle.thickness = randint(20, 60)
            Circle.generate = False

        if circle_1.collidepoint(mouse_pos):
            if mouse_state[0] and not mouse_pressed:  # circle anklicken können (nur eins, deswegen mouse_pressed)
                Circle.generate = True
                mouse_pressed = True
                if Start_Screen.time_set == 5:  # eigene Rechnung, je weniger Zeit, desto mehr Punkte. (Für HighScore)
                    Score.score += 2
                elif Start_Screen.time_set == 10:
                    Score.score += 1
                elif Start_Screen.time_set == 30:
                    Score.score += 0.4
                    Score.score = "{0:.2f}".format(Score.score)
                    Score.score = float(Score.score)

            elif not mouse_state[0] and mouse_pressed:
                mouse_pressed = False

        if current_time >= end_time:  # wenn Zeit zu Ende ist
            game_active = False
            check_highscore(Score.score)
            Circle.generate = False
            Start_Screen.time_set = None

    else:  # Start Screen
        check_highscore(0)  # High Score aktualisieren / am Anfang auch berechnen
        screen.blit(Score.high_score, (700, 100))
        screen.blit(Start_Screen.start_text, Start_Screen.start_rect)
        if Start_Screen.time_set is not None:  # wenn ein Modus ausgewählt wurde
            if Start_Screen.time_set == 5:  # damit alle anderen verschwinden, wenn eins ausgewählt
                screen.blit(Start_Screen.s5_surf, Start_Screen.s5_rect)
            if Start_Screen.time_set == 10:
                screen.blit(Start_Screen.s10_surf, Start_Screen.s10_rect)
            if Start_Screen.time_set == 30:
                screen.blit(Start_Screen.s30_surf, Start_Screen.s30_rect)
        else:       # wenn kein Modi gewählt wurde
            screen.blit(Start_Screen.s5_surf, Start_Screen.s5_rect)
            screen.blit(Start_Screen.s10_surf, Start_Screen.s10_rect)
            screen.blit(Start_Screen.s30_surf, Start_Screen.s30_rect)

        if mouse_state[0]:   # Modi wählen
            if Start_Screen.s5_rect.collidepoint(mouse_pos):
                Start_Screen.time_set = 5
            if Start_Screen.s10_rect.collidepoint(mouse_pos):
                Start_Screen.time_set = 10
            if Start_Screen.s30_rect.collidepoint(mouse_pos):
                Start_Screen.time_set = 30
            if Start_Screen.start_rect.collidepoint(mouse_pos) and Start_Screen.time_set is not None:
                game_active = True
                Score.score = 0
                end_time = time.time() + Start_Screen.time_set  # end time berechnen, also wann eine Runde zuende ist

    pygame.display.update()
    clock.tick(60)
