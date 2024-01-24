import pygame
import random
import sys

pygame.init()

window_width, window_height = 400, 800
window = pygame.display.set_mode([window_width, window_height])

SPACESHIP = pygame.image.load('spaceship.png')
METEORITE_IMAGE = pygame.image.load('meteors.png')
BACKGROUND_IMAGE = pygame.image.load('jpg.jpg')

class Meteorite:
    def __init__(self):
        self.image = METEORITE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, window_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(8, 20)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_height:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, window_width - self.rect.width)
            self.speed = random.randint(8, 20)

meteorites = []

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Initial spaceship coordinates
x = window_width // 2 - SPACESHIP.get_width() // 2
y = window_height // 2 - SPACESHIP.get_height() // 2

# Flags for movement and boost
move_left = False
move_right = False
move_up = False
move_down = False
boost_active = False

# Boost timer and duration
boost_timer = 0
BOOST_DURATION = 5000  # 5 seconds in milliseconds

# Game state
playing = True

# Score and high score
score = 0
high_score = 0
score_timer = pygame.time.get_ticks()

# New High Score text
new_high_score_text = pygame.font.Font(None, 36).render("New High Score!", True, (255, 255, 255))
new_high_score_rect = new_high_score_text.get_rect(center=(window_width // 2, window_height // 2 + 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                boost_active = True
                boost_timer = pygame.time.get_ticks()
            elif event.key == pygame.K_ESCAPE and not playing:
                playing = True
                meteorites = []
                x = window_width // 2 - SPACESHIP.get_width() // 2
                y = window_height // 2 - SPACESHIP.get_height() // 2
                score = 0
                score_timer = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                boost_active = False

    if playing:
        current_time = pygame.time.get_ticks()
        if boost_active and current_time - boost_timer > BOOST_DURATION:
            boost_active = False

        boost_multiplier = 2 if boost_active else 1
        if move_left:
            x = max(0, x - 10 * boost_multiplier)
        if move_right:
            x = min(window_width - SPACESHIP.get_width(), x + 10 * boost_multiplier)
        if move_up:
            y = max(0, y - 10 * boost_multiplier)
        if move_down:
            y = min(window_height - SPACESHIP.get_height(), y + 10 * boost_multiplier)

        for meteorite in meteorites:
            meteorite.update()

        for meteorite in meteorites:
            if meteorite.rect.colliderect(pygame.Rect(x, y, SPACESHIP.get_width(), SPACESHIP.get_height())):
                playing = False

        if all(meteorite.rect.y > window_height for meteorite in meteorites):
            for _ in range(2):
                meteorites.append(Meteorite())

        # Update score every second
        if current_time - score_timer > 1000:
            score += 100
            score_timer = current_time

            # Update high score and display "New High Score" message
            if score > high_score:
                high_score = score

        window.blit(BACKGROUND_IMAGE, (0, 0))

        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))

        # Display high score
        high_score_text = font.render(f"Best: {high_score}", True, (255, 255, 255))
        window.blit(high_score_text, (10, 50))

        for meteorite in meteorites:
            window.blit(meteorite.image, meteorite.rect.topleft)

        window.blit(SPACESHIP, [x, y])
        
    else:
        # Pause screen
        text = pygame.font.Font(None, 72).render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2 - 50))
        window.blit(text, text_rect)

        # Display player's score
        score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(score_text, score_text_rect)

        # Display "New High Score" message
        if score > high_score:
            window.blit(new_high_score_text, new_high_score_rect)

        # Display transparent buttons with border
        restart_button = pygame.Rect(window_width // 2 - 80, window_height // 2 + 100, 160, 50)
        pygame.draw.rect(window, (0, 0, 0, 128), restart_button)  # Transparent fill
        pygame.draw.rect(window, (0, 255, 0), restart_button, 2)  # Border
        restart_text = font.render("Restart", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        window.blit(restart_text, restart_text_rect)

        quit_button = pygame.Rect(window_width // 2 - 80, window_height // 2 + 170, 160, 50)
        pygame.draw.rect(window, (0, 0, 0, 128), quit_button)  # Transparent fill
        pygame.draw.rect(window, (255, 0, 0), quit_button, 2)  # Border
        quit_text = font.render("Quit", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        window.blit(quit_text, quit_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if restart_button.collidepoint(mouse_pos) and mouse_click[0] == 1:
            playing = True
            meteorites = []
            x = window_width // 2 - SPACESHIP.get_width() // 2
            y = window_height // 2 - SPACESHIP.get_height() // 2
            score = 0
            score_timer = pygame.time.get_ticks()

        elif quit_button.collidepoint(mouse_pos) and mouse_click[0] == 1:
            pygame.quit()
            sys.exit()

    pygame.display.update()

    clock.tick(30)
