import json

class Map:
    def __init__(self, _data) -> None:
        self.tiles = _data["tiles"]
        self.size = _data["size"]
        self.types_to_coords = {}
    
    def update(self, data):
        self.tiles = data["tiles"]
        self.size = data["size"]
        self.load_tiles()

    def load_tiles(self):
        ''' Pravi dict po tipovima polja'''
        # TODO: Da li je skupo vremenski?
        
        self.types_to_coords = {}
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                tile_type = tile['entity']['type']
                q, r = self.convert_to_qr(i, j)
                append_data = {'q': q, 'r': r}
                if tile_type == "WORMHOLE":
                    append_data['id'] = tile['entity']['id']
                    #append_data.append(tile['entity']['id'])
                if tile_type in self.types_to_coords:
                    self.types_to_coords[tile_type].append(append_data)
                else:
                    self.types_to_coords[tile_type] = [append_data]


    def get_all_tiles_type(self, type):
        return self.types_to_coords[type]

    def convert_to_rq(self, i, j):
        return [j - i, i - 14]

    def get_tile_type(self, i, j):
        ''' Ne sluzi nicemu za sad '''
        tile = self.tiles[i][j]

        return tile['entity']['type']


if __name__ == "__main__":
    with open('map.json') as json_file:
        data = json.load(json_file)
    map = Map(data)
    map.load_tiles()
    print(map.types_to_coords.keys())
    print(map.types_to_coords['HEALTH'])