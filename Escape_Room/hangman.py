import time
from collections import Counter
from map import *

def hangman(word):
    print('Guess the word! HINT: you may find this thing in your bedroom')
    print("You will have 15 chances to guess the word. ")

    for i in word:
        # For printing the empty spaces for letters of the word
        print('_', end=' ')
        print()

    playing = True
    # list for storing the letters guessed by the player
    letterGuessed = ''
    chances = 15
    correct = 0
    flag = 0
    try:
        while (chances != 0) and flag == 0:  # flag is updated when the word is correctly guessed
            print()
            print("You have " + str(chances) + " guesses left!")
            chances -= 1

            try:
                guess = str(input('Enter a letter to guess: '))
            except:
                print('Enter only a letter!')
                continue
            # Validation of the guess
            if not guess.isalpha():
                print('Enter only a LETTER')
                continue
            elif len(guess) > 1:
                print('Enter only a SINGLE letter')
                continue
            elif guess in letterGuessed:
                print('You have already guessed that letter')
                continue

            # If letter is guessed correctly
            if guess in word:
                k = word.count(guess)  # k stores the number of times the guessed letter occurs in the word
                for _ in range(k):
                    letterGuessed += guess  # The guess letter is added as many times as it occurs

            # Print the word
            for char in word:
                if char in letterGuessed and (Counter(letterGuessed) != Counter(word)):
                    print(char, end=' ')
                    correct += 1
                # If user has guessed all the letters
                elif (Counter(letterGuessed) == Counter(word)):  # Once the correct word is guessed fully,
                    # the game ends, even if chances remain
                    print("The word is: ", end=' ')
                    print(word)
                    flag = 1
                    print('Congratulations, You won!')
                    print()
                    time.sleep(1)
                    print("You hear a strange click sound from the closet in the storage room")
                    closet["open"] = True
                    break  # To break out of the for loop
                    break  # To break out of the while loop
                else:
                    print('_', end=' ')

        # If user has used all of his chances
        if chances <= 0 and (Counter(letterGuessed) != Counter(word)):
            print()
            print('You lost! Try again..')
            print('The word was {}'.format(word))

    except KeyboardInterrupt:
        print()
        print('Bye! Try again.')
        exit()

