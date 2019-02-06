import tkinter as tk

"""
COLORS CONSTANTS
"""

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

"""
SCREEN CONSTANTS
"""

rootSystem = tk.Tk()
SCREEN_WIDTH = rootSystem.winfo_screenwidth()
SCREEN_HEIGHT = rootSystem.winfo_screenheight()
SCREEN_DIMENSION = {"WIDTH": SCREEN_WIDTH, "HEIGHT": SCREEN_HEIGHT}
WIND_ARROW_WIDTH = 100
WIND_ARROW_HEIGHT = 50

"""
MATH CONSTANTS
"""

PI = 3.14
GRAVITY = 9.8

"""
MENU CONSTANS
"""

MAIN_MENU = 1
PAUSE_MENU = 2
PLAYER_MENU = 3
VICTORY_MENU = 4

ACTION_LEAVE = -1
ACTION_WAITING = 0
ACTION_PLAY = 1
ACTION_CONTINUE = 2
ACTION_BACK_TO_MENU = 3
ACTION_CHOOSE_PLAYER = 4

"""
PLAYER CONSTANT
"""

IDLE = 1
WALK = 2
JUMP = 3
DEAD = 4

"""
GAME CONSTANTS
"""
LITTLE_CIRCLE = 25
MEDIUM_CIRCLE = 50
LARGE_CIRCLE = 75
DRILL = 10

TOPLEFT = 1
TOP = 2
TOPRIGHT = 3
LEFT = 4
RIGHT = 5
BOTLEFT = 6
BOT = 7
BOTRIGHT = 8

FRAME_PER_SECOND = 60

CONTINUE_GAME = 0
VICTORY_TEAM_1 = 1
VICTORY_TEAM_2 = 2
