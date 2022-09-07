#Hangman scoreboard functions - Oct 2021 - Student No. 21048229 - Cardiff University
#Code Partially Referenced from 2nd Hackathon Project(https://git.cardiff.ac.uk/c21048229/hackathon2)

import os
import json
#code adapted from https://stackoverflow.com/questions/51520/how-to-get-an-absolute-file-path-in-python
file = os.path.abspath("db.json") #this line ensures that the correct file path is specified, no matter where the user installs the program
#reference end

data = []

def load(): #function to initially load the json file
    global data 
    try: #error handling if file cannot be read
        with open(file, "r", encoding="utf8") as i: #opens db.json in read mode with correct formatting
            data = json.load(i) #json is then parsed into python-friendly format
            return data #data gets returned
    except:
        print("Error loading file")
        return "error"


def search(name):
    result = []
    for user in data: #search through each user in json file
        if name.lower() == user["name"].lower(): #if name matches search term:
            result = user
    if result == []:
        return False #if there was no user found with specified name, return false
    else:
        return result #returns found user data

def save():
    try:
        with open(file, "w", encoding="utf8") as i: #file must be opened in 'w' (write) mode to write to file
            json.dump(data, i, indent=2) #converts data to json format with indentation of 2 spaces
    except:
        print("Could not save db.json")

def add(name,wins,losses): #function to add new user
    newData = { 
        "name":name,
        "wins":wins,
        "losses":losses
    }
    data.append(newData) #appends new data to the end of local data structure
    save()  #updates json file with local data structure

def update(name,wins,losses): #modifying exisiting user
    for user in data:
        if name.lower() == user["name"].lower(): #finds correct user based off name
            user["wins"] = wins #update wins with new values
            user["losses"] = losses #update losses with new values
            save() #updates json file with local data structur
            return "updated"


load()  #this gets run when the module is imported
