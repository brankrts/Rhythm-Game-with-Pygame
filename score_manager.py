import pygame

class ScoreManager:
    def __init__(self, screen, font, missed_value, screen_width , screen_height):
        self.screen = screen
        self.font = font
        self.missed_notes = 0
        self.max_missed_notes = missed_value
        self.correct_count = 0
        self.incorrect_count = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw_score(self):
        correct_text = self.font.render(f"Currect: {self.correct_count}", True, (0, 255, 0))
        incorrect_text = self.font.render(f"Missed: {self.incorrect_count}", True, (255, 0, 0))
        self.screen.blit(correct_text, (10, 10))
        self.screen.blit(incorrect_text, (10, 50))

    def draw_blue_circle(self):
        blue_circle_radius = 50
        fill_percentage = max(0, 1 - (self.missed_notes / self.max_missed_notes))
        fill_radius = int(blue_circle_radius * fill_percentage)
        pygame.draw.circle(self.screen, (0, 0, 255), (self.screen_width - 50, self.screen_height - 50), blue_circle_radius, 1)
        pygame.draw.circle(self.screen, (0, 0, 255), (self.screen_width - 50, self.screen_height - 50), fill_radius)

    def fill_blue_circle(self):

        if self.missed_notes >= 0:
            self.missed_notes -= 1

    def handle_incorrect(self, count):
        self.incorrect_count += count
        self.missed_notes += count
