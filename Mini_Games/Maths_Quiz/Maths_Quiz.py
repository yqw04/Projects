import random

Player = False

while Player == False:
    # Begin/Reset round
    user_option = input("What questions would you like? \nAddition \nSubtraction \nDivision \nMultiplication\n")
    
    # Allow user to select their range
    num_start = int(input("Start range: "))
    num_end = int(input("End range: "))

    number_one = random.randrange(num_start, num_end)
    number_two = random.randrange(num_start, num_end)

    # Questions + Answers
    if user_option == "Addition":
        problem = f"{number_one} + {number_two} = "
        solution = number_one + number_two
    elif user_option == "Subtraction":
        problem = f"{number_one} - {number_two} = "
        solution = number_one - number_two
    elif user_option == "Division":
        problem = f"{number_one} / {number_two} = "
        solution = number_one / number_two
    elif user_option == "Multiplication":
        problem = f"{number_one} * {number_two} = "
        solution = number_one * number_two
    else:
        print("Invalid option. Please choose Addition, Subtraction, Division, or Multiplication.")
        continue  # Restart the loop if the option is invalid

    # Scoring
    user_answer = input(problem)
    if float(user_answer) == solution:  
        print("Correct!")
    else: 
        print("Nice try!, but the correct answer is " + str(solution))

    # Section to start/end game
    play = input("\nPlay again? Yes or No: ").lower()
    if play == "yes":
        Player = False
    else:
        print("Thanks for playing!")
        break