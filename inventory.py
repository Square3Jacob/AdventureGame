class Inventory():
    def __init__(self):
        self.items =[]


    def add(self, item):
        self.items.append(item)

    def drop(self, item):
        self.items.remove(item)

    def list(self):
        print "You are carrying:"
        for item in self.items:
            print item.get_name()

class Items():
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name



class Literature(Item):
    def __init__(self, name, contents = "This item is blank."):
        Item.__init__ (self, name)
        self.contents = "This item is blank"

    def read(self):
        print "This item is blank"

    def set_contents(self, contents):
        self.contents = contents


class Flashlight(Item):
    def __index__(self, name, battery_level=100, state="Off"):
        Item.__init__(self, name)
        self.battery_level = battery_level

    def
