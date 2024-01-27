from itertools import count
from operator import truediv
from items import *
from player import *
from map import *
from datetime import datetime
from gameparser import *
import time


def drink_wine():
    counter = 0
    x = ""
    while counter < 3:
        if counter < 1:
            time.sleep(1)
            print('You drink a glass of the wine, but have not got much closer to getting the clue.')
            time.sleep(0.8)
            print('Would you like to drink another glass?')
            time.sleep(0.8)
            print('YES or NO')
            more = str(input('> '))
            if more == 'yes':
                counter += 1
            else:
                counter = 3
                x = 1
        elif counter == 1:
            time.sleep(1)
            print()
            print('You enjoy a second glass of wine, but can not see the bottom yet.')
            time.sleep(0.8)
            print('Would you like to drink another glass?')
            time.sleep(0.8)
            print('YES or NO')
            more = str(input('> '))
            if more == 'yes':
                counter += 1
            else:
                counter = 3
                x = 2
        else:
            time.sleep(1)
            print(".")
            time.sleep(0.2)
            print(".")
            time.sleep(0.2)
            print(".")
            time.sleep(0.2)
            print('You pass out from too much alchohol consumption.')
            time.sleep(0.8)
            print('You wake up 5 minutes later on the floor of the wine cellar.')
            time.sleep(1)
            print('...')
            counter += 1
            time.sleep(4)
            x = 3
    return x
            

def close_valve():
    if item_screwdriver in inventory:
        if location_boileroom["valve_open"]:
            location_boileroom["valve_open"] = False
            print("Well done! You stopped the leak!")
            time.sleep(0.8)
        else:
            print("Valve is closed")
            time.sleep(0.8)
    else:
        print("You need a screwdriver to close the valve")
        time.sleep(0.8)



def open_trapdoor(room):
    if room == trap_door:
        if item_lock["batteries"]:
            if key_card in inventory:
                trap_door["open"] = True
            else:
                time.sleep(0.8)
                print("You need a key card to open the lock.")
        else:
            time.sleep(0.8)
            print("The electrical lock requires batteries to open.")
    else:
        time.sleep(0.8)
        print("Command isn't available in this room")


def use_battery_lock(room):
    if room == trap_door:
        if item_batteries in inventory:
            item_lock["batteries"] = True
            inventory.remove(item_batteries)
            print("You placed the batteries in the electrical lock.")
            time.sleep(1)

def gas_timer(timer):
    time.sleep(0.8)
    current_time = datetime.now()
    time_taken = current_time - timer
    time_left = 180 - time_taken.total_seconds()
    minutes = time_left//60
    seconds = time_left%60
    if time_left > 0:
        print("You have", round(minutes), "minutes and", round(seconds), "seconds before the room fills with gas.")
