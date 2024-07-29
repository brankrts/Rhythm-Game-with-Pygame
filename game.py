import pygame
from diagonal_note import DiagonalNote
from input_handler import InputHandler
from note_manager import NoteManager
from score_manager import ScoreManager
from modal_manager import ModalManager

class Game:
    def __init__(self, screen, clock, bpm, screen_width, screen_height, fps , difficult , mode , peak_times,step_time_ms):
        self.screen = screen
        self.clock = clock
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.bpm = bpm
        self.note_hit_sound = pygame.mixer.Sound('./musics/click2_sound.mp3')
        self.note_hit_sound_diagonal = pygame.mixer.Sound('./musics/click2_sound.mp3')
        self.background_image = pygame.transform.scale(pygame.image.load('./assets/cat.jpg'), (screen_width, screen_height))
        self.running = True
        self.game_over = False
        self.font = pygame.font.SysFont(None, 36)
        self.difficulty = difficult
        self.peak_times = peak_times
        self.mode = mode
        self.step_time_ms = step_time_ms
        self.modal_manager = ModalManager(screen, pygame.font.SysFont(None, 36), screen_width, screen_height)
        self.input_handler = InputHandler(self.fps)

    def get_difficulty_settings(self, difficulty):
        if difficulty == 'easy':
            return 0.4, 5000
        elif difficulty == 'medium':
            return 0.3, 10
        elif difficulty == 'hard':
            return 0.2, 15
        else:
            return 0.16 , 20


    def start_game(self):
            note_interval, missed_value = self.get_difficulty_settings(self.difficulty)
            self.note_manager = NoteManager(self.screen_width, self.screen_height, note_interval, self.screen , self.mode , self.peak_times , self.step_time_ms)
            self.score_manager = ScoreManager(self.screen, self.font, missed_value, self.screen_width, self.screen_height)
            self.show_countdown() 
            self.game_loop()

    def load_music(self,music):
        self.is_music_loaded = False
        self.music = music
        return self.is_music_loaded

    def show_countdown(self):
        countdown_font = pygame.font.SysFont(None, 74)
        clock = pygame.time.Clock()  
        countdown_start_time = pygame.time.get_ticks()  
        countdown_duration = 5000  
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - countdown_start_time

            if elapsed_time > countdown_duration:
                break

            remaining_time = max(0, (countdown_duration - elapsed_time) // 1000)
            
            self.screen.fill((0, 0, 0))
            countdown_text = countdown_font.render(f"Starting in {remaining_time}", True, (255, 255, 255))
            self.screen.blit(countdown_text, (self.screen_width // 2 - countdown_text.get_width() // 2,
                                            self.screen_height // 2 - countdown_text.get_height() // 2))
            pygame.display.flip()
            clock.tick(30) 

    def update(self):
        self.note_manager.update(self.score_manager.handle_incorrect,self.note_hit_sound)

    def game_loop(self):
        self.note_manager.set_music_start_time(pygame.time.get_ticks())
        self.start_music()
        while self.running:
            if self.game_over or not self.is_music_finish():
                self.handle_game_over()
                continue

            self.input_handler.handle_events()
            self.handle_key_presses()
            self.screen.blit(self.background_image, (0, 0))
            self.update()
            self.score_manager.draw_blue_circle()
            self.score_manager.draw_score()

            if self.score_manager.missed_notes >= self.score_manager.max_missed_notes:
                self.game_over = True

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

    def handle_key_presses(self):

        if not self.note_manager.note_queue:
            return

        expected_note = self.note_manager.note_queue[0]
        direction = expected_note.direction

        if self.input_handler.is_key_valid(direction):

            if expected_note in self.note_manager.notes:

                if isinstance(expected_note, DiagonalNote):
                    self.score_manager.correct_count += 2
                    self.note_hit_sound.play()
                else:
                    self.score_manager.correct_count += 1
                    self.note_hit_sound.play()

                self.note_manager.notes.remove(expected_note)
                self.note_manager.note_queue.pop(0)
                self.score_manager.fill_blue_circle()
        self.input_handler.key_pressed = {key: False for key in self.input_handler.key_pressed} 

    def handle_game_over(self):
        self.stop_music()
        self.modal_manager.draw_modal(self.score_manager.correct_count)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_l:
                    self.running = False
                    pygame.quit()
                elif event.key == pygame.K_q:
                    self.running = False
    def reset_game(self):
        self.note_manager.notes.clear()
        self.note_manager.note_queue.clear()
        self.note_manager.last_note_time = pygame.time.get_ticks()
        self.score_manager.correct_count = 0
        self.score_manager.incorrect_count = 0
        self.score_manager.missed_notes = 0
        self.game_over = False
        self.note_manager.initialize_notes()
        self.start_music()

    def start_music(self):
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.15)

    def stop_music(self):
        pygame.mixer.music.stop()
    def is_music_finish(self):
        return pygame.mixer.music.get_busy()
