#Welcome the player
print("=== ESCAPE THE CASTLE ===")
print("Welcome, adventurer! You find yourself trapped in a mysterious castle. Your goal is to escape by making the right choices. Good luck!")
 
#Get player name, age and character class
playerName = input("What is your name, adventurer? ")
characterClass = input("Choose your character class (Warrior, Mage, Rogue): ")
characterAge = int(input("How old are you, adventurer? "))

#Set starting values
health = 100
gold = 20
hasKey = False
 
#Display the character profile
print(f"\n=== CHARACTER PROFILE ===")
print(f"Name: {playerName}")
print(f"Age: {characterAge}")
print(f"Class: {characterClass}")
print(f"Health: {health}")
print(f"Gold: {gold}")
print(f"Has Key: {hasKey}")
 
#Begin the story
print(f"\n{playerName}, you wake up in a dimly lit room.")
print("Your adventure begins now. What will you do?")

# ==========================================
# ESCAPE THE CASTLE - SCENE 1: THE CELL
# ==========================================
 
# Introduce the scene to the player
print("You wake up in a dimly lit room, as daylight filters through the bars, you see a door, a window and an old bed.")
print("What do you want to investigate?")

# Ask the player what they want to investigate
# .lower() converts their answer to lowercase
choice = input("Enter your choice (door, window, bed): ").lower()

# Check whether the player chose the door
if choice == "door":
    print("You approach the door and try the handle. It's locked.")

# Check whether the player chose the window
elif choice == "window":
    print("You look through the window and see a beautiful garden outside. But it's too high to jump.")
    print("The window is too small to climb through.")

# Check whether the player chose the bed
elif choice == "bed":
    print("You approach the bed and see a small Iron Key hidden under the pillow.")

else:
    print("This item doesn't seem to hide anything.")