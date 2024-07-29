from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QFileDialog, QLabel, QButtonGroup, QLineEdit
import pygame
import librosa
from game import Game
from sound_analyser import SoundAnalyzer

class GameSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Game lobby")
        self.resize(600, 400)  

        layout = QVBoxLayout()

       
        self.song_label = QLabel("Select a song")
        layout.addWidget(self.song_label)

        self.select_song_button = QPushButton("Select Song")
        self.select_song_button.clicked.connect(self.select_song)
        layout.addWidget(self.select_song_button)

        self.difficulty = 'easy'
        difficulty_group = QVBoxLayout()
        self.difficulty_label = QLabel("Difficulty:")
        difficulty_group.addWidget(self.difficulty_label)

        self.easy_rb = QRadioButton("Easy")
        self.medium_rb = QRadioButton("Normal")
        self.hard_rb = QRadioButton("Hard")
        self.barashka_rb = QRadioButton("Barasha Power")
        self.easy_rb.setChecked(True)

        self.difficulty_button_group = QButtonGroup()
        self.difficulty_button_group.addButton(self.easy_rb)
        self.difficulty_button_group.addButton(self.medium_rb)
        self.difficulty_button_group.addButton(self.hard_rb)
        self.difficulty_button_group.addButton(self.barashka_rb)

        difficulty_group.addWidget(self.easy_rb)
        difficulty_group.addWidget(self.medium_rb)
        difficulty_group.addWidget(self.hard_rb)
        difficulty_group.addWidget(self.barashka_rb)
        layout.addLayout(difficulty_group)

    
        self.mode = 'standard'
        mode_group = QVBoxLayout()
        self.mode_label = QLabel("Mode:")
        mode_group.addWidget(self.mode_label)

        self.standard_rb = QRadioButton("Standard")
        self.arcade_rb = QRadioButton("With Diagonals[BETA]")
        self.standard_rb.setChecked(True)

        self.mode_button_group = QButtonGroup()
        self.mode_button_group.addButton(self.standard_rb)
        self.mode_button_group.addButton(self.arcade_rb)

        mode_group.addWidget(self.standard_rb)
        mode_group.addWidget(self.arcade_rb)
        layout.addLayout(mode_group)

       
        self.threshold_label = QLabel("Threshold:")
        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText("Enter threshold value")
        layout.addWidget(self.threshold_label)
        layout.addWidget(self.threshold_input)

    
        self.step_size_label = QLabel("Step Size (ms):")
        self.step_size_input = QLineEdit()
        self.step_size_input.setPlaceholderText("Enter step size in ms")
        layout.addWidget(self.step_size_label)
        layout.addWidget(self.step_size_input)

     
        self.start_button = QPushButton("Start Game")
        self.start_button.setEnabled(False) 
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def select_song(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a song", "", "Music Files (*.mp3)")
        if file_path:
            self.song_label.setText(f"Selected song: {file_path}")
            self.selected_song = file_path
            self.start_button.setEnabled(True) 

    def analyze_beats(self, song_path):
        y, sr = librosa.load(song_path)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return beat_times, tempo

    def start_game(self):
        pygame.init()

        if not hasattr(self, 'selected_song') or not self.selected_song:
            print("Select a song!")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(self.selected_song)
        
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 1024
        FPS = 60
        
        threshold_text = self.threshold_input.text()
        step_size_text = self.step_size_input.text()
        
        try:
            threshold = float(threshold_text) if threshold_text else 100000
            step_size_ms = float(step_size_text) if step_size_text else 60 / self.analyze_beats(self.selected_song)[1] * 1000
        except ValueError:
            print("Invalid input for threshold or step size.")
            return

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('DashaSTAR')
        clock = pygame.time.Clock()
        _, bpm = self.analyze_beats(self.selected_song)
        peak_times = SoundAnalyzer(self.selected_song, threshold, step_size_ms=step_size_ms).find_peaks()
        
        difficulty = 'easy' if self.easy_rb.isChecked() else 'medium' if self.medium_rb.isChecked() else 'hard' if self.hard_rb.isChecked() else 'barasha_power'
        mode = 'standard' if self.standard_rb.isChecked() else 'diagonal'
        game = Game(screen, clock, bpm, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, difficulty, mode, peak_times, step_size_ms)
        game.start_game()
