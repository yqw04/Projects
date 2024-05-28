import random

Player = False

while Player == False:
    # Begin/Reset round
    count = input("How many rounds? ")
    win = 0
    lose = 0

    for i in range(int(count)):
        # Information for player
        word = ["rock", "scissors", "paper"]
        user_word = input("Choose rock, paper, or scissors: ").lower() 
        while user_word not in word:
            print("Please choose between rock, paper, or scissors.")
            user_word = input("Choose rock, paper, or scissors: ").lower()
        
        random_word = random.choice(word)
        print("Computer chose:", random_word)

        # All the possiblities 
        if user_word == random_word:
            print("Tie")
        elif user_word == "rock":
            if random_word == "scissors":
                print("You win")
                win = win + 1
            else:
                print("You lose")
                lose = lose + 1
        elif user_word == "paper":
            if random_word == "rock":
                print("You win")
                win = win + 1
            else:
                print("You lose")
                lose = lose + 1
        elif user_word == "scissors":
            if random_word == "paper":
                print("You win")
                win = win + 1
            else:
                print("You lose")
                lose = lose + 1

    # Scoring 
    print("Final score:", win, ":", lose)
    if win > lose:
        print("You win the game!")
    elif win < lose:
        print("You lose the game.")
    else:
        print("The game is a tie.")

    # Section to start/end game
    play = input("Play again? Yes or No: ").lower()
    if play == "yes":
        Player = False
    else:
        print("Thanks for playing!")
        break