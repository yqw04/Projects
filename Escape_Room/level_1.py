import time

from items import *
from player import *
from map import *


def open_diary(room_items):
    if item_diary in inventory:
        print("You opened the diary and found a hidden note.")
        time.sleep(0.8)
        room_items.append(item_note)
        item_diary.update({"open": True})
    else:
        print("You cannot open that.")
        time.sleep(0.8)


def open_safe(room_items):
    print("To open this safe you need a passcode.")
    time.sleep(0.8)
    print("Please enter the passcode.")
    passcode = input()
    if passcode == "042":
        print("THE PASSCODE WAS CORRECT!")
        time.sleep(0.8)
        print("Inside the safe you found a pair of batteries.")
        time.sleep(0.8)
        room_items.append(item_batteries)
        item_safe.update({"open": True})
    else:
        print("You try the code", passcode, "but the safe wouldn't open.")
        time.sleep(0.8)
        print("TRY AGAIN.")
        time.sleep(0.8)


def remove_battery_torch():
    if powered_torch in inventory:
        inventory.remove(powered_torch)
        inventory.append(item_batteries)
        inventory.append(unpowered_torch)
        print("You removed the batteries from the torch")
        time.sleep(0.5)


def use_battery_torch():
    if item_batteries in inventory:
        if unpowered_torch in inventory:
            inventory.remove(item_batteries)
            inventory.remove(unpowered_torch)
            inventory.append(powered_torch)
            print("You placed the batteries in the torch.")
            time.sleep(0.5)


def use_torch(room):
    if powered_torch in inventory:
        if room == location_dark_corner:
            room["items"].append(item_key)
        else:
            print("There is no use for the torch in this room")
            time.sleep(0.8)
    elif unpowered_torch in inventory:
        print("You flick the on/off button but the torch wouldn't turn on, "
              "(try finding some batteries to power the torch)")
        time.sleep(0.8)
    else:
        print("You cannot do that")
        time.sleep(0.4)


def read_note():
    if item_note in inventory:
        print("You read the note and notice a strange puzzle")
        time.sleep(0.8)
        print("682 >> one digit is correct & well placed")
        time.sleep(0.8)
        print("614 >> one digit is correct but wrong placed")
        time.sleep(0.8)
        print("206 >> two numbers are correct but wrong placed")
        time.sleep(0.8)
        print("738 >> nothing is correct")
        time.sleep(0.8)
        print("870 >> one number is correct but wrong placed")
        time.sleep(5)
    else:
        print("There is no note to read")
