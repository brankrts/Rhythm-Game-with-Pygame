import pygame
import time

class InputHandler:
    def __init__(self,fps):
        self.key_pressed = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        self.key_press_times = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}
        self.key_release_times = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}
        self.TOLERANCE_MS = 200  
        self.fps = fps

        self.directions = {
            '←': False,
            '→': False,
            '↑': False,
            '↓': False,
            '←→': False,
            '←↑': False,
            '→↑': False,
            '←↓': False,
            '→↓': False,
            '↓↑': False
        }

    def handle_events(self):
        current_ticks = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_pressed:
                    self.key_pressed[event.key] = True
                    self.key_press_times[event.key] =time.time() * 1000
            elif event.type == pygame.KEYUP:
                if event.key in self.key_pressed:
                    self.key_pressed[event.key] = False
                    self.key_release_times[event.key] = time.time() * 1000

        self.update_directions()

    def update_directions(self):
        self.directions['←'] = self.key_pressed[pygame.K_LEFT]
        self.directions['→'] = self.key_pressed[pygame.K_RIGHT]
        self.directions['↑'] = self.key_pressed[pygame.K_UP]
        self.directions['↓'] = self.key_pressed[pygame.K_DOWN]

        diagonal_combinations = {
            '←→': (pygame.K_LEFT, pygame.K_RIGHT),
            '←↑': (pygame.K_LEFT, pygame.K_UP),
            '→↑': (pygame.K_RIGHT, pygame.K_UP),
            '←↓': (pygame.K_LEFT, pygame.K_DOWN),
            '→↓': (pygame.K_RIGHT, pygame.K_DOWN),
            '↓↑': (pygame.K_UP, pygame.K_DOWN)
        }

        for direction, keys in diagonal_combinations.items():
            key1, key2 = keys
            time_diff = abs(self.key_press_times[key1] - self.key_press_times[key2])
            self.directions[direction] = (
                self.key_pressed[key1] and self.key_pressed[key2] and time_diff <= self.TOLERANCE_MS
            )

    def is_key_valid(self, direction):
        return self.directions.get(direction, False)