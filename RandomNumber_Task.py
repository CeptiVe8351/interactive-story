# # ==================================================
# # PRACTISE - NUMBER GUESSING GAME
# # ==================================================
 
# import random
 
# secret_number = random.randint(1, 10)
 
# guess = int(input("Guess a number between 1 and 10: "))
 
# # TODO:
# # Add a while loop that repeats while
# # guess is not equal to secret_number.
# #
# # Inside the loop:
# # 1. Tell the player their guess is incorrect.
# # 2. Ask them to guess again.
# # 3. Update the guess variable.
 
# print("Congratulations! You guessed correctly!")


import random

secret_number = random.randint(1, 10)

guess = int(input("Guess a number between 1 and 10: "))

while guess != secret_number:
    print("Incorrect! Try again.")
    guess = int(input("Guess another number: "))

print("Congratulations! You guessed correctly!")