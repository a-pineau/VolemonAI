import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Ball properties
ball_radius = 20
dynamic_ball_pos = [WIDTH // 2 - 100, 0]  # Start slightly off-center from the static ball
static_ball_pos = [WIDTH // 2, HEIGHT - 50 - ball_radius]  # Static ball position
vertical_speed = 0
horizontal_speed = 1  # Adjusted horizontal speed
gravity = 0.5
bounce_factor = -0.7

def calculate_contact_angle(dynamic_pos, static_pos):
    dx = dynamic_pos[0] - static_pos[0]
    dy = dynamic_pos[1] - static_pos[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    vertical_speed += gravity
    dynamic_ball_pos[1] += vertical_speed
    dynamic_ball_pos[0] += horizontal_speed

    # Collision detection
    distance = math.hypot(dynamic_ball_pos[0] - static_ball_pos[0], dynamic_ball_pos[1] - static_ball_pos[1])
    if distance < ball_radius * 2:
        vertical_speed *= bounce_factor
        horizontal_speed *= -1  # Reverse horizontal direction upon collision
        contact_angle = calculate_contact_angle(dynamic_ball_pos, static_ball_pos)
        print(f"Contact angle: {contact_angle} degrees")

    # Drawing
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 255), dynamic_ball_pos, ball_radius)
    pygame.draw.circle(screen, (255, 0, 0), static_ball_pos, ball_radius)

    pygame.display.flip()
    pygame.time.delay(10)
