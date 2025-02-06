import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
PARTICLE_COLOR = (0, 255, 255)
INFECTED_COLOR = (0, 255, 0)
IMMUNE_COLOR = (255, 165, 0)
DEAD_COLOR = (128, 128, 128)
PARTICLE_COUNT = 1000
PARTICLE_RADIUS = 2
SPEED_RANGE = (-1, 1)
IMMUNITY_TIME = 14

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Contagion Sim")

class Particle:
    def __init__(self, infected=False):
        self.x = random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
        self.y = random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)
        self.vx = random.choice([random.uniform(*SPEED_RANGE) for _ in range(2)])
        self.vy = random.choice([random.uniform(*SPEED_RANGE) for _ in range(2)])
        self.infected = infected
        self.immune = False
        self.dead = False
        self.infection_time = time.time() if infected else None


    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x - PARTICLE_RADIUS <= 0 or self.x + PARTICLE_RADIUS >= WIDTH:
            self.vx *= -1
        if self.y - PARTICLE_RADIUS <= 0 or self.y + PARTICLE_RADIUS >= HEIGHT:
            self.vy *= -1

        if self.infected and not self.immune:
            if time.time() - self.infection_time >= IMMUNITY_TIME:
                if random.randint(1, 10) == 10:
                    self.dead = True
                    self.infected = False
                    self.vy = 0
                    self.vx = 0
                else:
                    self.immune = True
                    self.infected = False
        if self.dead:
                pass
        if self.immune and (time.time() - self.infection_time) >= (IMMUNITY_TIME+(IMMUNITY_TIME/2)):
            self.immune = False
            self.infected = False
        
                


    def check_collision(self, other):
        if other.dead or self.dead:
            pass
        else:
            dx = self.x - other.x
            dy = self.y - other.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < 2 * PARTICLE_RADIUS:
                self.vx, other.vx = other.vx, self.vx
                self.vy, other.vy = other.vy, self.vy
                if random.randint(1, 4) > 1:
                    if (self.infected and not self.immune and not other.immune) or (other.infected and not other.immune and not self.immune):
                        self.infected = True
                        other.infected = True
                        if not self.infection_time:
                            self.infection_time = time.time()
                        if not other.infection_time:
                            other.infection_time = time.time()

    def draw(self, screen):
        if self.immune:
            color = IMMUNE_COLOR
        elif self.infected:
            color = INFECTED_COLOR
        elif self.dead:
            color = DEAD_COLOR
        else:
            color = PARTICLE_COLOR

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), PARTICLE_RADIUS)

particles = [Particle(infected=(i == 0)) for i in range(PARTICLE_COUNT)]

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for i, particle in enumerate(particles):
        particle.move()
        for j in range(i + 1, len(particles)):
            particle.check_collision(particles[j])
        particle.draw(screen)
    innocent_count = sum(1 for p in particles if not p.infected and not p.immune and not p.dead)
    dead_count = sum(1 for p in particles if p.dead)
    overall_count = sum(1 for p in particles if p)
    infected_count = sum(1 for p in particles if p.infected)
    immune_count = sum(1 for p in particles if p.immune)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Infected: {infected_count}  Immune: {immune_count} Overall: {overall_count} Innocent: {innocent_count} Dead: {dead_count}" , True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(10)

#live graph



pygame.quit()
