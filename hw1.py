import pygame
import sys

# hw1.py
# Simple platformer using pygame
# Run: pip install pygame
# Then: python hw1.py

pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")
CLOCK = pygame.time.Clock()

# Colors
BG = (135, 206, 235)
PLAYER_COLOR = (30, 30, 220)
PLATFORM_COLOR = (100, 50, 20)
TEXT_COLOR = (0, 0, 0)
START_COLOR = (50, 200, 50)
END_COLOR = (200, 50, 50)

GRAVITY = 0.8
FRICTION = 0.8
MOVE_SPEED = 5
JUMP_SPEED = 15

FONT = pygame.font.SysFont(None, 28)

LEVEL_WIDTH = 2000  # extend level to make it longer


class Player:
    def __init__(self, x, y, w=32, h=48):
        self.rect = pygame.Rect(x, y, w, h)
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def handle_input(self, keys):
        ax = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ax = -MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ax = MOVE_SPEED
        # apply horizontal movement directly (no acceleration)
        self.vel.x = ax

        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel.y = -JUMP_SPEED
            self.on_ground = False

    def apply_physics(self):
        self.vel.y += GRAVITY
        # simple terminal velocity
        if self.vel.y > 30:
            self.vel.y = 30

    def move(self, platforms):
        # Move horizontally and resolve collisions
        self.rect.x += int(self.vel.x)
        collided = [p for p in platforms if self.rect.colliderect(p)]
        for p in collided:
            if self.vel.x > 0:
                self.rect.right = p.left
            elif self.vel.x < 0:
                self.rect.left = p.right

        # Move vertically and resolve collisions
        self.rect.y += int(self.vel.y)
        self.on_ground = False
        collided = [p for p in platforms if self.rect.colliderect(p)]
        for p in collided:
            if self.vel.y > 0:
                self.rect.bottom = p.top
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:
                self.rect.top = p.bottom
                self.vel.y = 0

    def update(self, platforms, keys):
        self.handle_input(keys)
        self.apply_physics()
        self.move(platforms)

    def draw(self, surf, offset=(0, 0)):
        r = self.rect.move(-offset[0], -offset[1])
        pygame.draw.rect(surf, PLAYER_COLOR, r)


def build_level(level_width):
    platforms = []
    # ground across the extended level
    platforms.append(pygame.Rect(0, HEIGHT - 40, level_width, 40))
    # simple floating platforms spread out further
    platforms.append(pygame.Rect(120, HEIGHT - 160, 120, 20))
    platforms.append(pygame.Rect(300, HEIGHT - 250, 160, 20))
    platforms.append(pygame.Rect(540, HEIGHT - 200, 120, 20))
    platforms.append(pygame.Rect(740, HEIGHT - 300, 160, 20))
    platforms.append(pygame.Rect(980, HEIGHT - 180, 200, 20))
    platforms.append(pygame.Rect(1240, HEIGHT - 220, 160, 20))
    platforms.append(pygame.Rect(1500, HEIGHT - 150, 200, 20))
    # a small tall pillar
    platforms.append(pygame.Rect(460, HEIGHT - 120, 40, 80))

    # start and end markers (not solid platforms)
    start_x = 20
    player_h = 48
    start_rect = pygame.Rect(start_x, HEIGHT - 40 - player_h, 32, player_h)

    end_x = level_width - 80
    end_rect = pygame.Rect(end_x, HEIGHT - 40 - 64, 48, 64)  # taller flag/goal

    return platforms, start_rect, end_rect


def draw_platforms(surf, platforms, offset=(0, 0)):
    for p in platforms:
        r = p.move(-offset[0], -offset[1])
        pygame.draw.rect(surf, PLATFORM_COLOR, r)


def main():
    platforms, start_rect, end_rect = build_level(LEVEL_WIDTH)
    player = Player(start_rect.x, start_rect.y)

    camera_x = 0
    won = False

    while True:
        dt = CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not won:
            player.update(platforms, keys)

            # check win condition: touch the end rectangle
            if player.rect.colliderect(end_rect):
                won = True
                player.vel = pygame.math.Vector2(0, 0)

        else:
            # allow restart when won
            if keys[pygame.K_r]:
                # reset player
                player.rect.topleft = (start_rect.x, start_rect.y)
                player.vel = pygame.math.Vector2(0, 0)
                won = False

        # simple camera: follow player horizontally with bounds
        camera_x = max(0, player.rect.centerx - WIDTH // 2)
        max_camera_x = LEVEL_WIDTH - WIDTH
        if camera_x > max_camera_x:
            camera_x = max_camera_x

        SCREEN.fill(BG)
        draw_platforms(SCREEN, platforms, (camera_x, 0))

        # draw start and end (non-solid markers)
        sr = start_rect.move(-camera_x, 0)
        er = end_rect.move(-camera_x, 0)
        pygame.draw.rect(SCREEN, START_COLOR, sr)
        pygame.draw.rect(SCREEN, END_COLOR, er)

        player.draw(SCREEN, (camera_x, 0))

        # HUD
        if not won:
            status = f"Pos: {player.rect.x}, {player.rect.y}  Vel: {round(player.vel.x,1)},{round(player.vel.y,1)}"
            text = FONT.render(status, True, TEXT_COLOR)
            SCREEN.blit(text, (8, 8))

            instr = FONT.render("Arrows/A/D to move, Up/Space to jump. Reach the red goal. Close window to quit.", True, TEXT_COLOR)
            SCREEN.blit(instr, (8, 36))
        else:
            win_text = FONT.render("You reached the goal! Press R to restart.", True, TEXT_COLOR)
            SCREEN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 10))

        # draw simple labels for start/end
        start_label = FONT.render("Start", True, TEXT_COLOR)
        SCREEN.blit(start_label, (sr.x + 2, sr.y - 24))
        end_label = FONT.render("Goal", True, TEXT_COLOR)
        SCREEN.blit(end_label, (er.x + 2, er.y - 24))

        pygame.display.flip()


if __name__ == "__main__":
    main()