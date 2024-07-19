import os
import pygame
import sys
import tkinter as tk
from moviepy.editor import VideoFileClip

from core.screens import Screens
from core.splash_video import SplashVideo
from ui.tkinter.father_screen import FatherScreen
from utils.constants import Constants
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager

# Preload Sounds
sound_manager = SoundManager()
sound_manager.load_sound("splash_music", resource_path("assets\\sounds\\splash_music.mp3"))
sound_manager.set_volume("splash_music", 0.3)

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up the window to occupy the maximum resolution without full screen
screen = pygame.display.set_mode((screen_width, screen_height))
screen_selected = Screens.SPLASH
pygame.display.set_caption("BioScripts")
clock = pygame.time.Clock()

clip = VideoFileClip(resource_path("assets\\videos\\splash.mp4"))

# Calculate initial player position to center on the screen
initial_player_x = (Constants.SCREEN_WIDTH - Constants.TILE_SIZE) // 2 + 420
initial_player_y = (Constants.SCREEN_HEIGHT - Constants.TILE_SIZE) // 2 + 570

# Create Splash
splash_video = SplashVideo(screen_width, screen_height)

# Create Introduction1Video
introduction_1_video = None
# Create Introduction2Video
introduction_2_video = None

father_screen_ongoing = False

def start_father_screen():
    global pygame_paused, father_screen_ongoing
    pygame_paused = True
    if father_screen_ongoing:
        return
    father_screen_ongoing = True
    root = tk.Tk()
    def close_app(event=None):
        on_close(root)

    def on_focus_in(event):
        root.deiconify()

    def on_focus_out(event):
        root.withdraw()

    # def remove_title_bar(window):
    #     hwnd = win32gui.GetForegroundWindow()
    #     style = win32gui.GetWindowLong(hwnd, win32gui.GWL_STYLE)
    #     style &= ~win32gui.WS_CAPTION
    #     win32gui.SetWindowLong(hwnd, win32gui.GWL_STYLE, style)
    #     win32gui.SetWindowPos(hwnd, win32gui.HWND_TOP, 0, 0, 800, 600, win32gui.SWP_NOMOVE | win32gui.SWP_NOSIZE | win32gui.SWP_FRAMECHANGED)

    FatherScreen(root, close_app)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.bind("<FocusIn>", on_focus_in)
    root.bind("<FocusOut>", on_focus_out)
    # root.after(100, lambda: remove_title_bar(root))

    root.geometry(f"{screen_width}x{screen_height}+0+0")

    root.bind('<Escape>', close_app)
    root.mainloop()

def on_close(root):
    global father_screen_ongoing
    resume_pygame()
    go_to_game_screen_meet_housekeeper()
    root.destroy()
    father_screen_ongoing = False

pygame_paused = False

def pause_pygame():
    global pygame_paused
    pygame_paused = True

def resume_pygame():
    global pygame_paused
    pygame_paused = False

is_video_playing = False

text_area_rect = pygame.Rect(180, screen_height - 320, 400, 200)
font_path = os.path.join("assets", "fonts", "BavarianCrown.ttf")
font = pygame.font.Font(font_path, 32)
text_area_visible = False
text_input = ""

def go_to_game_screen_meet_housekeeper():
    global screen_selected
    print("CURRENT_SCREEN: GAME_SCREEN_MEET_HOUSEKEEPER")
    screen_selected = Screens.GAME_SCREEN_MEET_HOUSEKEEPER

def go_to_father_screen():
    global screen_selected
    print("CURRENT_SCREEN: FATHER")
    screen_selected = Screens.FATHER

# Game loop
running = True
show_overlay_analyze = False
show_overlay_dialog = False
dialog_progression = 0

def show_current_dialog():
    global show_overlay_dialog, dialog_progression
    dialog_progression += 1
    show_overlay_dialog = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if screen_selected == Screens.SPLASH:
        splash_video.play_video(screen, go_to_father_screen)
    elif screen_selected == Screens.FATHER:
        start_father_screen()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
