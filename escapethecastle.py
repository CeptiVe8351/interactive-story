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
print(f"\n{playerName}, you wake up in a dimly lit room. You see a door to your left and a window to your right.")
print("You hear a faint sound of footsteps approaching.")
print("Your adventure begins now. What will you do?")