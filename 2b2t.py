import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Parkour Game")
clock = pygame.time.Clock()

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

class Player:
    def __init__(self):
        self.pos = Vector3(0, -3, 0)
        self.vel = Vector3(0, 0, 0)
        self.angle_y = 0
        self.angle_x = 0
        self.on_ground = False
        self.speed = 0.15
        self.jump_force = 0.5
        self.gravity = 0.015
    
    def update(self, keys):
        forward = Vector3(math.sin(self.angle_y) * 0.5, 0, math.cos(self.angle_y) * 0.5)
        right = Vector3(math.cos(self.angle_y) * 0.5, 0, -math.sin(self.angle_y) * 0.5)
        
        if keys[pygame.K_w]:
            self.vel.x += forward.x * self.speed
            self.vel.z += forward.z * self.speed
        if keys[pygame.K_s]:
            self.vel.x -= forward.x * self.speed
            self.vel.z -= forward.z * self.speed
        if keys[pygame.K_a]:
            self.vel.x -= right.x * self.speed
            self.vel.z -= right.z * self.speed
        if keys[pygame.K_d]:
            self.vel.x += right.x * self.speed
            self.vel.z += right.z * self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = self.jump_force
            self.on_ground = False
        
        self.vel.x *= 0.85
        self.vel.z *= 0.85
        self.vel.y -= self.gravity
        
        self.pos = self.pos + self.vel
        
        if self.pos.y < -3:
            self.pos.y = -3
            self.vel.y = 0
            self.on_ground = True

def project(point, angle_x, angle_y):
    x, y, z = point.x, point.y, point.z
    
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    
    x, z = x * cos_y - z * sin_y, x * sin_y + z * cos_y
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    
    if z < 0.1:
        return None
    
    scale = 400 / z
    screen_x = WIDTH // 2 + x * scale
    screen_y = HEIGHT // 2 - y * scale
    
    return (screen_x, screen_y, z)

def draw_box(pos, size, angle_x, angle_y, color):
    vertices = [
        Vector3(pos.x - size, pos.y - size, pos.z - size),
        Vector3(pos.x + size, pos.y - size, pos.z - size),
        Vector3(pos.x + size, pos.y + size, pos.z - size),
        Vector3(pos.x - size, pos.y + size, pos.z - size),
        Vector3(pos.x - size, pos.y - size, pos.z + size),
        Vector3(pos.x + size, pos.y - size, pos.z + size),
        Vector3(pos.x + size, pos.y + size, pos.z + size),
        Vector3(pos.x - size, pos.y + size, pos.z + size),
    ]
    
    projected = [project(v, angle_x, angle_y) for v in vertices]
    projected = [p for p in projected if p]
    
    if len(projected) < 3:
        return
    
    sorted_proj = sorted(projected, key=lambda p: p[2], reverse=True)
    
    pygame.draw.polygon(screen, color, [(p[0], p[1]) for p in sorted_proj[:3]])


running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            dx, dy = pygame.mouse.get_rel()
            player.angle_y -= dx * 0.01
            player.angle_x -= dy * 0.01
    
    pygame.mouse.set_visible(False)
    keys = pygame.key.get_pressed()
    
    player.update(keys)
    
    screen.fill((135, 206, 235))
    
    for pos, size, color in platforms:
        draw_box(pos, size, player.angle_x, player.angle_y, color)
    
    pygame.display.flip()

pygame.quit()
sys.exit()