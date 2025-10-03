import pygame
import sys
import random

# Inicialización
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Microjuego Plataformero")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Estados
MENU = 0
CONTROLS = 1
GAME = 2
state = MENU

# Botones del menú
buttons = {
    "Inicio": pygame.Rect(300, 200, 200, 50),
    "Controles": pygame.Rect(300, 270, 200, 50),
    "Salir": pygame.Rect(300, 340, 200, 50)
}

# Contadores
lives = 3
deaths = 0
level_time = 60
start_ticks = None
current_level = 0

# Jugador
player = pygame.Rect(0, 0, 40, 40)
player_vel_y = 0
gravity = 1
jump_power = -15
on_ground = False

# Niveles
levels = []
for i in range(10):
    platforms = [pygame.Rect(0, 550, 800, 50)]
    for j in range(i + 1):
        platforms.append(pygame.Rect(random.randint(100, 700), random.randint(200, 500), 100, 20))
    enemies = [pygame.Rect(random.randint(100, 700), 510, 40, 40) for _ in range(i)]
    obstacles = [pygame.Rect(random.randint(100, 700), 530, 20, 20) for _ in range(i)]
    spawn = pygame.Rect(50, 500, 40, 40)
    goal = pygame.Rect(750, 500, 40, 40)
    levels.append({
        "platforms": platforms,
        "enemies": enemies,
        "obstacles": obstacles,
        "spawn": spawn,
        "goal": goal
    })

def load_level(n):
    global platforms, enemies, obstacles, player, player_vel_y, start_ticks
    level = levels[n]
    platforms = level["platforms"]
    enemies = level["enemies"]
    obstacles = level["obstacles"]
    player = level["spawn"].copy()
    player_vel_y = 0
    start_ticks = pygame.time.get_ticks()

def draw_menu():
    screen.fill(WHITE)
    title = font.render("Microjuego Plataformero", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    for text, rect in buttons.items():
        pygame.draw.rect(screen, GRAY, rect)
        label = font.render(text, True, BLACK)
        screen.blit(label, (rect.x + 50, rect.y + 10))

def draw_controls():
    screen.fill(WHITE)
    title = font.render("Controles del Juego", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    controls = [
        "← → : Moverse",
        "↑    : Saltar",
        "ESC : Volver al menú"
    ]
    for i, line in enumerate(controls):
        label = font.render(line, True, BLACK)
        screen.blit(label, (WIDTH//2 - label.get_width()//2, 180 + i * 40))

def draw_game_screen():
    screen.fill(WHITE)
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, obs)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, YELLOW, levels[current_level]["goal"])

    lives_text = font.render(f"Vidas: {lives}", True, BLACK)
    deaths_text = font.render(f"Muertes: {deaths}", True, BLACK)
    time_left = max(0, level_time - (pygame.time.get_ticks() - start_ticks) // 1000)
    time_text = font.render(f"Tiempo: {time_left}", True, BLACK)
    level_text = font.render(f"Nivel: {current_level + 1}/10", True, BLACK)

    screen.blit(lives_text, (10, 10))
    screen.blit(deaths_text, (10, 40))
    screen.blit(time_text, (10, 70))
    screen.blit(level_text, (10, 100))

def reset_player():
    global player, player_vel_y
    player = levels[current_level]["spawn"].copy()
    player_vel_y = 0

# Bucle principal
running = True
load_level(current_level)

while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if buttons["Inicio"].collidepoint(mouse_pos):
                    state = GAME
                    current_level = 0
                    lives = 3
                    deaths = 0
                    load_level(current_level)
                elif buttons["Controles"].collidepoint(mouse_pos):
                    state = CONTROLS
                elif buttons["Salir"].collidepoint(mouse_pos):
                    running = False

        elif state == CONTROLS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = MENU

        elif state == GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = MENU

    if state == MENU:
        draw_menu()
    elif state == CONTROLS:
        draw_controls()
    elif state == GAME:
        # Movimiento jugador
        player_vel_y += gravity
        player.y += player_vel_y
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP] and on_ground:
            player_vel_y = jump_power

        # Colisiones con plataformas
        on_ground = False
        for plat in platforms:
            if player.colliderect(plat) and player_vel_y >= 0:
                player.bottom = plat.top
                player_vel_y = 0
                on_ground = True

        # Colisiones con enemigos u obstáculos
        for enemy in enemies + obstacles:
            if player.colliderect(enemy):
                deaths += 1
                lives -= 1
                reset_player()
                if lives <= 0:
                    state = MENU

        # Meta alcanzada
        if player.colliderect(levels[current_level]["goal"]):
            current_level += 1
            if current_level >= len(levels):
                state = MENU
            else:
                lives = 3
                load_level(current_level)

        draw_game_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
