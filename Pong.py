import pygame
from pygame.locals import *
from colorama import Fore
import random

WIDTH = 630
HEIGHT = 630
SCREEN = (255, 255, 255)
color = (0, 0, 0)
ball_color = (225, 0, 0)
speed = 1.90
ball_speed = 1.9
player1_paddle_y = 255
player2_paddle_y = 255
ball_radius = 10
ball_position = (WIDTH // 2, HEIGHT // 2)
ball_speed_x = 1.5
ball_speed_y = 1.5
player1_score = 0
player2_score = 0

def pong():
    global ball_position, ball_speed_x, ball_speed_y, player1_score, player2_score

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    #print_timer = pygame.time.get_ticks()
    #print_interval = 1000

    #joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[K_w]:
            move_player1_paddle(-speed)
        if keys[K_s]:
            move_player1_paddle(speed)

        handle_gamepad_input()

        ball_position = (ball_position[0] + ball_speed_x, ball_position[1] + ball_speed_y)

        if ball_position[0] <= 0:
            player2_score += 1
            reset()
        elif ball_position[0] >= HEIGHT:
            player1_score += 1
            reset()

        '''
        current_time = pygame.time.get_ticks()
        if current_time - print_timer >= print_interval:
            print("Ball Position:", ball_position)
            print("Player 1 Paddle Y:", player1_paddle_y)
            print("Player 2 Paddle Y:", player2_paddle_y)
            print(joysticks)
            print_timer = current_time
        '''
        if ball_position[0] <= 0 or ball_position[0] >= WIDTH:
            ball_speed_x = -ball_speed_x

        if ball_position[1] <= 40 or ball_position[1] >= HEIGHT:
            ball_speed_y = -ball_speed_y

        if player1_paddle_collision(ball_position[0], ball_position[1]):
            ball_speed_x = -ball_speed_x
            print(Fore.YELLOW + "Player 1 Paddle Collision" + Fore.RESET)

        if player2_paddle_collision(ball_position[0], ball_position[1]):
            ball_speed_x = -ball_speed_x
            print(Fore.CYAN + "Player 2 Paddle Collision" + Fore.RESET)

        screen.fill(SCREEN)
        screen.blit(draw_score(), (10, 10))
        screen.blit(draw_opponent_score(), (450, 10))
        draw_dashed_line(screen)
        player1_paddle(screen)
        player2_paddle(screen)
        draw_ball(screen)
        pygame.display.flip()

    pygame.quit()

def draw_score():
    font = pygame.font.Font('freesansbold.ttf', 20)
    score_text = font.render('Player 1 Score: ' + str(player1_score), True, (0, 0, 0))
    return score_text
def draw_opponent_score():
    font = pygame.font.Font('freesansbold.ttf', 20)
    opponent_score_text = font.render(' Player 2 Score: ' + str(player2_score), True, (0, 0, 0))
    return opponent_score_text

def draw_dashed_line(screen):
    dash_width = 5
    gap_width = 50
    dash_count = HEIGHT // (dash_width + gap_width)

    for i in range(dash_count):
        dash_y = i * (dash_width + gap_width) + gap_width // 2
        pygame.draw.rect(screen,  (0, 0, 0), (WIDTH // 2 - dash_width // 2, dash_y, dash_width, dash_width))
def draw_ball(screen):
    pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

def reset():
    global ball_position, player1_paddle_y, player2_paddle_y, ball_speed_x, ball_speed_y
    ball_position = (WIDTH // 2, HEIGHT // 2)
    player1_paddle_y = 255
    player2_paddle_y = 255
    ball_speed_x = 1.5
    ball_speed_y = 1.5
    ball_speed_x = random.uniform(-speed, speed)
    ball_speed_y = random.uniform(-speed, speed)

def player1_paddle(screen):
    global player1_paddle_y
    pygame.draw.rect(screen, color, pygame.Rect(30, player1_paddle_y, 15, 100))

def player2_paddle(screen):
    global player2_paddle_y
    pygame.draw.rect(screen, color, pygame.Rect(585, player2_paddle_y, 15, 100))

def move_player1_paddle(dy):
    global player1_paddle_y
    player1_paddle_y += dy
    player1_paddle_y = max(40, min(HEIGHT - 110, player1_paddle_y))

def move_player2_paddle(dy):
    global player2_paddle_y
    player2_paddle_y += dy
    player2_paddle_y = max(40, min(HEIGHT - 110, player2_paddle_y))

def handle_gamepad_input():
    num_joysticks = pygame.joystick.get_count()

    if num_joysticks >= 1:
        joystick = pygame.joystick.Joystick(0)  # Player 2 joystick
        joystick.init()
        axis_vertical = joystick.get_axis(1)

        if axis_vertical > 0.5:  # Joystick down
            move_player2_paddle(speed)
        elif axis_vertical < -0.5:  # Joystick up
            move_player2_paddle(-speed)

def player1_paddle_collision(ball_x, ball_y):
    paddle_rect = pygame.Rect(30, player1_paddle_y, 15, 100)
    return paddle_rect.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 *
                                               ball_radius))

def player2_paddle_collision(ball_x, ball_y):
    paddle_rect = pygame.Rect(585, player2_paddle_y, 15, 100)
    return paddle_rect.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 *
                                               ball_radius))


if __name__ == "__main__":
    pong()