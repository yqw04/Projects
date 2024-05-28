import random

Player = False

while Player == False:  
    # Allow user select number range
    try:
        print("What range? Please enter 2 numbers separately ")
        num_start = int(input("Start range: "))
        num_end = int(input("End range: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue  
    
    number = random.randrange(num_start, num_end)

    while True:
        # Player guessing
        try:
            user_option = int(input("Your guess: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue  

        # Possible outcomes
        if user_option == number:
            print("You got it! ")
            break
        elif user_option > number:
            print("Lower")
            
        elif user_option < number:
            print("Higher")
        else:   
            print("Invalid option. Please choose a number")
            continue

    # Section to start/end game
    play = input("\nPlay again? Yes or No: ").lower()
    if play == "yes":
        Player = False
    else:
        print("Thanks for playing!")
        break       