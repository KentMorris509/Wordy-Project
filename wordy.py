#File: wordyiteration5.py
#Authors: Kent Morris and Jacob Aujero
#Date: December 13 2022
#Description: In Iteration 5 We created the color matching for the user's entry and set up parameters and messages for their entry guesses.
# Wordy game is now up and running!



# Imports
import random
import tkinter as tk
import tkinter.font as font
from enum import Enum
import time

class BadEntry(Exception):
    pass
class BadEntry_ValidWord(Exception):
    pass
class Not_A_Word(Exception):
    pass
class Word_Not_Done(Exception):
    pass

class Wordy:
    def __init__(self):
        #Initialize the game
        # Constants
        
        self.GuessRow = 0
        self.Guess_Column = 0
        self.user_guess = ''
        self.WORD_SIZE = 5  # number of letters in the hidden word
        self.NUM_GUESSES = 6 # number of guesses that the user gets 
        self.LONG_WORDLIST_FILENAME = "long_wordlist.txt"
        self.SHORT_WORDLIST_FILENAME = "short_wordlist.txt"

        # Size of the frame that holds all guesses.  This is the upper left
        # frame in the window.
        self.PARENT_GUESS_FRAME_WIDTH = 750
        self.PARENT_GUESS_FRAME_HEIGHT = 500

        # Parameters for an individual letter in the guess frame
        # A guess frame is an individual box that contains a guessed letter.
        self.GUESS_FRAME_HEIGHT = 1
        self.GUESS_FRAME_WIDTH = 2  # the width and height of the guess box.
        self.GUESS_FRAME_PADDING = 3 
        self.GUESS_FRAME_BG_BEGIN = 'white' # background color of a guess box 
                                            # after the user enters the letter,
                                            # but before the guess is entered.
        self.GUESS_FRAME_TEXT_BEGIN = 'black' # color of text in guess box after the
                                            # user enters the letter, but before
                                            # the guess is entered.
        self.GUESS_FRAME_BG_WRONG = 'grey'  # background color of guess box
                                            # after the guess is entered, and the
                                            # letter is not in the hidden word.
        self.GUESS_FRAME_BG_CORRECT_WRONG_LOC = 'orange' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # but in the wrong location.
        self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC = 'green' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # and in the correct location.
        self.GUESS_FRAME_TEXT_AFTER = 'white' # color of text in guess box after
                                            # the guess is entered.
        self.FONT_FAMILY = 'ariel'          # Font to use for letters in the guess boxes.
        self.FONT_SIZE_GUESS = 35   # Font size for letters in the guess boxes.

        # Parameters for the keyboard frame
        self.KEYBOARD_FRAME_HEIGHT = 200
        self.KEYBOARD_BUTTON_HEIGHT = 2
        self.KEYBOARD_BUTTON_WIDTH = 3  # width of the letter buttons.  Remember,
                                        # width of buttons is measured in characters.
        self.KEYBOARD_BUTTON_WIDTH_LONG = 5 # width of the enter and back buttons.

        # The following colors for the keyboard buttons
        # follow the same specifications as the colors defined above for the guess
        # boxes.  The problem is that at least on macs, in Tkinter you cannot change
        # the background color of a button.  So you will leave the background color as the
        # default (white),and just change the color of the text in the button, 
        # instead of the background color.
        # So the text color starts as the default (black), and then changes to grey, orange, 
        # green depending on the result of the guess for that letter.
        self.KEYBOARD_BUTTON_TEXT_BEGIN = 'black' 
        self.KEYBOARD_BUTTON_TEXT_WRONG = 'grey'  
        self.KEYBOARD_BUTTON_TEXT_CORRECT_WRONG_LOC = 'orange' 
        self.KEYBOARD_BUTTON_TEXT_CORRECT_RIGHT_LOC = 'green' 

        self.KEYBOARD_BUTTON_NAMES = [   
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"]]
        
        self.Keyboard_Row_One_Button_Names = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
        self.Keyboard_Row_Two_Button_Names = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
        self.Keyboard_Row_Three_Button_Names = ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"]
        
        # Parameters for the control frame
        self.CONTROL_FRAME_HEIGHT = self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT
        self.CONTROL_FRAME_WIDTH = 300
        self.USER_SELECTION_PADDING = 10  # Horizontal padding on either side of the widgets in
                                            # the parameter frame.

        self.MESSAGE_DISPLAY_TIME_SECS = 5 # Length of time the message should be
                                            # displayed.
                                            
        self.MESSAGE_DISPLAY_TIME_SECS_MS = 5000  # length of time the message should be displayed in MS
        
        self.PROCESS_GUESS_WAITTIME = 1  # When processing a guess (changing color
                                        # of the guess frames), time to wait between
                                        # updating successive frames.
        
        self.ENTRY_SIZE = 10 # Size of entry widget

        self.Current_Letter_Guess = None #Keeps track of most recent guess
        self.Current_Guess = ""

        self.Guess_Label_Dict = {} #Stores our label frames and labels for the guessing grid
        self.Guess_Text_Dict = {}

        ''' In this Portion of code it is creating two files one for the long_wordlist and one for the short word_list
         by reading through the file and adding the words only if the their the word_size'''
         
        self.Long_wordlist = []
        self.short_wordlist = []
        
        with open(self.LONG_WORDLIST_FILENAME) as file:
            for line in file:
                word = line.strip()
                if len(word) == self.WORD_SIZE:
                    self.Long_wordlist.append(word)
        
        with open(self.SHORT_WORDLIST_FILENAME) as file:
            for line in file:
                word = line.strip()
                if len(word) == self.WORD_SIZE:
                    self.short_wordlist.append(word)

        # instance variable for Hidden Word and states
        self.Hidden_Word = None
        self.state = State.WAITING_FOR_START

            # Create window
        self.window = tk.Tk()
        self.window.title("Wordy")
        self.window.configure(bg="white")
        
        self.Frames()  # helper method to make the frames
        self.FrameLabels_and_Parameters() # helper method to make labels/checkboxes/and parameters
        self.GuessBoxes()  # helper method to make Guess Boxes in Window
        self.keyboard()  # helper method to make keyboard
         
       # Start event loop
        self.window.mainloop()
       
        
    def Frames(self):
        
        '''Helper Method to make all the frames in the window to help organize the constructor'''
        
        # Create a Quess Frame.
        self.GuessFrame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.PARENT_GUESS_FRAME_HEIGHT, width = self.PARENT_GUESS_FRAME_WIDTH, bg = "lightgrey")
        self.GuessFrame.grid(row = 1, column = 1)
        self.GuessFrame.grid_propagate(False)

        # Create Keyboard Frame
        self.KeyboardFrame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.KEYBOARD_FRAME_HEIGHT, width = self.PARENT_GUESS_FRAME_WIDTH, bg = "lightgrey")
        self.KeyboardFrame.grid(row = 2, column = 1)
        self.KeyboardFrame.grid_propagate(False)

        # Create Control Frame.
        self.Control_Frame = tk.Frame(self.window, 
            borderwidth = 1, relief = 'solid',
            height = self.CONTROL_FRAME_HEIGHT, width = self.CONTROL_FRAME_WIDTH, bg = "lightgrey")
        self.Control_Frame.grid(row = 1, column = 2, rowspan = 2)
        self.Control_Frame.grid_propagate(False)

        # Create message frame, parameter frame, and the button frame
        
        # Message Frame
        self.MessageFrame = tk.Frame(self.Control_Frame, borderwidth = 1,	
            relief	= "solid", height = self.CONTROL_FRAME_HEIGHT/3, 
            width = self.CONTROL_FRAME_WIDTH, bg = "lightgrey")
        self.MessageFrame.grid(row = 1, column = 1)
        self.MessageFrame.grid_propagate(False)
        
        # ParemeterFrame
        self.ParemeterFrame = tk.Frame(self.Control_Frame, 
            borderwidth = 1, relief = 'solid',
            height = self.CONTROL_FRAME_HEIGHT/3, width = self.CONTROL_FRAME_WIDTH, bg = "lightgrey")
        self.ParemeterFrame.grid(row = 2, column = 1)
        self.ParemeterFrame.grid_propagate(False)
        
        # ButtonFrame
        self.ButtonFrame = tk.Frame(self.Control_Frame, 
            borderwidth = 1, relief = 'solid',
            height = self.CONTROL_FRAME_HEIGHT/3, width = self.CONTROL_FRAME_WIDTH, bg = "lightgrey")
        self.ButtonFrame.grid(row = 3, column = 1)
        self.ButtonFrame.grid_propagate(False)
        
        
    def FrameLabels_and_Parameters(self):
        
        '''Function creates all Frames, Labels, and Parameters in the window'''
        
        # Message Label
        self.Message_Label_var = tk.StringVar()
        self.Message_Label = tk.Message(self.MessageFrame, textvariable= self.Message_Label_var, 
                                        bg = 'lightgrey', fg = 'black',width = self.CONTROL_FRAME_WIDTH,)
        self.Message_Label.grid(row = 1,column = 1, padx = self.USER_SELECTION_PADDING)
        
        # centering Message Label
        self.MessageFrame.grid_rowconfigure(0, weight = 5)
        self.MessageFrame.grid_rowconfigure(1,weight = 0)
        self.MessageFrame.grid_rowconfigure(2, weight = 5)
        
        self.MessageFrame.grid_columnconfigure(0,weight = 5)
        self.MessageFrame.grid_columnconfigure(1,weight = 0)
        self.MessageFrame.grid_columnconfigure(2,weight = 5)
        
        # SpecifyWord Checkbox
        self.SpecifyWord_var = tk.BooleanVar()
        self.SpecifyWord_var.set(False)
        self.SpecifyWord_checkbox = tk.Checkbutton(self.ParemeterFrame, text="Specify word", 
                            var = self.SpecifyWord_var, bg = "lightgrey", fg = "black")
        self.SpecifyWord_checkbox.grid(row = 3, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)
        
        # Show Word Checkbox
        self.ShowWord_var = tk.BooleanVar()
        self.ShowWord_var.set(False)
        self.ShowWord_checkbox = tk.Checkbutton(self.ParemeterFrame, text="Show word", 
                            var = self.ShowWord_var, bg = 'lightgrey', fg = "black", command = self.Check_Show_Word_Status)
        self.ShowWord_checkbox.grid(row = 2, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)
        
        # Guesses are Words Checkbox
        self.Guesses_words_var = tk.BooleanVar()
        self.Guesses_words_var.set(True)
        
        self.Guesses_words_checkbox = tk.Checkbutton(self.ParemeterFrame, text="Guesses must be words", 
                            var = self.Guesses_words_var, bg = 'lightgrey', fg = "black")
        self.Guesses_words_checkbox.grid(row = 1, column = 1, sticky = tk.W, padx = self.USER_SELECTION_PADDING)
        
        # Create Hidden Word Label 
        self.Show_Hidden_Word_var = tk.StringVar()
        self.Show_Hidden_Word = tk.Label(self.ParemeterFrame, textvariable= self.Show_Hidden_Word_var, bg = 'lightgrey', fg = 'black')
        self.Show_Hidden_Word.grid(row = 2, column = 2)
        
        # Put an entry widget to the right
        self.entry_var = tk.StringVar()
        self.entry  = tk.Entry(self.ParemeterFrame, textvariable=self.entry_var, width = self.ENTRY_SIZE, bg = 'white', fg = 'black')
        self.entry.grid(row = 3, column=2, padx = self.USER_SELECTION_PADDING)

        # Center row 1 in the frame.
        self.ParemeterFrame.grid_rowconfigure(1, weight = 1)

        # Arrange spread out (columnwise) the checkbox and entry box.
        self.ParemeterFrame.grid_columnconfigure(0, weight = 1)
        self.ParemeterFrame.grid_columnconfigure(1, weight = 1)
        self.ParemeterFrame.grid_columnconfigure(2, weight = 1)
        self.ParemeterFrame.grid_columnconfigure(3, weight = 1)
        
        
        self.ParemeterFrame.grid_rowconfigure(0, weight = 5)
        self.ParemeterFrame.grid_rowconfigure(1, weight = 0)
        self.ParemeterFrame.grid_rowconfigure(2, weight = 0)
        self.ParemeterFrame.grid_rowconfigure(3, weight = 0)
        self.ParemeterFrame.grid_rowconfigure(4, weight = 5)
        
        # Put a button in the bottom frame
        self.Startbutton  = tk.Button(self.ButtonFrame, text = "Start Game", command = self.checklisthandler)
        self.Startbutton.grid(row = 1, column=1)
        
        self.Quitbutton  = tk.Button(self.ButtonFrame, text = "Quit", command = self.Quit_Button)
        self.Quitbutton.grid(row = 1, column=2)

        # Center the button in its frame
        self.ButtonFrame.grid_rowconfigure(1, weight = 1)
        
        self.ButtonFrame.grid_columnconfigure(0, weight = 5)
        self.ButtonFrame.grid_columnconfigure(1, weight = 1)
        self.ButtonFrame.grid_columnconfigure(2, weight = 1)
        self.ButtonFrame.grid_columnconfigure(3, weight = 5)
    
    def keyboard(self):
        
        '''This function creates the keyboard widget and centers the keyboard in our Keyboard Frame.
        Each button of the key gets its own handler that we store in our buttons dictionary to access later.'''
        
        self.FONT = font.Font(family=self.FONT_FAMILY)
       
        # Define text to go in the buttons
        self.buttons = {}
        
        # # Create frames for the button in each row to position correctly in the Keyboard Frame.
        
        self.Keyboard_Row_One_Frame = tk.Frame(self.KeyboardFrame, bg = "lightgrey")
        self.Keyboard_Row_One_Frame.grid(column=1, row = 1)
        
        self.Keyboard_Row_two_Frame = tk.Frame(self.KeyboardFrame, bg = 'lightgrey')
        self.Keyboard_Row_two_Frame.grid(column=1, row = 2)
        
        self.Keyboard_Row_three_Frame = tk.Frame(self.KeyboardFrame, bg = 'lightgrey')
        self.Keyboard_Row_three_Frame.grid(column=1, row = 3)
        
        # Create the buttons.
        for r in range(len(self.KEYBOARD_BUTTON_NAMES)):
            for c in range(len(self.KEYBOARD_BUTTON_NAMES[r])):

                # button gets its own hander.  
                # But each handler calls the same method
                # (button_handler), but with a parameter
                # that specifies which button was pressed.
                
                def handler(key = self.KEYBOARD_BUTTON_NAMES[r][c]):
                    self.Keyboard_Buttons(key)
                
                if self.KEYBOARD_BUTTON_NAMES[r][c] in self.Keyboard_Row_One_Button_Names:
                    
                    button = tk.Button(self.Keyboard_Row_One_Frame, width = self.KEYBOARD_BUTTON_WIDTH,
                            text = self.KEYBOARD_BUTTON_NAMES[r][c],
                            fg=self.KEYBOARD_BUTTON_TEXT_BEGIN, font=self.FONT,command = handler)
                    
                if self.KEYBOARD_BUTTON_NAMES[r][c] in self.Keyboard_Row_Two_Button_Names:
                    
                    button = tk.Button(self.Keyboard_Row_two_Frame, width = self.KEYBOARD_BUTTON_WIDTH,
                            text = self.KEYBOARD_BUTTON_NAMES[r][c],
                            fg=self.KEYBOARD_BUTTON_TEXT_BEGIN, font=self.FONT, command = handler)
                    
                if self.KEYBOARD_BUTTON_NAMES[r][c] in self.Keyboard_Row_Three_Button_Names:
                    if len(self.KEYBOARD_BUTTON_NAMES[r][c])> 1:
                        
                        button = tk.Button(self.Keyboard_Row_three_Frame,width = self.KEYBOARD_BUTTON_WIDTH_LONG,
                        text = self.KEYBOARD_BUTTON_NAMES[r][c],fg=self.KEYBOARD_BUTTON_TEXT_BEGIN,
                        font=self.FONT, command = handler)
                        
                    else:
                        button = tk.Button(self.Keyboard_Row_three_Frame, width = self.KEYBOARD_BUTTON_WIDTH,
                                           text = self.KEYBOARD_BUTTON_NAMES[r][c], fg=self.KEYBOARD_BUTTON_TEXT_BEGIN,
                                           font=self.FONT, command = handler)
                
                button.grid(row = r + 1, column = c + 1, padx = self.GUESS_FRAME_PADDING)
                
                # Put the button in a dictionary of buttons
                # where the key is the button text, and the
                # value is the button object.
                
                self.buttons[self.KEYBOARD_BUTTON_NAMES[r][c]] = button
                

        # Center the grid of buttons in the button frame
        
        self.KeyboardFrame.rowconfigure(0, weight = 1)
        self.KeyboardFrame.rowconfigure(len(self.KEYBOARD_BUTTON_NAMES) + 1, weight = 1)
        self.KeyboardFrame.columnconfigure(0, weight = 1)
        self.KeyboardFrame.columnconfigure(len(self.KEYBOARD_BUTTON_NAMES[0]) + 1, weight = 1)
    
    def GuessBoxes(self):
        
        ''' Creates widgets in the guess frame based off of how many guesses and word size of the hidden word'''
        
        self.FONT = font.Font(family=self.FONT_FAMILY,size= self.FONT_SIZE_GUESS)
        self.guesses = {}
        
        for r in range(self.NUM_GUESSES):
            for c in range(self.WORD_SIZE):
                
                self.guess_boxes = tk.Label(self.GuessFrame, width = self.GUESS_FRAME_WIDTH,
                                       height = self.GUESS_FRAME_HEIGHT,
                                       bg = self.GUESS_FRAME_BG_BEGIN, font = self.FONT, text = '', fg = 'black')
                self.guess_boxes.grid(row = r + 1, column = c + 1, padx = self.GUESS_FRAME_PADDING, pady = self.GUESS_FRAME_PADDING)
                self.guess_boxes.grid_propagate(False)
                
                self.guesses[f'{r}{c}'] = self.guess_boxes
        
        self.GuessFrame.rowconfigure(0, weight = 1)
        self.GuessFrame.rowconfigure(self.WORD_SIZE + 2, weight = 1)
        self.GuessFrame.columnconfigure(0, weight = 1)
        self.GuessFrame.columnconfigure(self.WORD_SIZE + 1, weight = 1)
    
        
        
    def checklisthandler(self):
        
        '''checklist handler function makes sure that when the specify word checklist is marked,
        a valid word is entered with the other parameters before starting the game. For invalid
        entry we set a message to the message frame and clear it after a set time using the after method.
        User can still fix the paremeter window while this happens.'''
        
        if self.state == State.WAITING_FOR_START:
            self.Hidden_Word = random.choice(self.short_wordlist)
            if self.SpecifyWord_var.get() == True: 
                        try:
                            if len(str(self.entry_var.get())) != self.WORD_SIZE:
                                raise BadEntry     # raises a exception if word doesn't match word size
                            if self.Guesses_words_var.get() == True and str(self.entry_var.get()) not in self.Long_wordlist:
                                raise BadEntry_ValidWord  # raises a exception if word isn't a actual word in the wordlist
                            
                            self.Hidden_Word = self.entry_var.get()       # set hidden word to specify entry
                            self.state = State.WORDY_STARTED
                            self.start_button_handler() # calls button handler to start game
                        except BadEntry:
                            self.Message_Label_var.set('Incorrect specified word length')
                            
                        except BadEntry_ValidWord:
                            self.Message_Label_var.set('specified word not a valid word')
                        
                        self.window.after(self.MESSAGE_DISPLAY_TIME_SECS_MS,lambda:self.Message_Label_var.set(""))
                        
            else:
                self.state = State.WORDY_STARTED
                self.start_button_handler()
                
    def start_button_handler(self):
        """
        Disables the checkbox and entry field.

        Prints out the state of the checkbox,
        and the contents of the entry field.
        """
        
        '''This function starts the game and disables the specify word checklist and quesses checkbox.
         Then displays the hidden word if the checkbox was marked.'''
        
        if self.state == State.WORDY_STARTED:
            
            
            self.Guesses_words_checkbox['state'] = 'disabled'
            self.SpecifyWord_checkbox['state'] = 'disabled'
            self.entry['state'] = 'disabled'
            
        
            if self.Guesses_words_var.get() == True and self.SpecifyWord_var.get() == False:
                self.Hidden_Word = random.choice(self.short_wordlist)    
           
            if self.ShowWord_var.get() == True:
                self.Show_Hidden_Word_var.set(self.Hidden_Word)
            
            self.state = State.WORDY_RUNNING
            print(f"Specify word Button status = {self.SpecifyWord_var.get()}")
            print(f"Show word = {self.ShowWord_var.get()}")
            print(f"Quesses must be words = {self.Guesses_words_var.get()}")
            print(f"Hidden word = {self.Hidden_Word}")
            
    def Keyboard_Buttons(self,text):
        if self.state == State.WORDY_RUNNING:
            try:
                if self.Guess_Column < self.WORD_SIZE and len(text) < 2:
                        self.guesses[f'{self.GuessRow}{self.Guess_Column}']['text'] = text
                        self.user_guess = self.user_guess + text
                        self.Guess_Column +=1
                else:
                    if text == "BACK" and self.Guess_Column>= 1:
                        self.Guess_Column -=1
                        self.guesses[f'{self.GuessRow}{self.Guess_Column}']['text'] = ""
                        self.user_guess = self.user_guess[0:-1]
                        
                        
                    elif text == 'ENTER':
                        self.Valid_Input()
            except Not_A_Word:
                self.Message_Label_var.set(f"{self.user_guess} is not in the word list")
            except Word_Not_Done:
                self.Message_Label_var.set("Word Not Finished")
                
            self.window.after(self.MESSAGE_DISPLAY_TIME_SECS_MS,lambda:self.Message_Label_var.set(""))
                    
    def Valid_Input(self):
        
        ''' Function first checks if guess entry is valid and if not displays message and lets the user try again.
        If the entry is valid we first check each character matching its positions and category of each character before changing the color of the frames.
        This allows us to correctly color code duplicates and understand how we are going to change the guess box colors apropriately. Then if the user 
        doesn't get the hidden word in 6 guesses the game is over and we print a message to the window and if they get the right message then our program displays
        a message saying they got the correct answer. Once they have run out of guesses or they get the right answer we do nothing to the window
        and change the state to State.WordyOver'''
        
        self.user_guess  = self.user_guess.lower()
        self.Hidden_Word = self.Hidden_Word.lower()
        
        if len(self.user_guess) != self.WORD_SIZE:
            raise Word_Not_Done
        if self.user_guess not in self.Long_wordlist and self.Guesses_words_var.get() == True:
            raise Not_A_Word
        
        else:
           
            hidden_word_lst = []
            for c in self.Hidden_Word:
                hidden_word_lst.append(c)
            
            correct_spot = []
            incorrect_spot = []
            duplicate = []
            not_in_word = []
            count = 0
            
            for i in range(self.WORD_SIZE):
                if self.user_guess[i] in self.Hidden_Word[i]:
                    correct_spot.append(i)
                    del hidden_word_lst[i - count]
                    count += 1
            
            
            for i in range(self.WORD_SIZE):
                if self.user_guess[i] in hidden_word_lst:
                    incorrect_spot.append(self.user_guess[i])
                    hidden_word_lst.remove(self.user_guess[i])
                    
                else:
                    if self.user_guess[i] in self.Hidden_Word:
                        duplicate.append(self.user_guess[i])
                       
                    else:
                        not_in_word.append(self.user_guess[i])
                
            
            for i in range(self.WORD_SIZE):
                self.window.update()
                time.sleep(self.PROCESS_GUESS_WAITTIME)
                #if self.user_guess[i] in self.Hidden_Word[i]:
                if i in correct_spot:
                    self.guesses[f'{self.GuessRow}{i}']['bg'] = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                    self.guesses[f'{self.GuessRow}{i}']['fg'] = self.GUESS_FRAME_TEXT_AFTER
                    self.buttons[self.user_guess[i].upper()]['fg'] = self.KEYBOARD_BUTTON_TEXT_CORRECT_RIGHT_LOC
                   
                    
                #elif self.user_guess[i] in self.Hidden_Word:
                elif self.user_guess[i] in incorrect_spot:
                    self.guesses[f'{self.GuessRow}{i}']['bg'] = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                    self.guesses[f'{self.GuessRow}{i}']['fg'] = self.GUESS_FRAME_TEXT_AFTER
                    self.buttons[self.user_guess[i].upper()]['fg'] = self.KEYBOARD_BUTTON_TEXT_CORRECT_WRONG_LOC
                    incorrect_spot.remove(self.user_guess[i])
                
                elif self.user_guess[i] in duplicate:
                    self.guesses[f'{self.GuessRow}{i}']['bg'] = self.GUESS_FRAME_BG_WRONG
                    self.guesses[f'{self.GuessRow}{i}']['fg'] = self.GUESS_FRAME_TEXT_AFTER
                else:
                    self.guesses[f'{self.GuessRow}{i}']['bg'] = self.GUESS_FRAME_BG_WRONG
                    self.guesses[f'{self.GuessRow}{i}']['fg'] = self.GUESS_FRAME_TEXT_AFTER
                    self.buttons[self.user_guess[i].upper()]['fg'] = self.KEYBOARD_BUTTON_TEXT_WRONG
                    self.buttons[self.user_guess[i].upper()]['state'] = 'disabled'
                
            
            if self.user_guess in self.Hidden_Word:
                self.state = State.Wordy_Over
                self.Message_Label_var.set("Correct. Nice Job. Game Over.")
                    
            self.GuessRow +=1
            
            if self.GuessRow > 5:
                if self.state == State.WORDY_RUNNING:
                    self.Message_Label_var.set(f"Guesses used up.\n Word was {self.Hidden_Word}.\n Game Over")
                    self.state = State.Wordy_Over
            self.user_guess = ''
            self.Guess_Column = 0
        
    
    def Check_Show_Word_Status(self):
        
        ''' Command so that user and ShowWord and unshow word while the game is running'''
        
        if self.state == State.WORDY_RUNNING or self.state == State.Wordy_Over:
            if self.ShowWord_var.get() == True:
                self.Show_Hidden_Word_var.set(self.Hidden_Word)
            if self.ShowWord_var.get() == False:
                self.Show_Hidden_Word_var.set('')
        
            
    def Quit_Button(self):
        ''' Quit Button command'''
        
        self.window.destroy()
        
        

class State:
    WAITING_FOR_START = 0
    WORDY_STARTED = 1
    WORDY_RUNNING = 2
    Wordy_Over = 3
if __name__ == "__main__":
   Wordy()