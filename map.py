import json

class Map:
    def __init__(self, _data) -> None:
        self.tiles = _data["tiles"]
        self.size = data["size"]
        self.types_to_coords = {}
    
    def update(self, data):
        self.tiles = data["tiles"]
        self.size = data["size"]
        self.load_tiles()

    def load_tiles(self):
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                tile_type = tile['entity']['type']
                append_data = self.convert_to_rq(i, j)
                if tile_type == "WORMHOLE":
                    append_data.append(tile['entity']['id'])
                if tile_type in self.types_to_coords:
                    self.types_to_coords[tile_type].append(append_data)
                else:
                    self.types_to_coords[tile_type] = [append_data]


    def get_all_tiles_type(self, type):
        return self.types_to_coords[type]

    def convert_to_rq(self, i, j):
        return [i - 14, j - i]

    def get_tile_type(self, r, q):
        start_r = r + 14
        start_q = -(14+r)
        tile = self.tiles[start_r][q-start_q]

        return tile['tileType']


if __name__ == "__main__":
    with open('map.json') as json_file:
        data = json.load(json_file)
    map = Map(data)
    map.load_tiles()
    print(map.types_to_coords.keys())
    print(map.types_to_coords['HEALTH'])