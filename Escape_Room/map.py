from items import *

location_centre = {
    "name": "Centre of the room",

    "description": """Find a way to escape the room! To the SOUTH there is a Fireplace.
from the WEST of the room there is a Bookshelf. From NORTH of the room there is a locked door with a keypad. 
You also see an office desk NORTH-EAST. There is a mysterious dark corner SOUTH-EAST of the room. 
Good luck you have 20 minutes!""",

    "exits": {"south": "fireplace", "west": "bookshelf", "north": "door", "north-east": "office desk", "south-east": "dark corner"},

    "items": [item_screwdriver]
}

location_Fireplace = {
    "name": "The Fireplace",

    "description": "The fireplace is made of brick and has a red brick chimney."
                   "The brick is very old and worn, but still strong enough to support the weight of a person. ",

    "exits":  {"north": "centre", "east": "dark corner"},

    "items": [unpowered_torch]
}

location_bookshelf = {
    "name": "Bookshelf",

    "description": """The bookshelf is full of old books and they are all very dusty.
You see a book standing out which appears to be a diary""",

    "exits": {"north-east": "door", "east": "centre"},

    "items": [item_diary]
}

Location_desk = {
    "name": "The office desk",

    "description": """You see a desk with what looks to be a safe underneath it.
You open the drawer, and sure enough, there is a small safe.""",

    "exits": {"west": "door", "south-west": "centre", "south" : "dark corner"},

    "items": [item_safe]
}

location_dark_corner = {
    "name": "a dark corner of the room",

    "description": """The dark corner is filled with dust, cobwebs and old papers.
There are also some old computers that no one uses anymore, probably the remnants of old computer science students.""",

    "exits": {"west": "fireplace", "north": "office desk", "north-west": "centre"},

    "items": []
}
location_door = {
    "name": "level 1 Escape door",

    "description": """The door is locked, the keypad has a red light that’s blinking.
You press the buttons randomly to no avail. You press more random buttons and the red light blinks faster. :( """,

    "exits": {"south": "centre"},
    "locked": True,
    "items": []

}
location_entrance = {
    "name": "level 2 Entrance",

    "description": """You find yourself in another level of the basement.
It takes a minute for your eyes to adjust to this new, brighter room.In this room there is a trap door with stairs leading up to it.
There seems to be a desk underneath the stairs. There are multiple different rooms to the NORTH, WEST, SOUTH, EAST, SOUTH-EAST and then back DOWNSTAIRS.
Once again you have 20 minutes, be careful and good luck.""",

    "exits": {"north": "wine cellar", "west": "storage room", "south": "boiler room", "east": "trap door", "south-east": "desk", "downstairs": "door"},

    "items": [],
    "entered": False
}
location_winecellar = {
    "name": "Wine Cellar",

    "description": """The wine cellar is filled wall to wall with the finest Lambrini and Echo Falls known to man.
As you inspect the Lambrini closer, something shiny at the bottom catches your eye.""",

    "exits": {"south": "entrance"},

    "items": [item_winebottle]
}
location_storage = {
    "name": "Storage Room",

    "description": """Infront of you a closet looms large but there are no handles to open the doors.
Confused, you scan the room to see if there is anything else useful.""",

    "exits": {"north": "closet", "east": "entrance"},

    "items": []
}
location_boileroom = {
    "name": "Boiler Room",
    
    "description": "The boiler looks battered and rusty. There is a hole in the bottom and the valve connection seems loose.",

    "exits": {"north": "entrance"},

    "items": [],
    "valve_open": False,

}
desk = {
    "name": "desk",
    "description": """The desk is similar to the one in the other room, there are many drawers that could hold important items.
Sure enough in one of the drawers there is a lock box that has a password. To unlock this box you must guess the word.""",
    "exits": {"north-west": "entrance"},
    "items": []
}
trap_door = {
    "name": "trap door",
    "description": """The trap door is locked!
There is an electronic lock, you could use your key again but there is no guarantee it seems unlikely it will work again. The lock also seems to have no power.""",
    "exits": {"west": "entrance"},
    "open": False,
    "items": [item_lock]
}
closet = {
    "name": "closet",
    "description": """You are amazed that the door is now mysteriously open, wondering how it happened you inspect it further.
The closet is wooden with dusty shelves and old literary texts. There is a key card here as well.""",
    "open": False,
    "exits": {"south": "storage room"},
    "items": [key_card]
}
locations = {
    "fireplace": location_Fireplace,
    "dark corner": location_dark_corner,
    "centre": location_centre,
    "bookshelf": location_bookshelf,
    "office desk": Location_desk,
    "door": location_door,
    "entrance": location_entrance,
    "wine cellar": location_winecellar,
    "storage room": location_storage,
    "boiler room": location_boileroom,
    "trap door": trap_door,
    "desk": desk,
    "closet": closet
}

