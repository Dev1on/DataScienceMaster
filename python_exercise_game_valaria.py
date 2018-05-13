import os

from random import randint
from time import sleep

"""
Python Excercise - 13.05.2018
1. Set up your IDE
2. Write a tiny game or everything else in Python to get fluent in Python.

Game: Kind of console RPG Game.

Concepts used:
- string formatting in print function
- random numbers
- if / else
- while
- inheritance
- console input
- constants
- dictionaries
- multi-line / single line comments
- sleep

@author Kevin Respondek Mat.Nr: 287056 - Fachhochschule Lübeck
"""
LINE_FEED = "===================================================================="

# class that is inherited by classes Player and Enemy
class Character:

    # initalize all values on init
    def __init__(self, name, health, exp, level, strength, target):
        self.name = name
        self.health = health
        self.exp = exp
        self.level = level
        self.strength = strength
        self.target = target

    # attack function
    def attack(self):
        # calculate damage based on strenght and level
        damage = self.strength + self.level
        self.target.health -= damage

        # formatted attack message
        print("%s attacked %s. %s lost %i health points!"%(self.name, self.target.name,self.target.name,damage))
        print(LINE_FEED)

        # if target has no health left -> die and update quest progress
        if self.target.health <= 0:
            self.die()

            if type(self.target) is Enemy:
                self.add_exp(4)
                self.check_level()

                self.enemies_defeated += 1
                print("Quest Goal: %i/%i monster defeated!"%(self.enemies_defeated, 5))
                if self.enemies_defeated == 5:
                    self.questSolved = True

            self.target = None

    def die(self):
        print("%s lost all health points and died!"%self.target.name)
        self.inFight = False

# representing enemies of various type - for simplicity only the name is changing based on pre-defined dictionary entries
class Enemy(Character):
    ENEMY_HEALTH = 12
    ENEMY_LEVEL = 1
    ENEMY_STRENGTH = randint(1, 5)
    ENEMIES = [
        "Mountain Troll",
        "Bone Crusher Orc",
        "Wind Wolve",
        "Fire Mage"
    ]

    # calls super init of Character class - chooses name fist based on randomized int
    def __init__(self, target):
        self.enemy_name = self.ENEMIES[randint(0,3)]
        super().__init__(self.enemy_name,self.ENEMY_HEALTH,None,self.ENEMY_LEVEL,self.ENEMY_STRENGTH,target)

# representing the player
class Player(Character):
    PLAYER_MAX_HEALTH = 20
    PLAYER_LEVEL = 1
    PLAYER_EXP = 0
    PLAYER_STRENGTH = 5
    PLAYER_ENEMIES_DEFEATED = 0

    # calls super init of Charactr class - also asks player for name input
    def __init__(self):
        super().__init__(input("Sir, would you please be so kind to tell me your name? "),self.PLAYER_MAX_HEALTH,self.PLAYER_EXP,self.PLAYER_LEVEL,self.PLAYER_STRENGTH,None)
        self.exp_to_next_level = self.PLAYER_LEVEL * 8
        self.enemies_defeated = self.PLAYER_ENEMIES_DEFEATED
        self.questSolved = False
        self.hasQuit = False
        self.inFight = False

    ## options that the player can call in console

    # print help - show options that player can call
    def help(self):
        print("You need some help? Hum... Okay let's see what you can do:")
        for option in OPTIONS.keys():
            print(option)

    # print current health status
    def health_status(self):
        print("Your health is at: %d/%d!"%(self.health, self.PLAYER_MAX_HEALTH))

    # player can rest and current health points are regenerated
    def recover(self):
        print("You are tired? Hum... Okay let's rest for a while!")
        sleep(1.4)
        print("...")
        if self.health < self.PLAYER_MAX_HEALTH:
            self.health += randint(1, 4)
        if self.health > self.PLAYER_MAX_HEALTH:
            self.health = self.PLAYER_MAX_HEALTH
        print("You've rested enough! We need to come back to our quest!")
        print("...")
        self.health_status()

    # explore the world - randomly an enemy is spawned and attacks the player
    def explore(self):
        print("You've entered a mystical region! Be alerted! You never know what is behind the next corner!")
        sleep(2)
        print("...")
        sleep(2)
        print("<clicking noise>")
        sleep(1)
        if(randint(0, 1)):
            self.enemy = Enemy(self)
            self.set_target(self.enemy)
            print("Sir, Caution! A %s appeared!"%self.enemy.name)
            self.inFight = True

            if(randint(0, 1)):
                self.enemy.attack()
        else:
            print("Hum nothing... We should go on!")

    # setter for target
    def set_target(self, enemy):
        self.target = enemy

    # if player quits the game
    def quit(self):
        self.hasQuit = True
        print("Okay Sir, see you again in a few moments!")

    # add exp after enemy defeated
    def add_exp(self, exp):
        self.exp += exp
        print("You've gained %i experience points!"%exp)

    # check current level - if exp are high enought player gets level up
    def check_level(self):
        if self.exp >= self.exp_to_next_level:
            self.level += 1
            self.strength += 2
            self.exp_to_next_level = self.level * 5
            self.exp = self.exp - self.exp_to_next_level
            print("You leveled up! Congrats! You are level %i now and your strength is %i"%(self.level,self.strength))
            print(LINE_FEED)

# main game
class ValariaGame():

    # initializes the whole game and creates a new player
    def __init__(self):
        self.initConsole()
        self.player = Player()
        self.start_game()

    # pretty printing of story and logo
    def initConsole(self):
        os.system('clear')
        print("==================================")
        print("__      __   _            _       ")
        print("\ \    / /  | |          (_)      ")
        print(" \ \  / /_ _| | __ _ _ __ _  __ _ ")
        print("  \ \/ / _` | |/ _` | '__| |/ _` |")
        print("   \  / (_| | | (_| | |  | | (_| |")
        print("    \/ \__,_|_|\__,_|_|  |_|\__,_|")
        print("==================================")

    # starts the overall game and contains the input logic
    def start_game(self):
        print(LINE_FEED)
        print("If I may help you Sir... Type 'help' to ge a list of actions you can do!")
        sleep(0.2)
        print("...")
        sleep(0.2)
        print("There are rumours about dark forces in the surroundings of our kingdom!")
        sleep(0.5)
        print("The king asked every brave man to move out and find 5 those creatures and defeat them!")
        sleep(0.5)
        print("...")

        self.questAccepted = False

        # ask for accepting the quest
        while(not self.questAccepted and not self.player.hasQuit):
            inputOption = input("Will you accept this quest of honorable motivation to protect our kingdom? ('y' / 'n'): ")
            # if invalid input - ask again
            if not (inputOption == 'y' or inputOption == 'n'):
                print("It seems like you've misunderstood... will you accept? ('y' / 'n'): ")
            else:
                # if quest not accepted quit game
                if inputOption == 'n':
                    print("Oh - well then! Go home and hope that other men are brave enough to save you!")
                    self.player.hasQuit = True
                # if quest accepted start game
                else:
                    self.questAccepted = True
                    print("Well then! Let's begin our jorney!")
                    print("...")
                    print(LINE_FEED)
                    print("You are entering a dark forest! What will we do next!")

        # as long as player has health, didn't quit the game or has solved the quest - continue to ask for next move
        while(self.player.health >= 0 and not self.player.hasQuit and not self.player.questSolved):
            if self.player.inFight:
                print("Sir... we need to fight ... %s is attacking... Be careful!"%self.player.target.name)
                if(randint(0, 1)):
                    self.player.target.attack()

            if self.player.health <= 0:
                break

            if self.player.health <= self.player.PLAYER_MAX_HEALTH / 2:
                print("Sir, your health is getting low... You just have %i health points left - if I may suggest to recover yourself a bit..."%self.player.health)

            inputOption = input("What will we do next?: ")
            args = inputOption.split()
            if len(args) > 0:
                validOption = False
                # choose from dictionary options
                for option in OPTIONS.keys():
                    if self.player.inFight and args[0] == "explore":
                        print("I am sorry, but we have to defeat %s!"%self.player.target.name)
                        sleep(0.3)
                        validOption = True
                        break
                    if not self.player.inFight and args[0] == "attack":
                        print("We have no target Sir...")
                        sleep(0.2)
                        validOption = True
                        break
                    if args[0] == option[:len(args[0])]:
                        OPTIONS[option](self.player)
                        validOption = True
                        break
                print(LINE_FEED)
                if not validOption:
                    print("Sir, it seems like you want to do something I dont understand... Hum...")
                    sleep(0.5)
                    print("What do you mean by %s? If you need help - remember to type 'help'."%args)
                    print("We really should do something! What shall we do Sir?")
                    print(LINE_FEED)

        # player solved quest successfully
        if self.player.questSolved:
            print("Congratulations Sir! I knew it right from the beginning that you are an honorable and brave man!")
            sleep(0.2)
            print("You successfully completed your quest!")
            print("...")
            sleep(0.2)
            print("The people in our kingdom can now sleep in peace for the next time!")

        # player lost all his health and died
        if self.player.health <= 0:
            print("Oh no! Sir... That ended up bad!")
            print("...")
            print("Rest in peace!")
OPTIONS = {
    'help': Player.help,
    'health': Player.health_status,
    'recover': Player.recover,
    'explore': Player.explore,
    'attack': Player.attack,
    'quit': Player.quit
}

game = ValariaGame()
