import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Driving Simulation with Traffic")

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Car settings
car_img = pygame.Surface((50, 30), pygame.SRCALPHA)  # Transparent surface for the player car
pygame.draw.polygon(car_img, RED, [(0, 0), (50, 15), (0, 30)])  # Player car shape
car_pos = [width // 2, height // 2]
car_angle = 0  # in degrees
car_speed = 0
max_speed = 5
acceleration = 0.1
deceleration = 0.05
turn_speed = 3

# Traffic settings
traffic_cars = []
num_traffic_cars = 5
traffic_speed = 2

# Create traffic cars with random positions
for _ in range(num_traffic_cars):
    traffic_pos = [random.randint(0, width), random.randint(0, height)]
    traffic_angle = random.randint(0, 360)
    traffic_cars.append([traffic_pos, traffic_angle])

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Main simulation loop
running = True
while running:
    window.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key press handling for player car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_speed = min(car_speed + acceleration, max_speed)
    elif keys[pygame.K_DOWN]:
        car_speed = max(car_speed - deceleration, -max_speed / 2)
    else:
        car_speed = max(0, car_speed - deceleration) if car_speed > 0 else min(0, car_speed + deceleration)

    if keys[pygame.K_LEFT]:
        car_angle += turn_speed
    if keys[pygame.K_RIGHT]:
        car_angle -= turn_speed

    # Update player car position based on angle and speed
    car_pos[0] += car_speed * math.cos(math.radians(car_angle))
    car_pos[1] += car_speed * math.sin(math.radians(car_angle))

    # Screen wrap-around for player car
    car_pos[0] %= width
    car_pos[1] %= height

    # Draw and update traffic cars
    for traffic_car in traffic_cars:
        traffic_pos, traffic_angle = traffic_car

        # Move traffic cars in their current direction
        traffic_pos[0] += traffic_speed * math.cos(math.radians(traffic_angle))
        traffic_pos[1] += traffic_speed * math.sin(math.radians(traffic_angle))

        # Wrap traffic cars around the screen edges
        traffic_pos[0] %= width
        traffic_pos[1] %= height

        # Draw traffic car
        traffic_img = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.polygon(traffic_img, BLUE, [(0, 0), (40, 10), (0, 20)])
        rotated_traffic = pygame.transform.rotate(traffic_img, -traffic_angle)
        traffic_rect = rotated_traffic.get_rect(center=(int(traffic_pos[0]), int(traffic_pos[1])))
        window.blit(rotated_traffic, traffic_rect.topleft)

    # Draw and update player car
    rotated_car = pygame.transform.rotate(car_img, -car_angle)
    car_rect = rotated_car.get_rect(center=(int(car_pos[0]), int(car_pos[1])))
    window.blit(rotated_car, car_rect.topleft)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS
