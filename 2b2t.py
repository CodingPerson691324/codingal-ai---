import pygame
import random
import math
pygame.init()
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
    target = pygame.Rect(WIDTH - 140, HEIGHT // 2 - TARGET_SIZE // 2, TARGET_SIZE, TARGET_SIZE)
    target_alive = True
    bullets = []
    particles = []
reset()
running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # seconds passed since last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and target_alive:
                spawn_bullet()
            elif event.key == pygame.K_r:
                reset()
    # Update bullets
    for b in bullets[:]:
        b['rect'].x += b['vel'][0] * dt
        b['rect'].y += b['vel'][1] * dt
        if b['rect'].right < 0 or b['rect'].left > WIDTH or b['rect'].bottom < 0 or b['rect'].top > HEIGHT:
            bullets.remove(b)
        elif target_alive and b['rect'].colliderect(target):
            explode_at(target.centerx, target.centery)
            target_alive = False
            bullets.remove(b)
    # Update particles
    for p in particles[:]:
        p['pos'][0] += p['vel'][0] * dt
        p['pos'][1] += p['vel'][1] * dt
        p['life'] -= dt
        if p['life'] <= 0:
            particles.remove(p)
