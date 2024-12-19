from random import randint

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
        ind = ord(ltr)-65
        self.ltrList[2*ind] = "_"
        if ltr in self.theWord:
            for i in range(len(self.theWord)):
                if ltr == self.theWord[i]:
                    self.wordState[2*i] = ltr
        else:
            self.wrongGuesses += 1
        if self.wrongGuesses == self.maxGuesses:
            self.endState = "Lost"
        if not ("_" in self.wordState):
            self.endState = "Won"

    def convertLtrList(self):
        outStr = ""
        for i in self.ltrList:
            outStr += i
        return outStr
    
    def convertState(self):
        outStr = ""
        for i in self.wordState:
            outStr += i
        return outStr

def GetWordList():
    wordList = ['APPLE', 'PEAR', 'BANANA', 'ORANGE', 'PEACH', 'GRAPE', 'KIWI', 'STRAWBERRY', 'RASBERRY', 'BLUEBERRY']
    return wordList

def DisplayGame(sWord):
    # Display Gallows
    dispList = ["   ---- ", "   |  | ", "   |    ", "   |    ", "   |    ", "   |    ", "-------"]
    if sWord.wrongGuesses > 0:
        dispList[2] = "   |  O"
    if sWord.wrongGuesses == 2:
        dispList[3] = "   |  | "
    if sWord.wrongGuesses == 3:
        dispList[3] = "   | \|  "
    if sWord.wrongGuesses > 3:
        dispList[3] = "   | \|/"
    if sWord.wrongGuesses > 4:
        dispList[4] = "   |  | "
    if sWord.wrongGuesses == 6:
        dispList[5] = "   | /  "
    if sWord.wrongGuesses == 7:
        dispList[5] = "   | / \ "
    for i in range(7):
        print(dispList[i])
    print()

    # Display Letter List
    print(sWord.convertLtrList())
    print()

    # Display State of Secret Word
    print(sWord.convertState())
    print()

def makeGuess(sWord):
    ltr = input("Guess a letter: ")
    badLetter = True
    while badLetter:
        if not (((ord(ltr) >= 65) and (ord(ltr) <= 90)) or ((ord(ltr) >= 97) and (ord(ltr) <= 122))):
            print("You did not enter a letter!  Please enter a letter!")
        else:
            LTR = ltr.capitalize()
            if (LTR in sWord.ltrList):
                badLetter = False
                break
            else:
                print("You've already used that letter!  Try again!!")
        ltr = input("Guess a letter: ")
    return LTR

def ChooseWord(wordList):
    randNum = randint(0,len(wordList))
    sWord = wordList[randNum]
    return wordList[randNum]

def OneRound(sWord):
   # Ask User to guess a letter 
    ltr = makeGuess(sWord)

    sWord.updateState(ltr)

def ContinueGame(sWord):
    return sWord.endState == "Playing"

def endGame(sWord):
    DisplayGame(sWord)
    if sWord.endState == "Won":
        print("Congratulations!  You beat the hangman!")
    else:
        print("So sorry!  You have run out of chances!")
    print()
    

# MAIN PROGRAM
# Define global variables

# Read Word List
wordList = GetWordList()

secretWord = hWord(ChooseWord(wordList))

while ContinueGame(secretWord):
    DisplayGame(secretWord)
    OneRound(secretWord)

endGame(secretWord)