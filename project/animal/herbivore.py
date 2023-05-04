class Herbivore:

    def __init__(self):
        self.animal_type = 'Herbivore'
        # self.food_type = 'grass'
        self.hunger_rate = 10
        self.status = 'alive'
        self.has_moved = False
        self.has_eaten = False
        self.is_eaten = False

    def animal_status(self):
        return self.status

