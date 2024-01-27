#!/usr/bin/python3
global current_room
global current_level

from map import *
from player import *
from gameparser import *
from hangman import *
from datetime import datetime
from items import *
from level_1 import *
import time
from level_2 import *
from leaderboard import *


start_time = ""
gas_starttime = ""
time_penalty = False


def list_of_items(items):
    time.sleep(0.1)
    new_list = ""
    for number in range(len(items)):
        if number == len(items) - 1:
            new_list += items[number]["name"]
        else:
            new_list += items[number]["name"] + ", "

    return new_list


def print_room_items(room):
    time.sleep(0.8)
    if room["items"]:
        print("There is", list_of_items(room["items"]), "here." + "\n")


def print_inventory_items(items):
    time.sleep(0.1)
    if items:
        print("You have", list_of_items(items) + "." + "\n")


def print_room(room):
    # Display room name
    print()
    print(room["name"].upper())
    print()
    time.sleep(0.5)
    # Display room description
    print(room["description"])
    print()
    time.sleep(1.2)
    print_room_items(room)
    time.sleep(0.5)

    #
    # COMPLETE ME!
    #


def exit_leads_to(exits, direction):
    return locations[exits[direction]]["name"]


def print_exit(direction, leads_to):
    time.sleep(0.2)
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    global current_level
    time.sleep(0.5)
    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))
    for items in room_items:
        if items["pick-up"]:
            time.sleep(0.2)
            print("TAKE", items["id"], "to take", items["name"] + ".")

    for items in inv_items:
        time.sleep(0.2)
        print("DROP", items["id"], "to drop", items["name"] + ".")
    for items in inv_items:
        if "open" in items:
            if not items["open"]:
                time.sleep(0.2)
                print("OPEN", items["id"], "to open", items["name"] + ".")
    if not location_boileroom["valve_open"]:
        time.sleep(0.2)
        print("CHECK TIMER to check the time remaining")
    if current_room == location_door and location_door["locked"]:
        if current_level == "level 1":
            time.sleep(0.2)
            print("UNLOCK DOOR to attempt to unlock the escape door")
        else:
            time.sleep(0.2)
            print("GO UPSTAIRS to go back to level 1")
    if item_note in inv_items:
        time.sleep(0.2)
        print("READ NOTE to read the hidden note")
    if item_safe in room_items:
        if not item_safe["open"]:
            time.sleep(0.2)
            print("OPEN SAFE to attempt to open the safe")
        else:
            "You've already opened the safe"
    if item_batteries in inventory and unpowered_torch in inventory:
        time.sleep(0.2)
        print("USE BATTERIES for TORCH to place the batteries in the torch")
    # if item_batteries in inventory and item_lock in inventory:
    #     print("USE BATTERIES for LOCK to place the batteries in the torch")
    if (powered_torch in inv_items) or (unpowered_torch in inv_items):
        time.sleep(0.2)
        print("USE TORCH to use your torch")
    if current_room == location_boileroom and location_boileroom["valve_open"]:
        time.sleep(0.2)
        print("CLOSE valve to close the valve and stop the leakage")
    if location_boileroom["valve_open"]:
        time.sleep(0.2)
        print("CHECK GAS TIMER to see how long left before the room fills with gas")
    if item_winebottle in inventory:
        time.sleep(0.2)
        print('DRINK WINE to have a glass of wine')
    if powered_torch in inventory:
        print("REMOVE BATTERIES from TORCH to remove the batteries from the torch")
        time.sleep(0.2)
    if current_room==desk:
        print("PLAY HANGMAN to play a game of hangman")
    if current_room==trap_door and item_batteries in inventory:
        print("USE BATTERIES for LOCK to place the batteries in the electrical lock")
        time.sleep(0.2)
    if current_room==trap_door:
        print("OPEN TRAP DOOR to open the trap door and exit out of it")
        time.sleep(0.2)
    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    time.sleep(0.1)
    return chosen_exit in exits


def execute_go(direction):
    global current_room
    if is_valid_exit(current_room["exits"], direction):
        new_room = move(current_room["exits"], direction)
        if new_room == closet and not closet["open"]:
            print("The closet is locked, complete an activity to open the closet")
            time.sleep(0.8)
        else:
            current_room = new_room
            return current_room
    else:
        print("You cannot go there")
        time.sleep(0.8)

def execute_take(item_id):
    found = False
    for items in current_room["items"]:
        if item_id == items["id"]:
            found = True
            if len(inventory) < 3:
                inventory.append(items)
                current_room["items"].remove(items)
            else:
                print("Your inventory is full, Drop an item to free some space.")
                time.sleep(0.8)
    if not found:
        print("You cannot take that.")
        time.sleep(0.4)


def execute_drop(item_id):
    found = False
    for items in inventory:
        if items["id"] == item_id:
            current_room["items"].append(items)
            inventory.remove(items)
            found = True

    if not found:
        print("You cannot drop that.")
        time.sleep(0.3)


def time_taken():
    current_time = datetime.now()
    time_taken = (current_time - start_time).total_seconds()
    if time_penalty:
        time_taken = time_taken + 300
    minutes = time_taken // 60
    seconds = time_taken % 60
    time = [round(minutes), round(seconds)]
    return time


def unlock_door():
    time.sleep(0.2)
    global current_room
    global start_time
    minutes = time_taken()[0]
    seconds = time_taken()[1]
    if current_room["name"] == "level 1 Escape door":
        if location_door["locked"]:
            if item_key in inventory:
                totalseconds = (minutes * 60) + seconds
                append_leaderboard(totalseconds, 'Times.csv')
                while True:
                    print("WELL DONE! You've escaped LEVEL 1 in a time of", minutes, "minutes and", seconds,"seconds")
                    print("Type CONTINUE to begin the next level")
                    response = input()
                    if normalise_input(response)[0] == "continue":
                        location_door["locked"] = False
                        location_door["exits"].update({"upstairs": "entrance"})
                        current_room = locations["entrance"]
                        start_time = datetime.now()
                        print("You open the door and see a staircase. You decide to head up to the next level...")
                        time.sleep(3)
                        break

            else:
                print("You need a key to open the door")
        else:
            print("Door is already unlocked")
    else:
        print("There is no door to open")


def check_timer():
    current_time = datetime.now()
    time_taken = current_time - start_time
    time_left = 1200 - time_taken.total_seconds()
    if time_penalty:
        time_left = time_left - 300
    minutes = time_left//60
    seconds = time_left%60
    print("You have", round(minutes), "minutes and", round(seconds), "seconds")
    time.sleep(0.2)



def execute_command(command):
    global time_penalty
    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    elif command[0] == "read":
        if command[1] == "note":
            read_note()
        else:
            print("Read what?")

    elif command[0] == "open":
        if command[1] == "diary":
            open_diary(current_room["items"])
        elif command[1] == "safe":
            open_safe(current_room["items"])
        elif command[1] == "trap" and command[2] == "door":
            open_trapdoor(current_room)
        else:
            print("Open what?")

    elif command[0] == "check":
        if len(command) > 1:
            if command[1] == "timer":
                check_timer()
            elif command[1] == "gas":
                if location_boileroom["valve_open"]:
                    gas_timer(gas_starttime)
        else:
            print("Check what?")
    elif command[0] == "unlock":
        if command[1] == "door":
            unlock_door()
        else:
            print("unlock what?")
    elif command[0] == "close":
        if command[1] == "valve":
            close_valve()
        else:
            print("unlock what?")
    elif command[0] == "use":
        if len(command) > 1:
            if command[1] == "batteries":
                if len(command) > 2:
                    if command[2] == "torch":
                        use_battery_torch()
                    elif command[2] == "lock":
                        use_battery_lock(current_room)
                else:
                    print("use batteries on what?")
            elif command[1] == "torch":
                use_torch(current_room)
        else:
            print("use what?")
    elif command[0] == "remove":
        if len(command) > 1:
            if command[1] == "batteries":
                if len(command) > 2:
                    if command[2] == "torch":
                        remove_battery_torch()
                else:
                    print("remove batteries from what?")
            elif command[1] == "torch":
                use_torch(current_room)
        else:
            print("remove what?")
    elif command[0] == "drink":
        if command[1] == "wine":
            x = drink_wine()
            if x == 3:
                time_penalty = True
        else:
            print("drink what?")
    elif command[0] == "play":
        if command[1] == "hangman":
            hangman("closet")
        else:
            print("play what?")
    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    # Display menu

    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    # Next room to go to
    return locations[exits[direction]]


# This is the entry point of our program
def main():
    global current_level
    current_level = "level 1"
    global gas_starttime
    global start_time
    start_time = datetime.now()
    # Main game loop
    while True:
        current_time = datetime.now()
        time_used = current_time - start_time
        time_left = 1200 - time_used.total_seconds()
        if time_penalty:
            time_left = time_left - 300
        if time_left < 0:
            print("Oh no! You ran out of time!")
            break
        if location_boileroom["valve_open"]:
            gastime = current_time - gas_starttime
            gastime_left = 180 - gastime.total_seconds()
            if time_penalty:
                gastime_left = gastime_left - 300
            if gastime_left <= 0:
                print("OH NO! The floor was filled with gas and you died")
                break
        # Display game status (room description, inventory etc.)
        if current_room == location_entrance:
            if not location_entrance["entered"]:
                location_boileroom["valve_open"] = True
                print("You immediately start hearing a high pitched hissing sound. You look around and see a valve needs to be closed. If only you had come sort of utensil to shut it.")
                print("You've got 3 minutes to close the valve in the boiling room before the room fills with gas.")
                time.sleep(5)
                gas_starttime = datetime.now()
                location_entrance["entered"] = True
        if trap_door["open"]:
            minutes = time_taken()[0]
            seconds = time_taken()[1]
            print()
            print("WELL DONE! You have completed the escape room.")
            print('You took', minutes, 'minutes and', seconds, 'seconds.')
            
            lvl2seconds = (minutes * 60) + seconds
            append_leaderboard(lvl2seconds, 'Timeslvl2.csv')
            print()
            break

        print_room(current_room)
        print_inventory_items(inventory)

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
