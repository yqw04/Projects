import random
import csv

Player = False

# For trial purposes, the csv reader is set to example.csv automatically
# csv_filename = input("Enter the CSV filename: ")

# Imports words from csv
with open('example.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    word_list = []
    for row in spamreader:
        word_list.append(row[0])

while Player == False:    
    # Allows players to guess words containing a certain amount of letters
    try:
        num_letter = int(input("How many letters? 3, 4, 5 or 6: "))
        filtered_words = []
        for word in word_list:
            if len(word) == num_letter:
                filtered_words.append(word)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue  

    random_word = random.choice(filtered_words)
    guessed_correctly = False
    print("To give up type 'give up'")

    while guessed_correctly == False:
        # Player guesses
        try:
            user_guess = input("Guess a word: ").lower()
        except ValueError:
            print("Invalid input. Please enter a valid word.")
            continue  
        
        if user_guess == random_word:
            print("You got it!")
            guessed_correctly = True
        elif user_guess == 'give up':
            break
        # Section to show if a letter is correct
        else:
            word = [] 
            for i in range(num_letter):
                if user_guess[i] == random_word[i]:
                    print("The letter " + user_guess[i] + " is in the correct place")
                    word.append(user_guess[i])
                elif user_guess[i] in random_word:
                    print("The letter " + user_guess[i] + " is in the word")
                    word.append("_")
                else:
                    word.append("_")

            print(''.join(word))

    # Section to start/end game
    play = input("\nPlay again? Yes or No: ").lower()
    if play == "yes":
        Player = False
    else:
        print("Thanks for playing!")
        break  