class Inventory():
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def drop(self, item):
        self.items.remove(item)

    def list(self):
        print ("You are carrying:")
        for item in self.items:
            print (item.get_name())

    def get(self, type):
        items_of_type = []
        for item in self.items:
            if isinstance(item, type):
                items_of_type.append(item)
        return items_of_type

    def process_command(self, command):
        result = []
        for item in self.items:
            if item.get_name() in command:
                result.append(item.process_command(command))
        return result


class Item():
    def __init__(self, name):
        self.name = name
        self.known_commands = {}

    def get_name(self):
        return self.name

    def process_command(self, command):
        for a_command in self.known_commands:
            if a_command in command:
                self.known_commands[a_command](command)

class Room():
    def __init__(self, name, description, id):
        self.name = name
        self.description = description
        self.id = id
        self.items = []
        self.connectors = []
        self.rooms = {}

    def add_item(self, item):
        self.items.append(item)

    def add_room(self, direction, room):
        self.rooms[direction] = room

    def add_connection(self, room, connector, actions):
        for direction in actions:
            self.rooms[direction] = room
        self.connectors.append((connector, actions[0]))

    def enter_room(self, inventory):
        print (self.name)
        print
        print (self.description)
        print
        for connector in self.connectors:
            print ("There is a " + connector[0] + \
                   " that goes " + connector[1] + ".")
        print
        for item in self.items:
            print ("You see a " + item.name + " here.")
        print

    def get_name(self):
        return self.name

    def is_valid_direction(self, direction):
        return direction in self.rooms.keys()

    def next_room(self, direction):
        return self.rooms[direction]

    def process_command(self, command, inventory):
        if command in self.rooms.keys():
            new_room = self.next_room(command)
            return new_room
        elif "get" in command or "take" in command:
            for item in self.items:
                if item.name in command:
                    inventory.add(item)
                    self.items.remove(item)
                    return "You picked up the " + item.name + "."
                else:
                    return "I don't know what you want to pick up."
        else:
            return None


entrance_stairs = Room('Stairs', 'You are at the entrance to the stariwell.', 's')
entrance_stairwell = Room('Entrance', 'You are in the Stairwell of e3 Civic High', 'e')
entrance = Room('Entrance', 'You are in the Entrance of e3 Civic High', 'e')
hallway1 = Room('Hallway', 'You are in the Hallway', 'h1')
hallway2 = Room('Hallway', 'You are in the Hallway', 'h2')
hallway3 = Room('Hallway', 'You are in the Hallway', 'h3')
hallway4 = Room('Hallway', 'You are in the Hallway', 'h4')
office1 = Room ('Front Office', 'You are in the Front Office', 'fo')
bathroom1 = Room('bathroom', 'You are in the bathroom.', 'br1')
hallway1part2 = Room('Hallway', 'You are still in the Hallway', 'h1p2')
entrance = Room('Entrance', 'You are in the Entrance of e3 Civic High', 'e')




# entrance connecting the entrance from the street to the stairwell
entrance_stairs.add_connection(entrance_stairwell, "doorway", ["south", "s"])
entrance_stairwell.add_connection(entrance_stairs, "doorway", ["north", "n"])

# connecting the stairwell to the entrance of e3
entrance_stairwell.add_connection(entrance, "doorway", ["south", "s"])
entrance.add_connection(entrance_stairwell, "doorway", ["north", "n"])

# connecting the entrance of e3 to the office to the west
entrance.add_connection(office1, "door", ["east", "e"])
office1.add_connection(entrance, "door", ["west", "w"])

# connecting the entrance of e3 to the 1st hallway to the east
entrance.add_connection(hallway1, "walkway", ["west", "w"])
hallway1.add_connection(entrance, "walkway", ["east", "e"])

# connecting the first half of hallway1 to the second half (hallway1part2)
hallway1.add_connection(hallway1part2, "walkway", ["west", "w"])
hallway1part2.add_connection(hallway1, "walkway", ["east", "e"])

#




inventory = Inventory()
current_room = entrance_stairs

while True:
    current_room.enter_room(inventory)
    command = raw_input("What would you like to do? ")
    if command in ["exit", "x", "quit", "q"]:
        break

    result = current_room.process_command(command, inventory)
    if isinstance(result, Room):
        current_room = result
        continue
    elif isinstance(result, str):
        print (result)
        continue

    result = inventory.process_command(command)
    if len(result) == 0:
        print ("I don't know what you mean.")


