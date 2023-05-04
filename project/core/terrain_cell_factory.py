from project.animal.carnivore import Carnivore
from project.animal.herbivore import Herbivore
from project.animal.scavenger import Scavenger
from project.terrain_cell.desert import Desert
from project.terrain_cell.grass import Grass
from project.terrain_cell.mountain import Mountain
from project.terrain_cell.water import Water


class TerrainCellFactory:
    terrain_cell_types = {
        'WATER': Water,
        'DESERT': Desert,
        'MOUNTAIN': Mountain,
        'GRASS': Grass,
    }

    def create_terrain_cell(self, cell_type):
        # print(cell_type)
        return self.__class__.terrain_cell_types[cell_type](cell_type)
