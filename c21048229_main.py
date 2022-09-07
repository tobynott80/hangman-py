#Hangman Game - Oct. 2021 - Student No. 21048229 - Cardiff University
#api used : https://github.com/mcnaveen/Random-Words-API - MIT License

import random   #required library - used for selecting random words - included in the standard python library
from os import system, name #required library - used for clearing terminal screen - included in the standard python library

try: #error testing to check whether all required files are correctly imported
    from c21048229_art import printArt #imports custom function from c21048229_art.py to print ascii art
    import c21048229_db as db #imports custom functions from c21048229_db.py to interact with the db.json file and update the scoreboard
except:
    print("Essential libraries not found, please ensure c21048229_art.py and c21048229_db.py exist")
    exit()

def clear():   #function to clear terminal - code adapted from https://stackoverflow.com/questions/54943464/how-to-clear-a-screen-in-python
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        _ = system('clear')
clear()

try:    #testing if requests library is installed, if not run in offline mode
    import requests #if this fails, the library is not installed and the except function is called and runs the program in offline mode
    print("Required libraries successfully installed")
    online = True
except: #The program can be ran without requests, see offline mode in getWord()
    print("'Requests' library not installed, running in offline mode. Offline mode uses locally stored words")
    print("To run in online mode, install requests with 'pip install requests'")
    online = False

if online == True: #important testing to see whether api is online
    try:
        print("Checking api is online")
        r = requests.get('https://random-words-api.vercel.app/word')
        if r.status_code == 200:    #status code 200=ok - testing if api is online, any other response that isn't 'ok' runs the program in offline mode
            print("Api Online!")
        else:  #any other code, or lack of a http return means api is offline or inaccessable, program must be run in offline mode
            print("API offline, running in offline mode")
            online = False
    except: #runs if requests runs into an error during sending http request
        print("API error, running in offline mode")
        online = False

def home(online):
    global ascii 
    print("Welcome to Hangman! \nThis program uses ASCII art to visualise the hangman's gallows, if you are using a small screen, the characters may not be correctly rendered")
    if input("Use ASCII art? (y/n default = yes) :").lower() == "n":
        ascii=False  #'ascii' gets passed through to the printArt() function to determine if the art is printed or not
    else:
        ascii=True
    initUser() #runs inituser to get user name and show how many games won or lost. If user doesn't exist, a new profile is created
    input("Continue?") #gives time for user to read the initUser() printouts.
    clear()
    word, definition = getWord(online) #getWord() returns two values, a random word and its definition
     #to avoid having too many parameters, its easier to store everything about the target word in a list
     #target = [target word, target definition, hidden target, guessedLetters, Found letters]
    target = [word, definition, hideWord(word), [], []]
    userGuess(5, target) #args: attemptsLeft(5 when calling fresh from home()) and the target word info 

def initUser(): #simple function implementing the db module to get the users name and show how many games they've won or lost. If user doesn't exist, a new profile is created
    global user
    usrName = str(input("Please enter your name  :"))
    if usrName == "":
        initUser()
    elif db.search(usrName) == False: #db.search returns true if the passed string is found as a user in db.json and returns false if not found
        print("Setting up a new account, since you are a new user")
        db.add(usrName,0,0) #creates a new user with the specified username with 0 wins and 0 losses
        user = [usrName,0,0] #sets the current user to the correct one
    else: #when the user is found
        result = db.search(usrName)
        user = [result["name"],result["wins"],result["losses"]] #sets the current user to the correct one
        print("Welcome back {}! You have {} wins and {} losses".format(user[0],user[1],user[2])) #informs the user of their stats

#simple functions to change score-board for when a user wins/looses a game      
def win():  
    user[1] += 1 #adds 1 to the wins variable
    db.update(user[0],user[1],user[2]) #updates the json file
    print("Updated Scoreboard")

def loss():
    user[2] += 1 #adds 1 to the losses variable
    db.update(user[0],user[1],user[2]) #updates the json file
    print("Updated Scoreboard")

#function to get the target word, if api is not available (online == False), a random word is selected from the backup dictionary
def getWord(online):
    if online == True: #api available and requests installed
        r = requests.get('https://random-words-api.vercel.app/word') #get request to api
        rJSON = r.json() #parse the json into a python dictionary
        rJSON = rJSON[0] #removes json whitespace
        word = (rJSON["word"]).lower() #all words are kept as lowercase to avoid errors with capitalisation
        definition = rJSON["definition"] #finds the word's definition
        return word, definition[:-2]    #api returns the definition with whitespace at the end, "[:-2]" removes it.
    else:   #handling for when running in offline mode - return a random word and definition from a preset dictionary
        wordList = {"Cardiff":"Capital City of Wales", 	"Karyology":"Study of cell nuclei", "Rede":	"To counsel or advise", "Ichthyonomy":"Classification of fishes"}
        word, definition = random.choice(list(wordList.items())) #uses random library to pick a random key-pair from dictionary
        return word.lower(), definition  #all words are kept as lowercase to avoid errors with capitalisation

#function to create a simple list that represents the hidden target word to show how many characters it has
def hideWord(word): 
    word = word.lower()     #setting the word to lowercase to avoid input and comparison errors
    hidden = [] #initalise list 
    for letter in word: #this for loop creates a list that hides the letters of the target word behind '-' characters.
        #this allows the rare case of punctuation such as hyphens and spaces to still be visable to the user
        if letter != " " or "-": #when the letter is a normal character
            hidden.append("_")
        else:
            hidden.append(letter)
    return hidden #returns the list of hidden letters
    
#function for user to enter their guess or select a menu item
def userGuess(attemptsLeft,target):
    word, definition, hidden = target[0:3] #word, definition and hidden are not modified within this function, so they can be assigned local variables
    print(" ".join(hidden)) #prints the hidden word in a user-friendly way
    printArt(attemptsLeft,ascii) #prints the hangman's gallows
    print("Enter Guess (Optionally enter '1' for a hint, '2' to quit, '3' to get a new word) and '4' to get your score")
    
    if (len(target[3])) > 0: #if the user has already guessed, list the letters they have already guessed
        print("So far you have guessed {}".format(target[3]))
    
    userInput = input(" :").lower()
    
    if len(userInput) == 0: #if the user enters nothing
        clear()
        userGuess(attemptsLeft,target)
    elif len(userInput) > 1:   #if the user is guessing a full word
        wordGuess(attemptsLeft,target,userInput)
    elif len(userInput) == 1:   #if the user is just guessing one letter
        if userInput == "1":
            clear()
            print("The definition is '{}' \n".format(definition))
            userGuess(attemptsLeft,target)
        elif userInput == "2":
            print("The word was {} \n".format(word))
            exit()
        elif userInput == "3":
            print("Getting a new word")
            home(online)
        elif userInput == "4":
            global user
            print("You have {} wins and {} losses".format(user[0],user[1]))
            userGuess(attemptsLeft,target)
        else:
            if (userInput in target[3]):
                clear()
                print("You have already guessed '{}', guess again".format(userInput))
                userGuess(attemptsLeft,target)
            else:
                letterGuess(attemptsLeft,target,userInput)

#function to check to see if the user has entered a letter thats in the target word
def letterGuess(attemptsLeft,target,userInput):
    word = target[0]
    target[3].append(userInput)
    i = 0
    correctLetter = False
    for letter in word:
        if userInput == letter:     #if the user has entered a correct letter...
            correctLetter = True    #...mark the guess as correct
            target[4].append(letter)  #...add the letter to foundLetters
            target[2][i] = letter  #...change the '_' placeholder to the correct letter in the "hidden" variable
        i += 1
    
    if ("_" in target[2]) and (correctLetter == False) and (attemptsLeft > 0): #if the word isn't done and the user didn't get the right letter
        clear()
        print("Wrong Letter :( Keep Guessing!")
        attemptsLeft -= 1
        if (attemptsLeft == 0): #handling when the user has no attempts left
            printArt(attemptsLeft,ascii)
            print("You have run out of attempts")
            print("The word was {} and it means '{}'".format(word,target[1]))
            loss()
            tryAgain()
        print("You have {} attempts left".format(attemptsLeft))
        userGuess(attemptsLeft,target)
    elif ("_" in target[2]) and (correctLetter == True):
        clear()
        userGuess(attemptsLeft,target)
    elif ("_" not in target[2]):
        print("Congrats! You correctly guessed the word! It was {} and it means '{}'".format(word,target[1]))
        win()
        tryAgain()
    else:        
        tryAgain()

def wordGuess(attemptsLeft,target,userInput):
    word = target[0]
    if attemptsLeft == 0:
        print("You have run out of attempts")
        print("The word was {} and it means '{}'".format(word,target[1]))
        loss()
        tryAgain()
    elif userInput.lower() == word.lower():
        clear()
        print("Congrats! You correctly guessed the word! It was {} and it means '{}'".format(word,target[1]))
        win()
        tryAgain()
    else:
        clear()
        print("{} is not the correct word".format(userInput))
        userGuess((attemptsLeft-1),target)

def tryAgain(): 
    if input("Try again ?(y/n) :") == "y":
        clear()
        home(online)
    else:
        exit()


if online == True:
    import json  #json library not needed when running in offline mode- used to parse data from api
    home(True) #need to add on/offline param
else:
    home(False) #need to add on/offline param