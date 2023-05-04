import random
from unittest import TestCase, main

from project.animal.carnivore import Carnivore
from project.animal.herbivore import Herbivore
from project.animal.scavenger import Scavenger
from project.terrain import Terrain
from project.terrain_cell.grass import Grass
from project.terrain_cell.mountain import Mountain
from project.terrain_cell.water import Water


class TerrainTests(TestCase):

    def setUp(self) -> None:
        self.x = 4
        self.y = 4
        self.animals_count = 7
        self.terrain = Terrain(self.x, self.y, self.animals_count)

    def test_terrain_init(self):
        x = 4
        y = 4
        animals_count = 7
        terrain = Terrain(x, y, animals_count)

        self.assertEqual(x, terrain.x)
        self.assertEqual(y, terrain.y)
        self.assertEqual(animals_count, terrain.animals_count)

        self.assertEqual([], terrain.terrain_map)
        self.assertEqual({}, terrain.animals_locations)
        self.assertEqual([], terrain.animals_locations_after_hunger_games)
        self.assertEqual({}, terrain.res)
        self.assertEqual([], terrain.animals_keys)
        self.assertEqual(0, terrain.dead_animals_count)
        self.assertEqual(False, terrain.all_animals_dead)
        self.assertEqual({}, terrain.animals_locations_after_one_iteration)
        self.assertEqual('AnimalFactory', terrain.animal_factory.__class__.__name__)
        self.assertEqual('TerrainCellFactory', terrain.terrain_cell_factory.__class__.__name__)

    def test_terrain_create_terrain_correct_size(self):
        action = self.terrain.create_terrain()
        x = len(self.terrain.terrain_map[0])
        y = len(self.terrain.terrain_map)

        size = x * y

        self.assertEqual(16, size)

    def test_terrain_create_terrain_correct_terrain_cell_type(self):
        correct_types = ['GRASS', 'WATER', 'MOUNTAIN', 'DESERT']

        action = self.terrain.create_terrain()
        rand_x = random.randint(0, self.x - 1)
        rand_y = random.randint(0, self.y - 1)

        result = self.terrain.terrain_map[rand_x][rand_y].cell_type

        self.assertTrue(result in correct_types)

    def test_terrain_fill_with_animals_correct_animal_type(self):
        correct_animal_types = ['Carnivore', 'Herbivore', 'Scavenger']

        self.terrain.create_terrain()
        self.terrain.fill_with_animals()

        for animal in self.terrain.animals_locations:
            self.assertTrue(animal.animal_type in correct_animal_types)

    def test_terrain_fill_with_animals_correct_animals_count_on_map(self):
        self.terrain.create_terrain()
        self.terrain.fill_with_animals()

        total_count_animals = 0
        for animal in self.terrain.animals_locations:
            total_count_animals += 1

        self.assertEqual(7, total_count_animals)

    def test_terrain_fill_with_animals_animal_dead_if_stepped_on_water(self):

        self.x = 1
        self.y = 1
        self.animals_count = 1

        self.terrain = Terrain(self.x, self.y, self.animals_count)

        self.terrain.create_terrain()
        self.terrain.terrain_map[0][0] = Water('WATER')

        self.terrain.fill_with_animals()

        for animal in self.terrain.animals_locations:
            self.assertEqual('dead', animal.status)

    def test_terrain_activate_animals_check_all_animals_dead_returns_true(self):
        self.terrain.create_terrain()
        self.terrain.fill_with_animals()

        for animal in self.terrain.animals_locations:
            animal.status = 'dead'

        self.assertTrue(True, self.terrain.all_animals_dead)

    def test_terrain_activate_animals_animal_hunger_rate_decrement_after_one_iteration_when_hunger_rate_bigger_than_or_equal_five(self):
        self.terrain.create_terrain()
        self.terrain.fill_with_animals()

        for animal in self.terrain.animals_locations:
            self.assertEqual(10, animal.hunger_rate)

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:
            self.assertEqual(9, animal.hunger_rate)

    def test_terrain_activate_animals_animal_type_herbivore_terrain_cell_different_than_grass_hunger_rate_decrement(self):
        self.terrain.terrain_map = [[Mountain('MOUNTAIN'), ], ]
        self.terrain.animals_locations = {Herbivore(): '0:0'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 4

            self.terrain.activate_animals()

            self.assertEqual(3, animal.hunger_rate)

    def test_terrain_activate_animals_animal_type_herbivore_animal_dies_when_hunger_rate_is_zero(self):
        self.terrain.terrain_map = [[Mountain('MOUNTAIN'), ], ]
        self.terrain.animals_locations = {Herbivore(): '0:0'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 1

            self.terrain.activate_animals()

            self.assertEqual('dead', animal.status)

    def test_terrain_activate_animals_animal_type_herbivore_animal_dies_dead_animals_count_increment(self):
        self.terrain.terrain_map = [[Mountain('MOUNTAIN'), ], ]
        self.terrain.animals_locations = {Herbivore(): '0:0'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 1

            self.terrain.activate_animals()

            self.assertEqual(1, self.terrain.dead_animals_count)

    def test_terrain_activate_animals_terrain_cell_type_equal_to_grass_herbivore_has_eaten_increment_hunger_rate(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Herbivore(): '0:0'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 2

            self.assertEqual(2, animal.hunger_rate)

            self.terrain.activate_animals()

            self.assertEqual(3, animal.hunger_rate)

    def test_terrain_activate_animals_carnivore_carnivore_in_same_cell_no_animal_is_eaten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Carnivore(): '0:0', Carnivore(): '0:0'}

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 2

        for check_animal in self.terrain.animals_locations:
            self.assertEqual('alive', check_animal.status)
            self.assertEqual(False, check_animal.is_eaten)
            self.assertEqual(False, check_animal.has_eaten)

    def test_terrain_activate_animals_carnivore_herbivore_in_same_cell_herbivore_is_eaten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Carnivore(): '0:0', Herbivore(): '0:0'}

        for i in self.terrain.animals_locations:
            i.hunger_rate = 2

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:

            if animal.__class__.__name__ == 'Herbivore':
                self.assertEqual(True, animal.is_eaten)
                self.assertEqual('dead', animal.status)
                self.assertEqual(1, self.terrain.dead_animals_count)

            elif animal.__class__.__name__ == 'Carnivore':
                self.assertEqual('alive', animal.status)
                self.assertEqual(3, animal.hunger_rate)

    def test_terrain_activate_animals_carnivore_more_than_one_herbivore_in_same_cell_herbivores_are_eaten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Carnivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0'}

        for i in self.terrain.animals_locations:
            i.hunger_rate = 2

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:

            if animal.__class__.__name__ == 'Herbivore':
                self.assertEqual(True, animal.is_eaten)
                self.assertEqual('dead', animal.status)
                self.assertEqual(2, self.terrain.dead_animals_count)

            elif animal.__class__.__name__ == 'Carnivore':
                print(animal.hunger_rate)
                self.assertEqual('alive', animal.status)
                self.assertEqual(4, animal.hunger_rate)

    def test_terrain_activate_animals_carnivore_hunger_rate_cannot_be_more_than_ten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Carnivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0'}

        for i in self.terrain.animals_locations:
            i.hunger_rate = 4

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:
            self.assertEqual(10, animal.hunger_rate)

    def test_terrain_activate_animals_carnivore_scavenger_in_same_cell_scavenger_is_eaten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Carnivore(): '0:0', Scavenger(): '0:0'}

        for i in self.terrain.animals_locations:
            i.hunger_rate = 2

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:

            if animal.__class__.__name__ == 'Scavenger':
                self.assertEqual(True, animal.is_eaten)
                self.assertEqual('dead', animal.status)
                self.assertEqual(1, self.terrain.dead_animals_count)

            elif animal.__class__.__name__ == 'Carnivore':
                self.assertEqual('alive', animal.status)
                self.assertEqual(3, animal.hunger_rate)

    def test_terrain_activate_animals_carnivore_more_than_one_scavenger_in_same_cell_scavengers_are_eaten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Carnivore(): '0:0', Scavenger(): '0:0', Scavenger(): '0:0'}

        for i in self.terrain.animals_locations:
            i.hunger_rate = 2

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:

            if animal.__class__.__name__ == 'Scavenger':
                self.assertEqual(True, animal.is_eaten)
                self.assertEqual('dead', animal.status)
                self.assertEqual(2, self.terrain.dead_animals_count)

            elif animal.__class__.__name__ == 'Carnivore':
                # print(animal.hunger_rate)
                self.assertEqual('alive', animal.status)
                self.assertEqual(4, animal.hunger_rate)

    def test_terrain_activate_animals_scavenger_scavenger_in_same_cell_no_animal_is_eaten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Scavenger(): '0:0', Scavenger(): '0:0'}

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 2

        for check_animal in self.terrain.animals_locations:
            self.assertEqual('alive', check_animal.status)
            self.assertEqual(False, check_animal.is_eaten)
            self.assertEqual(False, check_animal.has_eaten)

    def test_terrain_activate_animals_scavenger_eats_dead_animal(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Scavenger(): '0:0', Herbivore(): '0:0'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 4

            if animal.__class__.__name__ == 'Herbivore':
                animal.status = 'dead'

        self.terrain.activate_animals()

        for assert_animal in self.terrain.animals_locations:
            if assert_animal.__class__.__name__ == 'Scavenger':
                self.assertEqual(5, assert_animal.hunger_rate)

    def test_terrain_active_animals_scavenger_does_not_eat_alive_animal(self):
        self.x = 1
        self.y = 1
        self.animals_count = 2

        self.terrain = Terrain(self.x, self.y, self.animals_count)

        self.terrain.create_terrain()

        for terrain_cell in self.terrain.terrain_map:
            terrain_cell = Grass('GRASS')
            # print(terrain_cell)

        self.terrain.animals_locations = {Scavenger(): '0:0', Herbivore(): '0:0'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 2

        self.terrain.activate_animals()

        for assert_animal in self.terrain.animals_locations:
            if assert_animal.__class__.__name__ == 'Scavenger':
                self.assertEqual(1, assert_animal.hunger_rate)

    def test_terrain_activate_animals_scavenger_hunger_rate_cannot_be_more_than_ten(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Scavenger(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0', Herbivore(): '0:0'}

        for animal in self.terrain.animals_locations:

            animal.hunger_rate = 4

            if animal.__class__.__name__ == 'Herbivore':
                animal.status = 'dead'

        self.terrain.activate_animals()

        for animal in self.terrain.animals_locations:
            self.assertEqual(10, animal.hunger_rate)

    def test_terrain_animal_hunger_rate_equal_to_zero_animal_dead(self):
        self.terrain.terrain_map = [[Grass('GRASS'), ], ]
        self.terrain.animals_locations = {Scavenger(): '0:0'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 0

        self.terrain.activate_animals()

        for assert_animal in self.terrain.animals_locations:
            self.assertEqual('dead', assert_animal.status)
            self.assertEqual(1, self.terrain.dead_animals_count)

    def test_terrain_direction_there_is_border_animals_does_not_move(self):
        self.x = 1
        self.y = 1
        self.animals_count = 1

        self.terrain = Terrain(self.x, self.y, self.animals_count)

        self.terrain.create_terrain()

        for terrain_cell in self.terrain.terrain_map:
            terrain_cell = Grass('GRASS')

        self.terrain.animals_locations = {Scavenger(): '0:0'}

        self.terrain.activate_animals()

        location = list(self.terrain.animals_locations.values())[0]

        self.assertEqual('0:0', location)

    def test_terrain_animal_does_not_eat_makes_a_move(self):
        self.x = 3
        self.y = 3
        self.animals_count = 1

        self.terrain = Terrain(self.x, self.y, self.animals_count)

        self.terrain.create_terrain()
        # print(self.terrain.terrain_map)

        for terrain_cell in self.terrain.terrain_map:
            terrain_cell = Grass('GRASS')

        # print(self.terrain.terrain_map)
        self.terrain.animals_locations = {Scavenger(): '1:1'}

        for animal in self.terrain.animals_locations:
            animal.hunger_rate = 3

        self.terrain.activate_animals()

        location = list(self.terrain.animals_locations.values())[0]

        self.assertNotEqual('1:1', location)


if __name__ == '__main__':
    main()