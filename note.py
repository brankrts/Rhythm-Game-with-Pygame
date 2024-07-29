import pygame

class Note:
    ICON_SIZE = (60, 60)  #
    CIRCLE_THICKNESS = 3  
    CIRCLE_SPEED =92.1  
    
    ICON_PATHS = {
        '←': 'assets/arrow_left.png',
        '→': 'assets/arrow_right.png',
        '↑': 'assets/arrow_up.png',
        '↓': 'assets/arrow_down.png',
        '←→': None,  
        '←↑': None,
        '→↑': None,
        '←↓': None,
        '→↓': None,
        '↓↑': None
    }

    def __init__(self, x, y, direction, is_diagonal=False,appear_time = None):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_diagonal = is_diagonal
        self.start_time = pygame.time.get_ticks() + appear_time
        self.icon = self.load_icon(direction)
        self.circle_radius = 100  
        self.max_radius = self.circle_radius
        self.pair = None
        self.appear_time = appear_time
        self.is_fist_update = True


    def load_icon(self, direction):
        icon_path = self.ICON_PATHS.get(direction)
        if icon_path:
            icon = pygame.image.load(icon_path)
            return pygame.transform.scale(icon, self.ICON_SIZE)
        return pygame.Surface(self.ICON_SIZE) 

    def update(self,song):
        if self.is_fist_update:
            self.start_time = pygame.time.get_ticks()
            self.is_fist_update = False
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.circle_radius = self.max_radius - (elapsed_time / 1000) * self.CIRCLE_SPEED
        if self.circle_radius < self.ICON_SIZE[0] / 2 :
            song.play()
            return False
        return True 

        
    def draw(self, screen):
        if self.is_diagonal and self.pair:
            icons = {
                '←→': ('←', '→'),
                '←↑': ('←', '↑'),
                '→↑': ('→', '↑'),
                '←↓': ('←', '↓'),
                '→↓': ('→', '↓'),
                '↓↑': ('↓', '↑')
            }
            icon1, icon2 = icons.get(self.direction)
            img1 = pygame.image.load(self.ICON_PATHS[icon1])
            img1 = pygame.transform.scale(img1, self.ICON_SIZE)
            img2 = pygame.image.load(self.ICON_PATHS[icon2])
            img2 = pygame.transform.scale(img2, self.ICON_SIZE)

            screen.blit(img1, (self.x - self.ICON_SIZE[0] // 2, self.y - self.ICON_SIZE[1] // 2))
            screen.blit(img2, (self.pair.x - self.ICON_SIZE[0] // 2, self.pair.y - self.ICON_SIZE[1] // 2))
            pygame.draw.line(screen, self.get_color(), (self.x, self.y), (self.pair.x, self.pair.y), 5)
            pygame.draw.circle(screen, pygame.Color('white'), (int(self.x), int(self.y)), int(self.circle_radius), self.CIRCLE_THICKNESS)
        else:
            img = self.icon
            img_rect = img.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(img, img_rect)
            pygame.draw.circle(screen, pygame.Color('white'), (int(self.x), int(self.y)), int(self.circle_radius), self.CIRCLE_THICKNESS)

    def get_color(self):
        if '→' in self.direction and '←' in self.direction:
            return pygame.Color('blue')
        elif '↑' in self.direction and '↓' in self.direction:
            return pygame.Color('orange')
        else:
            return pygame.Color('purple')

    def set_pair(self, pair_note):
        self.pair = pair_note
        pair_note.pair = self

