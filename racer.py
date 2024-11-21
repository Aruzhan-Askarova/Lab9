import pygame, sys
from pygame.locals import *
import random, time

# Инициализация pygame
pygame.init()

# Константы
FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COLLECTED_COINS = 0  # Для отслеживания коинов до увеличения скорости
TOTAL_COINS = 0  # Для отображения общего числа собранных монет
COINS_TO_SPEEDUP = 5  # Увеличивать скорость каждые N монет

# Цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка фона
background = pygame.image.load("AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Классы
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin1.png")  # Изображение монеты
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT // 2))
        self.weight = random.randint(1, 3)  # Вес монеты (1-3)
        self.speed = random.randint(2, 5)  # Скорость падения монеты

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:  # Если монета уходит за экран
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Новая позиция

# Создание объектов
P1 = Player()
E1 = Enemy()
coin = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(coin)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin)

# Главный игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение очков
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_collected = font_small.render(f"Coins: {TOTAL_COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_collected, (10, 30))

    # Обновление всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка столкновений с врагами
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Проверка столкновений с монетами
    if pygame.sprite.spritecollideany(P1, coins):
        collected_coin = pygame.sprite.spritecollideany(P1, coins)
        COLLECTED_COINS += collected_coin.weight  # Увеличиваем временный счётчик
        TOTAL_COINS += collected_coin.weight  # Увеличиваем общий счёт
        collected_coin.kill()  # Удаляем монету

        # Создаём новую монету
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

        # Увеличение скорости
        if COLLECTED_COINS >= COINS_TO_SPEEDUP:
            SPEED += 1
            COLLECTED_COINS = 0  # Сбрасываем временный счётчик

    # Обновление экрана
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
