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
