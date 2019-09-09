"""
##### 0) Header #####
# Text Adventure Game
A chance to make your own Text Adventure Game.
This is an INDIVIDUAL project. Do not consult with others or share code.
Refer to the instructions on Canvas for more information.

# When You Are Done
When you pass all tests, remember to clean and document your code.
Be sure to unit test and document your functions.
"""

##### 1) Author Info #####

# Change these three fields
__author__ = "andychen@udel.edu"
__title__ = "Saving Sam"
__description__ = "One day you at your home, and you get a phone call from kidnapper about kidnapping your girlfriend. Therefore, you are going to save her."

# Leave these two fields unchanged
__version__ = 1
__date__ = "Spring 2019"


##### 2) Record Definitions #####
# Add a new record and modify the existing ones to fit your game.

'''
Records:
    World:
        status (str): Whether or not the game is "playing", "won",
                      "quit", or "lost". Initially "playing".
        map (dict[str: Location]): The lookup dictionary matching 
                                   location names to their
                                   information.
        player (Player): The player character's information.

      
    Player:
        location (str): The name of the player's current location.
        inventory (list[str]): The player's collection of items.
                               Initially empty.

    Location:
        about (str): A sentence that describes what this location 
                     looks like.
        neighbors (list[str]): A list of the names of other places 
                               that you can reach from this 
                               location.
        stuff (list[str]): A collection of things available at 
                           this location.
'''

##### 3) Core Game Functions #####
# Implement the following to create your game.

def render_introduction():
    '''
    Create the message to be displayed at the start of your game.
    
    Returns:
        str: The introductory text of your game to be displayed.
    '''
    
    return "== Saving Sam ==\n = By Yen-An Chen =\n After hearing a bad new that your girlfriend have been kidnapped from devil,\n you are at your bedroom."

def create_map():
    return {
        'bedroom': {
            'neighbors': ['kitchen', 'home entrance'],
            'about': "Your room is a mess and you receive them message from devil",
            'stuff': [],
        },
        'kitchen': {
            'neighbors': ['bedroom'],
            'about': "It's messy here, you are likely to pick up a knive",
            'stuff': ["knive"]
        },
        'home entrance': {
            'neighbors': ['bedroom', 'police station', "girlfriend's house"],
            'about': "You see your girlfriend's house and a police station.",
            'stuff': []
        },
        'police station': {
            'neighbors': ['home entrance'],
            'about': "You see a police officer inside and ask for help?.",
            'stuff': ["police officer"]
        },
        "girlfriend's house": {
            'neighbors': ['home entrance'],
            'about': "You see a devil kidnapping your girlfriend.",
            'stuff': ["devil"]
        }
    }
    
def create_player():
    return {
        'location': 'bedroom',
        'inventory': [],}
        
def create_world():
    '''
    Creates a new version of the world in its initial state.
    Returns:
        World: The initial state of the world
    '''
    
    return {
        'map': create_map(),
        'player': create_player(),
        'status': "playing"}

def render(world):
    '''
    Consumes a world and produces a string that will describe the current stateof the world. Does not print.
    
    Args:
        world (World): The current world to describe.
        
    Returns:
        str: A textual description of the world.
    '''
    
    return (render_location(world) + render_visible_stuff(world))
    
def render_location(world):
    
    location = world['player']['location']
    here = world['map'][location]
    about = here['about']
    return ("You are in " + location + "\n" + about + "\n")

def render_visible_stuff(world):
    location = world['player']['location']
    here = world['map'][location]
    stuff = here['stuff']
    inventory = world['player']['inventory']

    visible_stuff = []
    for thing in stuff:
        if thing == 'knive':
            visible_stuff.append(thing)
        else:
            visible_stuff.append(thing)

    return "You see: " + ', '.join(visible_stuff)
    
    
def get_options(world):
   
    '''
    Consumes a world and produces a list of strings representing the options
    that are available to be chosen given this state.
    
    Args:
        world (World): The current world to get options for.
    
    Returns:
        list[str]: The list of commands that the user can choose from.
    '''
    commands = ["Quit"] 
    
    location = world['player']['location']
    here = world['map'][location]
    stuff = here['stuff']
    inventory = world['player']['inventory'] 
    
    if location == 'kitchen' and 'knive' in stuff and 'knive' not in inventory:
        commands.append("pick up knive")
        inventory.append("knive")
    if location == 'police station' and 'police officer' in stuff:
        commands.append("ask police officer for help")
    if location == "girlfriend's house" and 'devil' in stuff and 'knive' in inventory:
        commands.append('fight with your knive')
    if location == "girlfriend's house" and 'devil' in stuff and 'knive' not in inventory:
        commands.append('fight devil without weapon')
    if location == 'bedroom':
        commands.append('go to kitchen')
    if location == 'bedroom':
        commands.append('go to home entrance') 
    if location == 'kitchen':
        commands.append('go to bedroom')
    if location == 'home entrance':
        commands.append('go to bedroom')
    if location == 'home entrance':
        commands.append('go to police station')
    if location == 'home entrance':
        commands.append("go to girlfriend's house")
    if location == 'police station':
        commands.append('go to home entrance')
    else:
        return commands
    return commands
    
def goto(world,command):
    new_location = command[len('go to '):]
    world['player']['location'] = new_location
    return "You went to " + new_location
    
    
def update(world, command):
    
    '''
    Consumes a world and a command and updates the world according to the
    command, also producing a message about the update that occurred. This
    function should modify the world given, not produce a new one.
    
    Args:
        world (World): The current world to modify.
    
    Returns:
        str: A message describing the change that occurred in the world.
    '''
    
    if command.startswith('go to '):
        return goto(world,command)
    if command == "Quit":
        world['status'] = 'quit'
        return "You quit the game"
    elif command == "ask police officer for help":
        world['status'] = 'lost'
        return "You lost the game"
    elif command == "fight with your knive":
        world['status'] = 'won'
        return "you won the game"
    elif command == "fight devil without weapon":
        world['status'] = 'lost'
        return "you lost the game"
    else:
        return "Unknown command: " + command
    
    
def render_ending(world):
    '''
    Create the message to be displayed at the end of your game.
    
    Args:
        world (World): The final world state to use in describing the ending.
    
    Returns:
        str: The ending text of your game to be displayed.
    '''

    if world['status'] == 'won':
        return "You won!"
    elif world['status'] == 'lost':
        return "You lost."
    elif world['status'] == 'quit':
        return "You quit."
        
    
def choose(options):
    '''
    Consumes a list of commands, prints them for the user, takes in user input
    for the command that the user wants (prompting repeatedly until a valid
    command is chosen), and then returns the command that was chosen.
    
    Note:
        Use your answer to Programming Problem #42.3
    
    Args:
        options (list[str]): The potential commands to select from.
    
    Returns:
        str: The command that was selected by the user.
    '''
    print("You can:")
    for option in options:
        print(option)
    print("What will you do?")
    while True:
        reply = input()
        if reply in options:
            return reply

###### 4) Win/Lose Paths #####
# The autograder will use these to try out your game
# WIN_PATH (list[str]): A list of commands that win the game when entered
# LOSE_PATH (list[str]): A list of commands that lose the game when entered.

WIN_PATH = ["go to kitchen",
            "pick up knive",
            "go to bedroom",
            "go to home entrance",
            "go to girlfriend's house",
            "fight with your knive"]
LOSE_PATH = []
    
###### 5) Unit Tests #####
# Write unit tests here

from cisc108 import assert_equal

assert_equal(render_introduction(),"""== Saving Sam == 
                                      = By Yen-An Chen =
                                      After hearing a bad new that your girlfriend have been kidnapped from devil,
                                      you are at your bedroom.""")
                                      
assert_equal("Saving Sam" in render_introduction(), True)


###### 6) Main Function #####
# Do not modify this area

def main():
    '''
    Run your game using the Text Adventure console engine.
    Consumes and produces nothing, but prints and indirectly takes user input.
    '''
    print(render_introduction())
    world = create_world()
    while world['status'] == 'playing':
        print(render(world))
        options = get_options(world)
        command = choose(options)
        print(update(world, command))
    print(render_ending(world))

if __name__ == '__main__':
    main()
