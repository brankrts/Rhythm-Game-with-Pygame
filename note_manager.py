import pygame
import random
from note import Note
from diagonal_note import DiagonalNote


class NoteManager:
    def __init__(self, screen_width, screen_height, bpm,screen ,mode , peak_times , step_time_ms):
        self.peak_times = peak_times
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_x = screen_width //2
        self.note_hit_sound_diagonal = pygame.mixer.Sound('./musics/click2_sound.mp3')
        self.center_y = screen_height //2
        self.bpm = bpm    
        self.notes = []
        self.radius = 150
        self.note_queue = []
        self.last_note_time = pygame.time.get_ticks()
        self.screen = screen
        self.mode =mode
        self.music_start_time = None
        self.step_time_ms = step_time_ms
        self.peak_time_offset = 760
        self.initialize_notes()
        

    def initialize_notes(self):
        for peak_time in self.peak_times:
            if (peak_time - self.peak_time_offset <=0):
                note_appear_time = peak_time 
                self.add_random_note(note_appear_time)
                continue
            note_appear_time = peak_time - self.peak_time_offset
            self.add_random_note(note_appear_time)



    def get_arrow_coords(self, direction):
        margin_x = self.screen_width * 0.25
        margin_y = self.screen_height * 0.25
        offset_x = 60
        offset_y = 60
        if direction == 'right':
            x = random.uniform(self.center_x + self.radius, self.screen_width - margin_x) 
            y = random.uniform(self.center_y - offset_y, self.center_y + offset_y)
        elif direction == 'left':
            x = random.uniform(margin_x, self.center_x - self.radius)
            y = random.uniform(self.center_y - offset_y, self.center_y + offset_y)
        elif direction == 'up':
            x = random.uniform(self.center_x - offset_x, self.center_x + offset_x)
            y = random.uniform(margin_y, self.center_y - self.radius)
        else:  
            x = random.uniform(self.center_x - offset_x, self.center_x + offset_x)
            y = random.uniform(self.center_y + self.radius, self.screen_height - margin_y)
        return x, y 
    def set_difficult (self, difficult , mode):
        self.difficult = difficult
        self.mode = mode

    def add_random_note(self , note_appear_time):
        directions = ['←', '→', '↑', '↓']
        diagonal_directions = ['←↑', '→↑', '←↓', '→↓', '↓↑', '←→']
        probability = random.random() < 0.7 if self.mode == "diagonal" else True

        if probability:  
            direction = random.choice(directions)
            if direction == '→':
                x, y = self.get_arrow_coords("right")
            elif direction == '←':
                x, y = self.get_arrow_coords("left")
            elif direction == '↑':
                x, y = self.get_arrow_coords("up")
            else: 
                x, y = self.get_arrow_coords("down")

            new_note = Note(x, y, direction,appear_time=note_appear_time)
            self.notes.append(new_note)
            self.note_queue.append(new_note) 
        else:
            direction = random.choice(diagonal_directions)
            
            if direction == '←↑':
                x1, y1 = self.get_arrow_coords("up")
                x2, y2 = self.get_arrow_coords("left")
            elif direction == '→↑':
                x1, y1 = self.get_arrow_coords("up")
                x2, y2 = self.get_arrow_coords("right")
            elif direction == '←↓':
                x1, y1 = self.get_arrow_coords("down")
                x2, y2 = self.get_arrow_coords("left")
            elif direction == '→↓':
                x1, y1 = self.get_arrow_coords("down")
                x2, y2 = self.get_arrow_coords("right")
            elif direction == '↓↑':
                x1, y1 = self.get_arrow_coords("up")
                x2, y2 = self.get_arrow_coords("down")
                x2 = x1 
            elif direction == '←→':
                x1, y1 = self.get_arrow_coords("right")
                x2, y2 = self.get_arrow_coords("left")
                y2 = y1  

            note1 = Note(x1, y1, direction, is_diagonal=True ,appear_time=note_appear_time)
            note2 = Note(x2, y2, direction, is_diagonal=True,appear_time=note_appear_time)
            diagonal_note = DiagonalNote(note1, note2 , appear_time=note_appear_time , diagonal_hit_sound=self.note_hit_sound_diagonal)
            self.notes.append(diagonal_note)
            self.note_queue.append(diagonal_note)

    def set_music_start_time(self , time):
        self.music_start_time = time

    def update(self,handle_incorrect,song):

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.music_start_time

        for note in self.notes[:]:
            if note.appear_time <= elapsed_time:
                if note.update(song):
                    note.draw(self.screen)
                else:
                    self.notes.remove(note)
                    self.note_queue.pop(0)
                    handle_incorrect(2 if isinstance(note, DiagonalNote) else 1) 

