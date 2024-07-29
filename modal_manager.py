import pygame

class ModalManager:
    def __init__(self, screen, font, screen_width, screen_height):
        self.screen = screen
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.modal_rect = pygame.Rect(0, 0, 400, 300)
        self.modal_rect.center = (screen_width // 2, screen_height // 2)
        self.retry_button_rect = pygame.Rect(0, 0, 150, 50)
        self.retry_button_rect.center = (screen_width // 2, screen_height // 2 + 50)
        self.lobby_button_rect = pygame.Rect(0, 0, 150, 50)  
        self.lobby_button_rect.center = (screen_width // 2, screen_height // 2 + 120) 

    def draw_modal(self, correct_count):
        pygame.draw.rect(self.screen, (0, 0, 0), self.modal_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect, 2)

        game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.modal_rect.centerx - game_over_text.get_width() // 2, self.modal_rect.centery - 100))

        score_text = self.font.render(f"Skor: {correct_count}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.modal_rect.centerx - score_text.get_width() // 2, self.modal_rect.centery - 50))

        retry_text = self.font.render("Retry (R)", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 255), self.retry_button_rect)
        self.screen.blit(retry_text, (self.retry_button_rect.centerx - retry_text.get_width() // 2, self.retry_button_rect.centery - retry_text.get_height() // 2))

        lobby_text = self.font.render("Lobby (L)", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 255, 0), self.lobby_button_rect)
        self.screen.blit(lobby_text, (self.lobby_button_rect.centerx - lobby_text.get_width() // 2, self.lobby_button_rect.centery - lobby_text.get_height() // 2))
 