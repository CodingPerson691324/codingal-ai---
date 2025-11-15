import pygame
import random
import math
import sys

# Simple shooter: blue block shoots bullets at a red block. On hit, the red block explodes into particles.
# Save as makeagame.py and run: python makeagame.py

WIDTH, HEIGHT = 800, 600
FPS = 60

BLUE = (50, 130, 255)
RED = (220, 50, 50)
BG = (30, 30, 30)
WHITE = (240, 240, 240)

PLAYER_SIZE = 40
TARGET_SIZE = 48
BULLET_SIZE = 8
BULLET_SPEED = 700  # px/sec

PARTICLE_MIN = 20
PARTICLE_MAX = 40
PARTICLE_SPEED = 200
PARTICLE_LIFE = 1.1  # seconds

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blue Shoots Red - Explosion Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

# Entities
player = pygame.Rect(60, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
target = pygame.Rect(WIDTH - 140, HEIGHT // 2 - TARGET_SIZE // 2, TARGET_SIZE, TARGET_SIZE)
target_alive = True

bullets = []  # dicts: {'rect': Rect, 'vel': (vx,vy)}
particles = []  # dicts: {'pos': [x,y], 'vel': [vx,vy], 'life': t, 'max_life': t, 'color': (r,g,b)}

def spawn_bullet():
    bx = player.right
    by = player.centery - BULLET_SIZE // 2
    rect = pygame.Rect(bx, by, BULLET_SIZE, BULLET_SIZE)
    bullets.append({'rect': rect, 'vel': (BULLET_SPEED, 0)})

def explode_at(x, y):
    count = random.randint(PARTICLE_MIN, PARTICLE_MAX)
    for _ in range(count):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(PARTICLE_SPEED * 0.3, PARTICLE_SPEED)
        vx, vy = math.cos(angle) * speed, math.sin(angle) * speed
        life = random.uniform(PARTICLE_LIFE * 0.6, PARTICLE_LIFE * 1.1)
        color = random.choice([(255, 180, 40), (255, 110, 20), (255, 220, 110)])
        particles.append({'pos': [x, y], 'vel': [vx, vy], 'life': life, 'max_life': life, 'color': color, 'r': random.randint(3, 8)})

def draw_particle(surf, p):
    life_ratio = max(0.0, p['life'] / p['max_life'])
    alpha = int(255 * life_ratio)
    r = int(p['r'] * (1 + (1 - life_ratio)))  # grow slightly
    col = (*p['color'], alpha)
    s = pygame.Surface((r*2+2, r*2+2), pygame.SRCALPHA)
    pygame.draw.circle(s, col, (r+1, r+1), r)
    surf.blit(s, (p['pos'][0]-r, p['pos'][1]-r))

def reset():
    global target, target_alive, bullets, particles
    target = pygame.Rect(WIDTH - 140, random.randint(80, HEIGHT-80-TARGET_SIZE), TARGET_SIZE, TARGET_SIZE)
    target_alive = True
    bullets.clear()
    particles.clear()

# Game loop
running = True
shoot_cooldown = 0.15  # seconds
shoot_timer = 0.0
respawn_delay = 2.0
respawn_timer = 0.0

while running:
    dt = clock.tick(FPS) / 1000.0
    shoot_timer = max(0.0, shoot_timer - dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_SPACE and shoot_timer == 0.0 and target_alive:
                spawn_bullet()
                shoot_timer = shoot_cooldown

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player.y -= int(300 * dt)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.y += int(300 * dt)
    # keep player on screen
    player.y = max(0, min(HEIGHT - PLAYER_SIZE, player.y))

    # Update bullets
    for b in bullets[:]:
        b['rect'].x += int(b['vel'][0] * dt)
        b['rect'].y += int(b['vel'][1] * dt)
        # remove off-screen bullets
        if b['rect'].left > WIDTH or b['rect'].right < 0 or b['rect'].top > HEIGHT or b['rect'].bottom < 0:
            bullets.remove(b)
            continue
        # check collision with target
        if target_alive and b['rect'].colliderect(target):
            # explode
            cx = target.centerx
            cy = target.centery
            explode_at(cx, cy)
            target_alive = False
            respawn_timer = respawn_delay
            try:
                bullets.remove(b)
            except ValueError:
                pass

    # Update particles
    for p in particles[:]:
        p['pos'][0] += p['vel'][0] * dt
        p['pos'][1] += p['vel'][1] * dt + 60 * dt  # slight gravity effect
        p['life'] -= dt
        if p['life'] <= 0:
            particles.remove(p)

    # Respawn target after delay
    if not target_alive:
        respawn_timer -= dt
        if respawn_timer <= 0:
            # tiny burst when respawn
            target = pygame.Rect(WIDTH - 140, random.randint(80, HEIGHT-80-TARGET_SIZE), TARGET_SIZE, TARGET_SIZE)
            target_alive = True

    # Draw
    screen.fill(BG)
    # HUD
    txt = font.render("W/S or Up/Down: move  Space: shoot  R: reset  Esc: quit", True, WHITE)
    screen.blit(txt, (8, 8))

    # draw player
    pygame.draw.rect(screen, BLUE, player)
    # draw bullets
    for b in bullets:
        pygame.draw.rect(screen, (200, 200, 255), b['rect'])
    # draw target
    if target_alive:
        pygame.draw.rect(screen, RED, target)
        # subtle pulsing outline
        pulse = 4 + int(2 * math.sin(pygame.time.get_ticks() * 0.008))
        pygame.draw.rect(screen, (255, 120, 120), target.inflate(pulse, pulse), 2)
    else:
        # draw a faint smoke rectangle where it was
        r = pygame.Rect(target)
        r.inflate_ip(8, 8)
        pygame.draw.rect(screen, (80, 30, 30), r, 1)

    # draw particles
    for p in particles:
        draw_particle(screen, p)

    pygame.display.flip()

pygame.quit()
sys.exit()