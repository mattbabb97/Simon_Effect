#   ,-,--.   .=-.-.       ___     _,.---._    .-._                  ,-,--.   ,---.                    ,-,--.  
# ,-.'-  _\ /==/_ /.-._ .'=.'\  ,-.' , -  `. /==/ \  .-._         ,-.'-  _\.--.'  \   ,--.-.  .-,--.,-.'-  _\ 
#/==/_ ,_.'|==|, |/==/ \|==|  |/==/_,  ,  - \|==|, \/ /, /       /==/_ ,_.'\==\-/\ \ /==/- / /=/_ //==/_ ,_.' 
#\==\  \   |==|  ||==|,|  / - |==|   .=.     |==|-  \|  |        \==\  \   /==/-|_\ |\==\, \/=/. / \==\  \    
# \==\ -\  |==|- ||==|  \/  , |==|_ : ;=:  - |==| ,  | -|         \==\ -\  \==\,   - \\==\  \/ -/   \==\ -\   
# _\==\ ,\ |==| ,||==|- ,   _ |==| , '='     |==| -   _ |         _\==\ ,\ /==/ -   ,| |==|  ,_/    _\==\ ,\  
#/==/\/ _ ||==|- ||==| _ /\   |\==\ -    ,_ /|==|  /\ , |        /==/\/ _ /==/-  /\ - \\==\-, /    /==/\/ _ | 
#\==\ - , //==/. //==/  / / , / '.='. -   .' /==/, | |- |        \==\ - , |==\ _.\=\.-'/==/._/     \==\ - , / 
# `--`---' `--`-` `--`./  `--`    `--`--''   `--`./  `--`         `--`---' `--`        `--`-`       `--`---'  
                                                                                                                                
import sys                  # Import the 'system' library
import random               # Import the 'random' library which gives cool functions for randomizing numbers
import math                 # Import the 'math' library for more advanced math operations
import time                 # Import the 'time' library for functions of keeping track of time (ITIs, IBIs etc.)
import datetime
import os                   # Import the operating system (OS)
import glob                 # Import the glob function
import pygame               # Import Pygame to have access to all those cool functions
import Matts_Toolbox        # Import Matt's Toolbox with LRC specific functions

pygame.init()               # This initializes all pygame modules

# READ TECHNICAL FILES ------------------------------------------------------------------------------------------------

# Grab the monkey name from monkey.txt
with open("monkey.txt") as f:
    monkey = f.read()

# Set Current Date
today = time.strftime('%Y-%m-%d')

# ----------------------------------------------------------------------------------------------------------------------

"""SET UP LOCAL VARIABLES --------------------------------------------------------------------------------------------"""

white = (255, 255, 255)                                         # This sets up colors you might need
black = (0, 0, 0)                                               # Format is (Red, Green, Blue, Alpha)
green = (0, 200, 0)                                             # 0 is the minimum 260 is the maximum
red = (250, 0, 0)                                               # Alpha is the transparency of a color
transparent = (0, 0, 0, 0)

"""Put your sounds here"""
sound_chime = pygame.mixer.Sound("chime.wav")                   # This sets your trial initiation sound
sound_correct = pygame.mixer.Sound("correct.wav")               # This sets your correct pellet dispensing sound
sound_incorrect = pygame.mixer.Sound("Incorrect.wav")           # This sets your incorrect sound

"""Put your Screen Parameters here"""
scrSize = (800, 600)                                            # Standard Resolution of Monkey Computers is 800 x 600
scrRect = pygame.Rect((0, 0), scrSize)                          # Sets the shape of the screen to be a rectangle
fps = 60                                                        # Frames Per Second


"""FILE MANIPULATION FUNCTIONS --------------------------------------------------------------------------------------"""

# Create an Output File
from Matts_Toolbox import writeLn

# Name the file of your Data Output
from Matts_Toolbox import makeFileName

# Get parameters from parameters.txt
from Matts_Toolbox import getParams

# Save parameters into their own file for safe keeping
from Matts_Toolbox import saveParams

"""SCREEN MANIPULATION FUNCTIONS ------------------------------------------------------------------------------------"""
from Matts_Toolbox import setScreen

from Matts_Toolbox import refresh

        # Argument to pass: Surface

"""HELPER FUNCTIONS -------------------------------------------------------------------------------------------------"""
# Quit Program Function
from Matts_Toolbox import quitEscQ

# Sound Playing Function
from Matts_Toolbox import sound

# Pellet Dispensing Function
from Matts_Toolbox import pellet

# Moving the Cursor
from Matts_Toolbox import joyCount
from Matts_Toolbox import moveCursor

from Matts_Toolbox import pseudorandomize
from Matts_Toolbox import shuffle_array

"""LIST OF TODOS ----------------------------------------------------------------------------------------------------"""

# TODO: Work on writing data into excel file
# TODO: Check to make sure training parameters work
# TODO: Delete excess/unused code
# TODO: Remove print() statements for seconds

"""ICON CLASS -------------------------------------------------------------------------------------------------------"""

from Matts_Toolbox import Box

# Draws the Icons for Ephemeral and Permanent buttons
class Icon(Box):
    def __init__(self, PNG, position, scale):                                  # Pass the image and position (x,y)
        super(Icon, self).__init__()
        image = pygame.image.load(PNG).convert_alpha()                          # image = image you passed in arguments
        self.size = image.get_size()                                            # Get the size of the image
        self.image = pygame.transform.smoothscale(image, scale)                 # Scale the image = scale inputted
        self.rect = self.image.get_rect()                                       # Get rectangle around the image
        self.rect.center = self.position = position                             # Set rectangle and center at position
        self.mask = pygame.mask.from_surface(self.image)                        # Creates a mask object

    def mv2pos(self, position):                                           # Move the Image obj to position (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position = position


"""TRIAL CLASS -----------------------------------------------------------------------------------------------------"""

class Trial(object):
    def __init__(self):
        super(Trial, self).__init__()
        self.train_level = train_level                      # Level of Training
        self.side_bias = side_bias
        self.trial_number = 0                               # Trial Number {1 - 80}
        self.trial_within_block = -1                        # Trial Within the current block {0 - 9}
        self.block = 1                                      # Block number {1-20}
        self.block_length = trials_per_block                # Number of trials per block = stored in parameters.txt
        self.blocks_per_session = blocks_per_session        # Number of blocks per session stored in parameters.txt
        self.LorR = (0, 0)
        self.startphase = True                              # start button
        self.phase1 = False                                 # draw image and buttons
        self.phase2 = False                                 # phase2 = not used by "SIMON_TRAIN.py"
        self.stimID = 0                                     # stimID used to indicate which stimuli flashes = not used by "SIMON_TRAIN.py"
        self.trial_type = [1, 1, 1, 2, 2, 2, 1, 1, 1, 2,
                           2, 2, 1, 1, 1, 2, 2, 2, 1, 2]    # Trial Type = 1: Blue Icon -- Trial Type = 2: Red Icon
        if self.train_level >= 3:
            pseudorandomize(self.trial_type)

        # Keep Track of Training Performance
        self.correct_pct = 0.00 
        self.num_correct = 0
        self.consecutive = 0



        self.stimuli = []                              # Create a blank list for stimuli input
        self.stimuliPosition = []                      # Create a blank list for Left/Right Positions

    def new(self):
        global start_time
        global subselection
        global SELECT
        SELECT = -1
        self.trial_number += 1                                                # Increment trial number by 1
        self.trial_within_block += 1                                          # Increment trial within block by 1
        sound_chime.play()
        print("Trial: " + str(self.trial_number))
        print("Trial_within_block: " + str(self.trial_within_block))
        #print("Trial Type: " + str(self.trial_type[self.trial_within_block]))
        print("Block: " + str(self.block))

        if self.trial_within_block == self.block_length:                      # If this is the last trial in the block
            self.trial_within_block = 0                                       # Reset this to 0           
            self.newBlock()                                                   # Run .newBlock()
            print("Block Complete!")

        self.startphase = True
        self.phase1 = False
        self.phase2 = False

        pseudorandomize(icon_positions)                                 # Randomise the Left/Right Positions
        self.create_stimuli()                                           # Run .create_stimuli()
        cursor.mv2pos((400, 550))                                       # Move the cursor to the start position
        start_time = pygame.time.get_ticks()


    def newBlock(self):
        """Moves program to the next block and randomizes the trial types"""
        self.stimID = 0
        self.block += 1                                                 # Increment block by 1

        if self.train_level == 1:
            self.train_level += 1
            print("Increasing  Training Level to level: " + str(self.train_level))

        elif self.train_level == 2:
            self.train_level += 1
            pseudorandomize(self.trial_type)
            pseudorandomize(self.trial_type)
            

        elif self.train_level >= 3:
            pseudorandomize(self.trial_type)
            self.correct_pct = self.num_correct / 20.00
            if self.correct_pct >= 0.74:
                self.consecutive += 1
                if self.consecutive == 2:
                    print("TRAINING LEVEL PASSED")
                    self.train_level += 1
                    print("Increasing  Training Level to level: " + str(self.train_level))
                    self.consecutive = 0
                else:
                    pass
            else:
                self.consecutive = 0

        self.num_correct = 0

        if self.block > self.blocks_per_session:                             # Check if this is the last block in the session
            print("Session Complete!")                                          # If it is, then quit!
            pygame.quit()
            sys.exit()

    def create_stimuli(self):
        """Create the stimuli based on the trial type"""
        global icon_condition

        if self.train_level >= 5:
            Icons = [Icon("start.png", (150, 200), (140, 140)),
                     Icon("imageA.png", (0, 0), (150, 150)),
                     Icon("imageB.png", (0, 0), (150, 150)),
                     Icon("Blue_Button_Blank.png", (0, 0), (400, 400)),
                     Icon("Red_Button_Blank.png", (0, 0), (400, 400)),
                     Icon("blank_button.png", (0,0), (400, 400))]
        else:
            Icons = [Icon("start.png", (150, 200), (140, 140)),
                     Icon("imageA.png", (0, 0), (150, 150)),
                     Icon("imageB.png", (0, 0), (150, 150)),
                     Icon("Blue_Button.png", (0, 0), (400, 400)),
                     Icon("Red_Button.png", (0, 0), (400, 400)),
                     Icon("blank_button.png", (0,0), (400, 400))]

        # Blue Triangle Trials
        if self.trial_type[self.trial_within_block] == 1:
            if self.train_level == 1:
                self.stimuli = [Icons[0], Icons[1], Icons[3], Icons[5]]
            else:
                self.stimuli = [Icons[0], Icons[1], Icons[3], Icons[4]]

        # Red Circle Trials
        elif self.trial_type[self.trial_within_block] == 2:
            if self.train_level == 1:
                self.stimuli = [Icons[0], Icons[2], Icons[5], Icons[4]]
            else:
                self.stimuli = [Icons[0], Icons[2], Icons[3], Icons[4]]


        self.stimID += 1



# USE THIS IF DIFFERENT ICON CONDITIONS AND TRAINING LEVELS ONLY 
        
        #if icon_condition == 1:
        #    
        #    if self.train_level == 1:
        #        train_stim = glob.glob('stimuli/train1/*.png')
        #    elif self.train_level == 2:
        #        train_stim = glob.glob('stimuli/train2/*.png')
        #    elif self.train_level == 3:
        #        train_stim = glob.glob('stimuli/train3/*.png')
        #    elif self.train_level == 4:
        #       print("Training Complete!")
        #        pygame.quit()
        #        sys.exit()
                
        #elif icon_condition == 2:
        #    
        #    if self.train_level == 1:
        #        train_stim = glob.glob('stimuli/train1/*.png')
        #    elif self.train_level == 2:
        #        train_stim = glob.glob('stimuli/train2/*.png')
        #    elif self.train_level == 3:
        #        train_stim = glob.glob('stimuli/train3/*.png')
        #    elif self.train_level == 4:
        #        print("Training Complete!")
        #        pygame.quit()
        #        sys.exit()           


    def draw_start(self):
        """Draw the start button at center of the screen"""
        self.stimuli[0].mv2pos((400, 300))
        self.stimuli[0].draw(screen)

    def draw_stimuli(self):
        """Draw the stimuli at their positions after start button is selected"""
        global icon_positions
        global button_positions
        self.stimuli[1].mv2pos((400, 100))
        self.stimuli[1].draw(screen)

        self.stimuli[2].mv2pos(button_positions[1])
        self.stimuli[3].mv2pos(button_positions[0])
        self.stimuli[2].draw(screen)
        self.stimuli[3].draw(screen)


    def get_trial_type(self):
        return self.trial_type[self.trial_within_block]
        print("Trial Type: " + str(self.trial_type[self.trial_within_block]))

    def trial_duration(self):
        global duration
        global timer
        global start_time
        global SELECT
        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000)
            print(seconds)
        if seconds > duration and SELECT != -1:
            seconds = seconds
        elif seconds > duration and SELECT == -1:
            sound(False)
            start_time = pygame.time.get_ticks()
            self.trial_number -= 1
            self.trial_within_block -= 1
            self.stimID -= 1
            seconds = 0
            selection = 0
            self.startphase = True
            self.new()

        return seconds


    def response_time(self):
        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() - start_time) / 1000)

        return seconds
        
    
#----------------------------------------------------------------

    def start(self):
        global SELECT
        global timer
        global start_time
        self.draw_start()
        cursor.draw(screen)
        moveCursor(cursor, only = 'up')

        if cursor.collides_with(self.stimuli[0]):
            screen.fill(white)
            start_time = pygame.time.get_ticks()
            self.startphase = False
            self.phase1 = True


    def run_trial(self):
        global SELECT
        global timer
        global start_time
        global button_positions
        
        cursor.draw(screen)
        #moveCursor(cursor, only = 'left, right')
        self.stimuli[0].mv2pos((-50, -50))
        self.stimuli[0].size = 0
        self.draw_stimuli()
        self.trial_duration()
        self.response_time()

        # If the Blue Triangle Appears
        if self.trial_type[self.trial_within_block] == 1:
            # If a LEFT side bias is present
            if self.side_bias == 1:
                if cursor.position[0] <= 320:
                    moveCursor(cursor, only = 'right')
                else:
                    moveCursor(cursor, only = 'left, right')
            else:
                moveCursor(cursor, only = 'left, right')
                
            if SELECT == 2:
                self.LorR = button_positions[1]
                self.write(data_file, self.left_or_right(), self.response_time(), 1)
                sound(True)
                pellet()
                self.num_correct += 1
                screen.fill(white)
                refresh(screen)
                pygame.time.delay(ITI * 1000)
                self.new()
            elif SELECT == 3:
                self.LorR = button_positions[0]
                self.write(data_file, self.left_or_right(), self.response_time(), 0)
                sound(False)
                screen.fill(white)
                refresh(screen)
                pygame.time.delay(time_out * 1000)
                self.new()
                

        # If the Orange Circle Appears
        elif self.trial_type[self.trial_within_block] == 2:
            # If a RIGHT side bias is present
            if self.side_bias == 2:
                if cursor.position[0] >= 480:
                    moveCursor(cursor, only = 'left')
                else:
                    moveCursor(cursor, only = 'left, right')
            else:
                moveCursor(cursor, only = 'left, right')

            if SELECT == 2:
                self.LorR = button_positions[1]
                self.write(data_file, self.left_or_right(), self.response_time(), 0)
                sound(False)
                screen.fill(white)
                refresh(screen)
                pygame.time.delay(time_out * 1000)
                self.new()
            elif SELECT == 3:
                self.LorR = button_positions[0]
                self.write(data_file, self.left_or_right(), self.response_time(), 1)
                sound(True)
                pellet()
                self.num_correct += 1
                screen.fill(white)
                refresh(screen)
                pygame.time.delay(ITI * 1000)
                self.new()
            

    def left_or_right(self):
        global button_positions
        if self.LorR == button_positions[0]:
            return "left"
        elif self.LorR == button_positions[1]:
            return "right"

    def write(self, file, side, time_taken, correct):
        global icon_condition
        now = time.strftime('%H:%M:%S')
        # Training data
        data = [monkey, today, now, icon_condition, self.train_level, self.block, self.trial_number, "training", side, time_taken, self.trial_type[self.trial_within_block], correct]
        
        # Testing data
        #data = [monkey, today, now, self.session_type, self.block, self.trial_number, self.trial_type[self.trial_within_block], side, time_taken, correct]
        writeLn(file, data)



# ---------------------------------------------------------------------------------------------------------------------


# UPLOAD TASK PARAMETERS ----------------------------------------------------------------------------------------------
varNames = ['full_screen', 'train_level', 'icon_condition', 'session_type', 'trials_per_block', 'blocks_per_session', 'ITI',
            'duration', 'run_time', 'time_out', 'side_bias']
params = getParams(varNames)
globals().update(params)

full_screen = params['full_screen']                     # Since your parameters are stored in a dictionary
train_level = params['train_level']                       # You can pull their value out with dictionary[key]
icon_condition = params['icon_condition']
session_type = params['session_type']
trials_per_block = params['trials_per_block']
blocks_per_session = params['blocks_per_session']
ITI = params['ITI']
duration = params['duration']
run_time = params['run_time']
time_out = params['time_out']
side_bias = params['side_bias']


# START THE CLOCK
clock = pygame.time.Clock()
start_time = (pygame.time.get_ticks() / 1000)
stop_after = run_time * 60 * 1000

# CREATE THE TASK WINDOW
screen = setScreen(full_screen)
pygame.display.set_caption("Simon_Says_Training")
display_icon = pygame.image.load("Monkey Icon.png")
pygame.display.set_icon(display_icon)
screen.fill(white)

# DEFINE THE CURSOR
cursor = Box(color = red, speed = 8, circle = True)


"""MAKE ICONS FROM PNGs-------------------------------------------------------------------------------------------"""

button_positions = [(100, 350), (718, 350)]                             # Set the LEFT/RIGHT positions for the button icons
icon_positions = [(175, 300), (625, 300)]                               # Set the LEFT/RIGHT positions for the target icons




"""CREATE THE DATA FILE-------------------------------------------------------------------------------------------"""
data_file = makeFileName('Simon_Says_Train')
writeLn(data_file, ['monkey', 'date', 'time', 'icon_condition','train_level', 'block', 'trial_number', 'trial_type',
                    'response_side', 'response_time', 'red_or_blue', 'correct_or_incorrect'])



"""SET UP IS COMPLETE - EVERYTHING BELOW THIS IS RUNNING THE MAIN PROGRAM"""


# MAIN GAME LOOP ------------------------------------------------------------------------------------------------------

trial = Trial()             # Initialize a new Trial


trial.new()                 # Begin ;)

running = True
while running:
    quitEscQ()
    timer = (pygame.time.get_ticks() / 1000)
    if timer > run_time:
        pygame.quit()
        sys.exit()
    screen.fill(white)
    cursor.draw(screen)

    SELECT = cursor.collides_with_list(trial.stimuli)
    clock.tick(fps)
    if trial.startphase == True:
        trial.start()
    elif trial.startphase == False:
        if trial.phase1 == True:
            trial.run_trial()




    refresh(screen)

# --------------------------------------------------------------------------------------------------------------------
