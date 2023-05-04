from project.animal.carnivore import Carnivore
from project.animal.herbivore import Herbivore
from project.animal.scavenger import Scavenger


class AnimalFactory:
    animal_types = {
        'Carnivore': Carnivore,
        'Herbivore': Herbivore,
        'Scavenger': Scavenger
    }

    def create_animal(self, animal_type):
        # print(animal_type)
        return self.__class__.animal_types[animal_type]()
