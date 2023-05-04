from project.terrain_cell.terrain_cell import TerrainCell


class Mountain(TerrainCell):
    def __init__(self, cell_type):
        super().__init__(cell_type)