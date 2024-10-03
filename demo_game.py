from adventurelib import *

Room.items = Bag()



current_room = starting_room = Room("""
You are in a dark room.
""")

valley = starting_room.north = Room("""
You are in a beautiful valley.
""")

magic_forest = valley.north = Room("""
You are in a enchanted forest where magic grows wildly.
""")

Dungeon = magic_forest.north = Room("""
You are in a dungeon
""")

mallet = Item('rusty mallet', 'mallet')
valley.items = Bag({mallet,})

World_Ender = Item('Atom Bomb', 'Game ender', 'World ender')
Dungeon.items = Bag({World_Ender,})

inventory = Bag()
#
#       N
#     W + E
#       S
#
#Map Array
#      ________________
row0 = ["X", "D", " X"]
row1 = ["X", "MF", "X"]
row2 = ["X", "V", " X"]
row3 = ["X", "DR", "X"]


#Map Function
@when('map')
def map():
    print(row1)
    print(row2)
    print(row3)



@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        current_room = room
        say('You go %s.' % direction)
        look()
        if room == magic_forest:
            set_context('magic_aura')
        else:
            set_context('default')

#take item function
@when('take ITEM')
def take(item):
    obj = current_room.items.take(item)
    if obj:
        say('You pick up the %s.' % obj)
        inventory.add(obj)
    else:
        say('There is no %s here.' % item)


@when('drop THING')
def drop(thing):
    obj = inventory.take(thing)
    if not obj:
        say('You do not have a %s.' % thing)
    else:
        say('You drop the %s.' % obj)
        current_room.items.add(obj)


@when('look')
def look():
    say(current_room)
    if current_room.items:
        for i in current_room.items:
            say('A %s is here.' % i)


@when('inventory')
def show_inventory():
    say('You have:')
    for thing in inventory:
        say(thing)

@when('cast', context='magic_aura', magic=None)
@when('cast MAGIC', context='magic_aura')
def cast(magic):
    if magic == None:
        say("Which magic you would like to spell?")
    elif magic == 'fireball':
        say("A flaming Fireball shoots form your hands!")
    elif magic == 'Earthquake':
        say("A rumbling Earthquake shakes the world!")

@when('use THING')
def use(thing):
    obj = inventory.take(thing)
    if not obj:
        say("You do not have %s" % thing)
    elif thing == mallet:
        say("You swing the %s" % thing)
        inventory.add(obj)
    elif thing == World_Ender:
        say("The world Self Destructs" % thing)
        quit()
    else:
        say("You use %s" % thing)
        inventory.add(thing)


look()
start()
