from project.terrain_cell.terrain_cell import TerrainCell


class Desert(TerrainCell):
    def __init__(self, cell_type):
        super().__init__(cell_type)