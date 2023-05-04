import random

from project.animal.carnivore import Carnivore
from project.animal.herbivore import Herbivore
from project.animal.scavenger import Scavenger
from project.core.animal_factory import AnimalFactory
from project.core.terrain_cell_factory import TerrainCellFactory


class Terrain:

    terrain_cell_types = {
        1: 'WATER',
        2: 'DESERT',
        3: 'MOUNTAIN',
        4: 'GRASS',
    }

    animal_types = {
        1: 'Carnivore',
        2: 'Herbivore',
        3: 'Scavenger'
    }

    directions = {
        1: 'up',
        2: 'down',
        3: 'left',
        4: 'right'
    }

    def __init__(self, x, y, animals_count):
        self.x = x
        self.y = y
        self.animals_count = animals_count

        self.terrain_map = []
        self.animals_locations = {}
        self.animals_locations_after_hunger_games = []
        self.res = {}

        self.animals_keys = []
        self.dead_animals_count = 0

        self.all_animals_dead = False
        self.animals_locations_after_one_iteration = {}

        self.animal_factory = AnimalFactory()
        self.terrain_cell_factory = TerrainCellFactory()

    def create_terrain(self):
        # self.terrain_map = [[Terrain.terrain_cell_types[random.randint(1, 4)] for _ in range(self.y)] for _ in
        #                        range(self.x)]
        self.terrain_map = [
            [self.terrain_cell_factory.create_terrain_cell(Terrain.terrain_cell_types[random.randint(1, 4)]) for _ in
             range(self.y)] for _ in range(self.x)]
        # print(self.terrain_map)

    def fill_with_animals(self):
        # size = self.x * self.y

        for i in range(self.animals_count):
            # rand_position = random.randint(0, size - 1)
            rand_animal = Terrain.animal_types[random.randint(1, 3)]

            animal = self.animal_factory.create_animal(rand_animal)

            rand_row = random.randint(0, self.x - 1)
            rand_col = random.randint(0, self.y - 1)
            rand_position = f'{rand_row}:{rand_col}'

            self.animals_locations[animal] = rand_position

            if self.terrain_map[rand_row][rand_col].cell_type == 'WATER':
                animal.status = 'dead'
                self.dead_animals_count += 1
                print(f'Animal {animal.animal_type} stepped on water.')
                continue

            # self.animals_locations[animal] = rand_position

    def activate_animals(self):

        if self.dead_animals_count == self.animals_count:
            self.all_animals_dead = True
            print('There are no alive animals in the terrain.')
            return

        animals_position = self.animals_locations.items()

        # [print(f'{x}:{y}') for x, y in list(animals_position)]
        for animal, position in animals_position:
            if animal.hunger_rate < 5:
                different_type_animals_in_same_cell = []

                if animal.animal_type == 'Herbivore' and animal.status == 'alive':
                    row, col = position.split(':')
                    row, col = int(row), int(col)

                    if self.terrain_map[row][col].cell_type != 'GRASS':
                        animal.hunger_rate -= 1
                        if animal.hunger_rate <= 0:
                            animal.status = 'dead'
                            print(f'Animal {animal.animal_type} died of hunger.')
                            self.dead_animals_count += 1
                        continue
                    else:
                        animal.hunger_rate += 1
                        animal.has_eaten = True

                if animal.animal_type == 'Carnivore' and animal.status == 'alive':
                    for x, y in list(animals_position):
                        if y == position and x.animal_type != animal.animal_type and x.is_eaten == False:

                            different_type_animals_in_same_cell.append({x: y})
                            x.is_eaten = True
                            x.status = 'dead'
                            self.dead_animals_count += 1
                            animal.has_eaten = True

                    for animal_key_value in different_type_animals_in_same_cell:
                        for animal_key in animal_key_value.keys():
                            self.animals_keys.append(animal_key)

                    if animal.hunger_rate + len(different_type_animals_in_same_cell) <= 10 and animal.has_eaten == True:
                        animal.hunger_rate += len(different_type_animals_in_same_cell)
                    elif animal.hunger_rate + len(
                            different_type_animals_in_same_cell) > 10 and animal.has_eaten == True:
                        animal.hunger_rate = 10

                    # for remove_animal in Terrain.animals_keys:
                    #     animal.has_eaten = True
                    #     del Terrain.animals_locations[remove_animal]
                    # print(Terrain.animals_locations)

                if animal.animal_type == 'Scavenger' and animal.status == 'alive':
                    for x, y in list(animals_position):
                        if y == position and x.animal_type != animal.animal_type and x.status == 'dead':
                            different_type_animals_in_same_cell.append({x: y})
                            animal.has_eaten = True
                            x.is_eaten = True
                            self.dead_animals_count += 1

                    # print(different_type_animals_in_same_cell)

                    for animal_key_value in different_type_animals_in_same_cell:
                        for animal_key in animal_key_value.keys():
                            self.animals_keys.append(animal_key)
                    # print(f'Length of different types animals in same cell: {len(different_type_animals_in_same_cell)}')
                    if animal.hunger_rate + len(different_type_animals_in_same_cell) <= 10:
                        animal.hunger_rate += len(different_type_animals_in_same_cell)
                    else:
                        animal.hunger_rate = 10

                    # for remove_animal in Terrain.animals_keys:
                    #     del Terrain.animals_locations[remove_animal]
                    # print(Terrain.animals_locations)

                rand_num = random.randint(1, 4)
                direction = Terrain.directions[rand_num]

                if animal.status == 'alive' and animal.has_eaten == False:
                    animal.hunger_rate -= 1

                    if animal.hunger_rate <= 0:
                        animal.status = 'dead'
                        self.dead_animals_count += 1
                        continue

                    row, col = position.split(':')
                    row, col = int(row), int(col)

                    if direction == 'up':
                        if row - 1 < 0:
                            print(f'{animal.animal_type} cannot go to this direction. There is a border up!')
                            new_location = f'{row}:{col}'
                            self.animals_locations_after_one_iteration[animal] = new_location
                            continue
                        else:
                            new_location = f'{row - 1}:{col}'

                            if self.terrain_map[row - 1][col].cell_type == 'WATER':
                                self.dead_animals_count += 1
                                print(f'Animal {animal.animal_type} stepped on water.')
                                animal.status = 'dead'
                            self.animals_locations_after_one_iteration[animal] = new_location
                    elif direction == 'down':
                        if row + 1 >= self.x:
                            print(f'{animal.animal_type} cannot go to this direction. There is a border down!')
                            new_location = f'{row}:{col}'
                            self.animals_locations_after_one_iteration[animal] = new_location
                            continue
                        else:
                            new_location = f'{row + 1}:{col}'

                            if self.terrain_map[row + 1][col].cell_type == 'WATER':
                                self.dead_animals_count += 1
                                print(f'Animal {animal.animal_type} stepped on water.')
                                animal.status = 'dead'
                            self.animals_locations_after_one_iteration[animal] = new_location
                    elif direction == 'left':
                        if col - 1 < 0:
                            print(f'{animal.animal_type} cannot go to this direction. There is a border left!')
                            new_location = f'{row}:{col}'
                            self.animals_locations_after_one_iteration[animal] = new_location
                            continue
                        else:

                            new_location = f'{row}:{col - 1}'
                            if self.terrain_map[row][col - 1].cell_type == 'WATER':
                                self.dead_animals_count += 1
                                print(f'Animal {animal.animal_type} stepped on water.')
                                animal.status = 'dead'
                            self.animals_locations_after_one_iteration[animal] = new_location
                    elif direction == 'right':
                        if col + 1 >= self.y:
                            print(f'{animal.animal_type} cannot go to this direction. There is a border right!')
                            new_location = f'{row}:{col}'
                            self.animals_locations_after_one_iteration[animal] = new_location
                            continue
                        else:

                            new_location = f'{row}:{col + 1}'
                            if self.terrain_map[row][col + 1].cell_type == 'WATER':
                                self.dead_animals_count += 1
                                print(f'Animal {animal.animal_type} stepped on water.')
                                animal.status = 'dead'
                            self.animals_locations_after_one_iteration[animal] = new_location

                animal.has_eaten = False
                # self.res = self.animals_locations | self.animals_locations_after_one_iteration
                # print(f'res: {self.res}')

            else:
                animal.hunger_rate -= 1
        self.res = self.animals_locations | self.animals_locations_after_one_iteration
        # print(f'res: {self.res}')
        self.animals_locations = self.res

        for remove_animal in self.animals_keys:
            del self.animals_locations[remove_animal]
        self.animals_keys = []

        self.res = {}


terrain = Terrain(3, 4, 3)

# terrain = Terrain(1, 1, 1)
terrain.create_terrain()
# print(terrain.terrain_map)
terrain.fill_with_animals()
# print(terrain.terrain_map)

# print(terrain.animals_locations)

days = int(input("Enter days count: "))

for day in range(days):
    if not terrain.all_animals_dead:
        terrain.activate_animals()

