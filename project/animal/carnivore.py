class Carnivore:

    def __init__(self):
        self.animal_type = 'Carnivore'
        # self.food_type = 'alive animals'
        self.hunger_rate = 10
        self.status = 'alive'
        self.has_moved = False
        self.has_eaten = False
        self.is_eaten = False

    def animal_status(self):
        return self.status
