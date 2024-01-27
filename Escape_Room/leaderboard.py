import csv, datetime
from email.utils import format_datetime
from datetime import datetime
from csv import reader

def view_leaderboard(filename):

    if filename == 'Times.csv':
        print('LEVEL 1 \n')
    else:
        print('LEVEL 2 \n')

    print("________Leaderboard________\n")

    with open(str(filename)) as csv_file:
       csv_reader = csv.reader(csv_file, delimiter=',')
       line_count = 0  #csv reader becomes a 2d list with contents of the Times.csv file
       for row in csv_reader:
            if line_count == 0:
                pass
                line_count += 1
            else:
                time = row[2] 
                time = int(time)
                minutes = round(time // 60)
                seconds = round(time % 60)
                time = [str(minutes), str(seconds)]
                name = row[1]

                print(f'{row[1]} escaped in {time[0]} minutes and {time[1]} seconds!')
                line_count += 1

def append_leaderboard(seconds_used,filename):  #time_used = 20 minutes - time remaining

    minutes = seconds_used // 60
    seconds = seconds_used % 60
    time = [round(minutes), round(seconds)] 

    print("Congrats, enter your name on the leaderboard!")
    name = input("What's your name? : ")
    print('Well done! '+name)
    print(f'You escaped in {time[0]} minutes and {time[1]} seconds')

    file = open(str(filename), 'r') 
    csv_reader = reader(file)
    list_of_rows = list(csv_reader)

    lastrow = list_of_rows[-1]
    old_index = lastrow[0] 

    if old_index == 'index':
        old_index = 0

    newindex = int(old_index) + 1
    file.close()

    file = open(str(filename), 'w')
    for row in list_of_rows:
        
        newRecord = str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "\n"
        file.write(newRecord)   

    lastRecord = str(newindex) + "," + str(name) + "," + str(seconds_used) + "\n"
    file.write(str(lastRecord))       #Writes data into the file
    file.close()

    print("Input 'Yes' or 'No'")
    userinput = input("Would you like to view the leaderboard? : ")
    userinput = userinput.lower()
    if userinput == 'yes':
        view_leaderboard(filename)
        print('Returning back to the game...')
    elif userinput == 'no':
        print("Continuing back into the game...")
    

    #Returns back to game.py
