import pygame
import time
import random

pygame.init()

# Настройки цветов и экрана
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (148, 0, 211)
cyan = (0, 255, 255)

dis_width, dis_height = 800, 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by AdaL')
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15
slow_speed = 5  # Скорость при остановке времени

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
powerup_font = pygame.font.SysFont("bahnschrift", 20)

# Настройки остановки времени
TIME_STOP_DURATION = 5.0  # Длительность эффекта в секундах
TIME_STOP_SPAWN_INTERVAL = 10.0  # Интервал появления бонуса в секундах


def your_score(score):
    """Отображение текущего счёта."""
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list, time_stopped):
    """Отрисовка змейки. При остановке времени змейка становится голубой."""
    color = cyan if time_stopped else black
    for x in snake_list:
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    """Отображение сообщения на экране."""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def draw_time_stop_powerup(x, y, block_size):
    """Отрисовка бонуса остановки времени (фиолетовый ромб)."""
    center_x = x + block_size // 2
    center_y = y + block_size // 2
    half = block_size // 2 + 2
    points = [
        (center_x, center_y - half),
        (center_x + half, center_y),
        (center_x, center_y + half),
        (center_x - half, center_y),
    ]
    pygame.draw.polygon(dis, purple, points)
    # Маленький символ часов внутри
    pygame.draw.circle(dis, white, (center_x, center_y), 3)


def draw_time_stop_hud(remaining_time):
    """Отображение индикатора остановки времени на HUD."""
    bar_width = 150
    bar_height = 15
    bar_x = dis_width - bar_width - 10
    bar_y = 10

    # Фон полоски
    pygame.draw.rect(dis, (80, 80, 80), [bar_x, bar_y, bar_width, bar_height])

    # Заполнение полоски
    fill_width = int(bar_width * (remaining_time / TIME_STOP_DURATION))
    pygame.draw.rect(dis, purple, [bar_x, bar_y, fill_width, bar_height])

    # Рамка
    pygame.draw.rect(dis, white, [bar_x, bar_y, bar_width, bar_height], 2)

    # Текст
    text = powerup_font.render("TIME STOP", True, purple)
    dis.blit(text, [bar_x, bar_y + bar_height + 2])


def spawn_powerup_position():
    """Генерация случайной позиции для бонуса."""
    px = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    py = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    return px, py


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Переменные остановки времени
    time_stop_active = False
    time_stop_end = 0
    time_stop_powerup_visible = False
    time_stop_px = 0
    time_stop_py = 0
    next_powerup_spawn_time = time.time() + TIME_STOP_SPAWN_INTERVAL

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block

        # Проверка выхода за границы
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        # Отрисовка еды
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Появление бонуса остановки времени
        if not time_stop_powerup_visible and not time_stop_active:
            if current_time >= next_powerup_spawn_time:
                time_stop_px, time_stop_py = spawn_powerup_position()
                # Убедимся что бонус не совпадает с едой
                while time_stop_px == foodx and time_stop_py == foody:
                    time_stop_px, time_stop_py = spawn_powerup_position()
                time_stop_powerup_visible = True

        # Отрисовка бонуса остановки времени
        if time_stop_powerup_visible:
            draw_time_stop_powerup(int(time_stop_px), int(time_stop_py), snake_block)

        # Обновление змейки
        snake_List.append([x1, y1])
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка столкновения с собой
        for x in snake_List[:-1]:
            if x == [x1, y1]:
                game_close = True

        our_snake(snake_block, snake_List, time_stop_active)
        your_score(Length_of_snake - 1)

        # Проверка поедания еды
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Проверка поедания бонуса остановки времени
        if time_stop_powerup_visible:
            if x1 == time_stop_px and y1 == time_stop_py:
                time_stop_active = True
                time_stop_end = current_time + TIME_STOP_DURATION
                time_stop_powerup_visible = False

        # Проверка окончания эффекта остановки времени
        if time_stop_active:
            remaining = time_stop_end - current_time
            if remaining <= 0:
                time_stop_active = False
                next_powerup_spawn_time = current_time + TIME_STOP_SPAWN_INTERVAL
            else:
                draw_time_stop_hud(remaining)

        pygame.display.update()

        # Применение скорости
        if time_stop_active:
            clock.tick(slow_speed)
        else:
            clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
