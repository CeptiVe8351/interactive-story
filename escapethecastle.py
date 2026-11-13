
# ==========================================
# CHARACTER INTRODUCTION
# ==========================================

def introduction():

    # Welcome the player
    print("=== ESCAPE THE CASTLE ===")
    print("Welcome, adventurer! You find yourself trapped in a mysterious castle. Your goal is to escape by making the right choices. Good luck!")

    # Get player name, age and character class
    global playerName

    playerName = input("What is your name, adventurer? ")
    characterClass = input("Choose your character class (Warrior, Mage, Rogue): ")
    characterAge = int(input("How old are you, adventurer? "))

    # Set starting values
    health = 100
    gold = 20

    # Display the character profile
    print("\n=== CHARACTER PROFILE ===")
    print(f"Name: {playerName}")
    print(f"Age: {characterAge}")
    print(f"Class: {characterClass}")
    print(f"Health: {health}")
    print(f"Gold: {gold}")

    # Begin the story
    print(f"\n{playerName}, you wake up in a dimly lit room.")
    print("Your adventure begins now. What will you do?")


# Start the introduction
introduction()


# ==========================================
# ESCAPE THE CASTLE - SCENE 1: THE CELL
# ==========================================
 
# Create an inventory to store collected items

inventory = []

# Define the Cell scene
def cell():
    global has_key
    print("\nYou wake up in a dark castle cell.")
    print("You can see a door, a window and an old bed.")

    # Track whether the player has found the key
    has_key = False
    escaped = False

    # Repeat while the player has not escaped
    while escaped == False:

        # Ask the player what to investigate
        choice = input("\nInvestigate the door, window or bed? ").lower()

        if choice == "door":
            print("The door is locked.")
            print("You need to find a key")

        elif choice == "window":
            print("You look through the window and see a beautiful garden outside. But it's too high to jump.")
            print("The window is too small to climb through.")

        elif choice == "bed":
            print("You look underneath the bed.")
            print("You find a small Iron Key")

            # Add the key to the inventory
            inventory.append("Iron Key")
            has_key = True
            escaped = True

        else:
            print("Invalid choice. Please choose 'door', 'window', or 'bed'.")

    # Code runs once the player has found the key
    if escaped:
        print("\nYou unlock the cell door.")
        print("You step out into the corridor.")
        inventory.remove("Iron Key")
        print(f"Your inventory: {inventory}")


# Start the scene
cell()

# # ==========================================
# # ESCAPE THE CASTLE - SCENE 2: THE CORRIDOR
# # ==========================================

# Create a list to store the player's inventory
# We are assuming the player already found the Iron Key
inventory = []

# Introduce the scene
print("You enter a long, dark corridor.")
print("You notice an old wooden door with a strange symbol on it.")

choice = input("Do you want to try to open the door? yes/no: ").lower()

if choice == "yes":
    print("You try to open the door.")
    print("Inside, you find a rusty sword and a small pouch of gold coins.")
    print("You open the pouch and find 20 gold coins inside.")

    inventory.append("Rusty Sword")
    inventory.append("20 Gold Coins")

    print("You pick up the rusty sword and the pouch of gold coins.")

elif choice == "no":
    print("You decide to leave the door alone and continue down the corridor.")

print(f"\n Your inventory: {inventory}")



# ==========================================
# ESCAPE THE CASTLE - SCENE 3: THE ROOM
# ==========================================

import random

def creature_encounter():
    print("You hear a strange noise in the corridor...")

    creatures = ["Guard", "Ghost", "Draugr"]
    random_creature = random.choice(creatures)

    encounter(random_creature)


def encounter(creature):

    if creature == "Guard":
        print("The guard draws their sword!")

    elif creature == "Ghost":
        print("A ghost floats towards your location!")

    elif creature == "Draugr":
        print("The draugr wakes up and slowly walks towards you!")

    print(f"\nA {creature} appears!!!")

    choice = input("\nDo you want to fight or hide? ").lower()

    if choice == "fight":
        print(f"\nYou decide to fight the {creature}!")

        if creature == "Guard":
            print("You raise your sword and defeat the guard!")

        elif creature == "Ghost":
            print("You use your sword to weaken the ghost until it disappears!")

        elif creature == "Draugr":
            print("You strike the draugr with your sword and defeat it!")

        print("You have successfully defeated the creature!")
        print("You continue towards the library.")

    elif choice == "hide":
        print("\nYou quickly hide behind an old suit of armour.")
        print(f"The {creature} searches the corridor but cannot find you.")
        print("Eventually, the creature wanders away.")
        print("You quietly leave your hiding place and continue towards the library.")

    else:
        print("Invalid choice. Please choose fight or hide.")
        encounter(creature)


def corridor():

    print("\nYou walk down a dark castle corridor.")
    print("You hear a strange noise ahead...")

    creatures = ["Guard", "Ghost", "Draugr"]

    random_creature = random.choice(creatures)

    encounter(random_creature)


# Start the scene
corridor()

# # ==========================================
# # ESCAPE THE CASTLE - LIBRARY SCENE
# # ==========================================

def library():

    print("\nYou enter an old, duty library that looks like it hasn't been touched for centuries.")
    print("Books are neatly placed within the bookshelves, apart from one that catches your eye.")
    print("There's a book with a faint glow lay down on a table.")
    print("There may be a clue inside.")

    found_clue = False
    bookshelf_open = False

    while found_clue == False or bookshelf_open == False:

        choice = input("\nDo you investigate the glowing book, fireplace, or the bookshelf? ").lower()

        if choice == "glowing book":
            print("\nYou open the glowing book and start to read.")
            print("You see some of the history of the castle.")
            print("On the last page you find a clue")
            print("'I follow you wherever you go, but I disappear when there is no light.'")
            print("You discover that the password is SHADOW.")
            found_clue = True

        elif choice == "fireplace":
            print("\nYou have a closer look at the fireplace.")
            print("There are only ashes and burnt pieces of paper.")

        elif choice == "bookshelf":
            print("\nYou pull out a duty book from the bookshelf.")
            print("Suddenly, you hear a loud grinding noise, and the bookself begins to move!")
            print("A secret passage appears behind the bookshelf, seemingly the way forward.")

            bookshelf_open = True

        else:
            print("Invalid choice. Please choose again.")

    if found_clue == True:
        print("\nYou memorise the password before going down the secret passage")

    print("\nYou walk down the hidden passage leading towards the castle gate")

library()

# ==========================================
# ESCAPE THE CASTLE - SCENE 5: CASTLE GATE
# ==========================================

def castle_gate():

    print("\nYou reach the gates of the dark castle.")
    print("You look and notice a strange keypad on the gate.")
    print("you approach the keypad.")
    print("A message reads: 'Enter the password to escape.'")

    password = ""

    while password != "SHADOW":

        password = input("\nEnter the password: ").lower()

        if password == "SHADOW":
            print("\nThe keypad glows brightly!")
            print("You hear a loud click as the gates unlock.")
            print("The quickly run past the gates before they completely open.")
            print("\nYou have escaped the castle!")
            print("Congratulations, adventurer!")
            print(f"Well done, {playerName}!")

        else:
            print("Incorrect password!")
            print("Think carefully about the clue you found in the library.")


castle_gate()


# ==========================================
# MAIN GAME
# ==========================================

def play_game():

    introduction()

    cell()

    corridor()

    creature_encounter()

    library()

    castle_gate()


# Start the game
play_game()
