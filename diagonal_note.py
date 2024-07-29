import pygame
class DiagonalNote:
    def __init__(self, note1, note2 , appear_time,diagonal_hit_sound):
        self.note1 = note1
        self.note2 = note2
        self.direction = note1.direction  
        self.note1.set_pair(self.note2)
        self.appear_time = appear_time
        self.diagonal_hit_sound = diagonal_hit_sound

    def draw(self, screen):
        
        self.note1.draw(screen)
        self.note2.draw(screen)
        pygame.draw.line(screen, self.note1.get_color(), (self.note1.x, self.note1.y), (self.note2.x, self.note2.y), 5)

    def update(self,song):
        note1_updated = self.note1.update(self.diagonal_hit_sound)
        note2_updated = self.note2.update(self.diagonal_hit_sound)
        return note1_updated or note2_updated

    def remove(self):
        return self.note1, self.note2