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


class Literature(Item):
    def __init__(self, name, contents="This item is blank."):
        Item.__init__(self, name)
        self.contents = contents
        self.known_commands["read"] = self.read
        self.known_commands["write"] = self.write(command)

    def read(self, command):
        print (self.contents)

    def write(self, contents):
        self.contents = contents


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


class LightSource(Item):
    def __init__(self, name, on=False):
        self.on = on
        Item.__init__(self, name)
        self.known_commands["turn on"] = self.turn_on
        self.known_commands["turn off"] = self.turn_off

    @staticmethod
    def is_one_on(sources):
        if len(sources) > 0:
            for source in sources:
                if source.is_on():
                    return True
        return False

    def is_on(self):
        return self.on

    def turn_on(self, command):
        self.on = True
        print ("The " + self.name + " is on.")

    def turn_off(self, command):
        self.on = False
        print ("The " + self.name + " is off.")


class Flashlight(LightSource):
    def __init__(self, name="flashlight", battery_level=100, on=False):
        LightSource.__init__(self, name, on)
        self.battery_level = battery_level

    def change_batteries(self):
        self.battery_level = 100

    def compute_usage(self):
        # Compute the time it's been on and then drain the battery an equal amount
        pass


class DarkRoom(Room):
    def enter_room(self, inventory):
        light_sources = inventory.get(LightSource)
        if LightSource.is_one_on(light_sources):
            Room.enter_room(self, inventory)
        else:
            print ("You were eaten by a grue.")
            print ("Game over.")
            exit()


kitchen = Room('Kitchen', 'You are in the kitchen.', 'k')
dining = Room('Dining Room', 'You are in the dining room.', 'd')
hallway = Room('Hallway', 'You are in the hallway.', 'h')
hallway2 = Room('Upstairs Hallway', 'You are in the hallway.', 'uh')
bedroom1 = Room('Bedroom', 'You are in a bedroom.', 'b1')
bedroom2 = Room('Bedroom', 'You are in a bedroom.', 'b2')
bedroom3 = DarkRoom('Bedroom', 'You are in a bedroom.', 'b3')
living = Room('Living Room', 'You are in the living room.', 'lr')

kitchen.add_connection(dining, "doorway", ["east", "e"])
dining.add_connection(kitchen, "doorway", ["west", "w"])
dining.add_connection(hallway, "doorway", ["north", "n"])
hallway.add_connection(dining, "doorway", ["south", "s"])
hallway.add_connection(hallway2, "staircase", ["up", "u"])
hallway.add_connection(living, "doorway", ["east", "e"])
living.add_connection(hallway, "doorway", ["west", "w"])
hallway2.add_connection(hallway, "starcase", ["down", "d"])
hallway2.add_connection(bedroom1, "door", ["north", "n"])
hallway2.add_connection(bedroom2, "door", ["west", "w"])
hallway2.add_connection(bedroom3, "door", ["east", "e"])
bedroom1.add_connection(hallway2, "door", ["south", "s"])
bedroom2.add_connection(hallway2, "door", ["east", "e"])
bedroom3.add_connection(hallway2, "door", ["west", "w"])

kitchen.add_item(Flashlight())

inventory = Inventory()
current_room = dining

while True:
    current_room.enter_room(inventory)
    command = input("What would you like to do? ")
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


