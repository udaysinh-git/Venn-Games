import pygame
from pygame import mixer

pygame.init()
mixer.init()



class volumeSlider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.val = initial_val
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.val = self.min + (event.pos[0] - self.rect.x) / self.rect.width * (
                    self.max - self.min
                )
                self.val = max(min(self.val, self.max), self.min)
                pygame.mixer.music.set_volume(self.val)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                self.rect.x,
                self.rect.y,
                (self.val - self.min) / (self.max - self.min) * self.rect.width,
                self.rect.height,
            ),
        )
