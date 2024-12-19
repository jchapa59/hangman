from random import randint
import os
import pyglet
from pyglet.window import key

# Set global variables
global windowWd, windowHt, imWd, imHt, offset, restart
windowWd, windowHt, imWd, restart = 998, 625, 330, True

# Create Game Window
window = pyglet.window.Window(width = windowWd, height = windowHt, caption = "Hangman Game")
global batch
batch = pyglet.graphics.Batch()

# Load Gallows images - resize graphics to 330 pixels
working_dir = os.getcwd()
pyglet.resource.path = [working_dir]
pyglet.resource.reindex()

hmIm = list(range(8))

for i in range(8):
    fname = 'hangman/pics/hm' + str(i) + '.png'
    hmIm[i] = pyglet.image.load(fname)
    
# Load letter images
ltrIm = list(range(27))
for i in range(27):
    fname = 'hangman/pics/ltr' + str(i) + '.jpg'
    ltrIm[i] = pyglet.image.load(fname)

# Create button class
class btn:
    def __init__(self, simpleName):
        fname = 'hangman/pics/' + simpleName
        self.btnIm = pyglet.image.load(fname)
        self.btnWd = self.btnIm.width
        self.btnHt = self.btnIm.height
        self.bBounds = [-2, -1, -2, -1]

    def dispBtn(self, x,y):
        self.btnIm.blit(x,y)
        self.bBounds = [x, x + self.btnWd, y, y + self.btnHt]

# Create hangman word class
class hWord:
    def __init__(self, chosenWord):
        self.theWord = chosenWord
        self.wordState = []
        self.ltrList = list('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z')
        self.endState = "Playing"
        self.wrongGuesses = 0
        self.maxGuesses = 7
        for i in self.theWord:
            self.wordState.append("_")
            self.wordState.append(" ")

    def updateState(self, ltr):
        # Update the state of the secret word based on correct letter guess
        ind = ord(ltr)-97
        self.ltrList[2*ind] = "_"
        if ltr in self.theWord:
            for i in range(len(self.theWord)):
                if ltr == self.theWord[i]:
                    self.wordState[2*i] = chr(ord(ltr)-32)
        else:
            self.wrongGuesses += 1
        if self.wrongGuesses == self.maxGuesses:
            self.endState = "Lost"
        if not ("_" in self.wordState):
            self.endState = "Won"

    def convertLtrList(self):
        # Convert a list of letters to a string of letters
        outStr = ""
        for i in self.ltrList:
            outStr += i
        return outStr
    
    def convertState(self):
        # Convert the state of the guessed word from a list of characters to a string
        outStr = ""
        for i in self.wordState:
            outStr += i
        return outStr

def GetWordList():
    # Load the full list of possible secret hangman words
    fname = 'hangman/words.txt'
    f = open(fname, "r")
    wordList = f.read().splitlines()
    for i in range(len(wordList)):
        wordList[i] = wordList[i]
    f.close
    return wordList

def ChooseWord(wordList):
    # Choose a random word from the loaded word list
    randNum = randint(0,len(wordList)-1)
    return wordList[randNum]

def ContinueGame(sWord):
    # Returns True if the game is still playing.  Word has not yet been guessed & user has not won
    return sWord.endState == "Playing"

def endGame(sWord):
    # Display the appropriate text when game is over.  Either they won or they lost.
    endText = list("AB")
    if sWord.endState == "Won":
        endText[0] = "Congratulations!"
        endText[1] = "You beat the hangman!"
    else:
        endText[0] = "So sorry!"
        endText[1] = "You have run out of chances!"
    return endText

@window.event
def on_mouse_press(x, y, button, modifiers):
    global startx
    global starty
    global restart
    startx = x
    starty = y
    gap = 50
    # Create boolean:  True if mouse click in first row of letters, False is not
    firstRow = (starty > 0.16 * window.height) and (starty < 0.16 * window.height + ltrIm[1].height)
    # Create boolean:  True if mouse click in second row of letters, False is not
    secondRow = (starty > 0.04 * window.height) and (starty < 0.04 * window.height + ltrIm[1].height)
    # Find the column (1 - 13) that the mouse clicked.  Col = 0 if no letter was clicked
    num = (x - offset)//int(1.5 * ltrIm[1].width) + 1
    rmn = (x - offset) % int(1.5 * ltrIm[1].width)
    if (rmn < ltrIm[1].width) and (num > 0 and num <= 13):
        col = num
    else:
        col = 0
    # Generate the capital letter that was clicked
    ltr = "@"
    if (col > 0) and (col <=13):
        if firstRow:
            ltr = chr(96 + col)
        elif secondRow:
            ltr = chr(109 + col)
    if ltr != "@":
        secretWord.updateState(ltr)

    # Check to see if "Play Again!" button was clicked
    if (x > playBtn.bBounds[0]) and (x < playBtn.bBounds[1]) and ( y > playBtn.bBounds[2]) and (y < playBtn.bBounds[3]):
        restart = True
        pyglet.app.exit()
    # Check to see if "Quit" button was clicked    
    if (x > quitBtn.bBounds[0]) and (x < quitBtn.bBounds[1]) and ( y > quitBtn.bBounds[2]) and (y < quitBtn.bBounds[3]):
        restart = False
        pyglet.app.exit()

@window.event
def on_draw():
    window.clear()

    # Display white background
    bg = pyglet.shapes.Rectangle(0,0,windowWd, windowHt, color=(255,255,255), batch=batch)
    batch.draw()

    # Display appropriate gallow image
    hmIm[secretWord.wrongGuesses].blit((windowWd//2-imWd)//2, 0.42 * windowHt)

    # Display letters in two rows.  If the letter was already chosen, don't display it
    for i in range(13):
        if secretWord.ltrList[2*i] != "_":
           ltrIm[i].blit(offset + i * int(1.5 * ltrIm[1].width), 0.16*window.height)
    for i in range(13, 26):
        if secretWord.ltrList[2*i] != "_":
            ltrIm[i].blit(offset + (i-13) * int(1.5 * ltrIm[1].width), 0.04*window.height)

    # Display guessed word
    wordDisplay = pyglet.text.Label(secretWord.convertState(), font_name = 'Times New Roman', font_size = 30, 
        x=window.width//2, y=window.height * 0.35, anchor_x='center', anchor_y='center', color=(0,0,0,255))
    wordDisplay.draw()

    # Check to see if Game Completed.  Display appropriate text
    if not ContinueGame(secretWord):
        endText = endGame(secretWord)
        for i in range(2):
            endTextDisplay = pyglet.text.Label(endText[i], font_name = 'Times New Roman', font_size = 22, 
                x=0.70*window.width, y=window.height * 0.75 - 33 * i, anchor_x='center', anchor_y='center', color=(0,0,0,255))
            endTextDisplay.draw()
            gap = 50
        # Display "Play Again!" and "Quit!" buttons
        playBtn.dispBtn(0.7 * window.width-gap//2-playBtn.btnWd, 0.50 * window.height)
        quitBtn.dispBtn(0.7 * window.width+gap//2, 0.50 * window.height)


# MAIN PROGRAM
# Read Word List
offset = (window.width - 19 * ltrIm[1].width)//2
wordList = GetWordList()
playBtn = btn('playIm.png')
quitBtn = btn('quitIm.png')


while restart:
    secretWord = hWord(ChooseWord(wordList))
    pyglet.app.run()
    del secretWord
window.close()
