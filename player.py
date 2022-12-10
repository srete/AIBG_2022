import json
from map import Map
import pickle

class Player:

    def __init__(self, _data, _map:Map) -> None:
        self.data = _data
        self.map = _map

    def update(self, new_data, new_map):
        ''' Updates player atributes'''
        self.data = new_data
        self.map = new_map

    def get_position(self):
        return(self.data["r"], self.data["q"])

    def get_health(self):
        return(self.data["health"])

    def get_power(self):
        return(self.data["power"])

    def get_level(self):
        return(self.data["level"])

    def get_score(self):
        return(self.data["score"])

    def get_trapped(self):
        return(self.data["trapped"])

    def get_trap_duration(self):
        return(self.data["trapDuration"])

    def create_empty_map(self):
        tiles = self.map.tiles
        empty_map = []
        for i, row in enumerate(tiles):
            new_row = []
            for j, tile in enumerate(row):
                new_row.append(0)
            empty_map.append(new_row)

        return empty_map

    def bfs_path(self, i_start, j_start, i_end, j_end, asteroids=False):
        '''Vrsi BFS pretragu i vraca sledeci potez'''
        visited = self.create_empty_map()
        queue = [[(i_start, j_start)]]
        asteroids = []

        delta_i = [0, 1, 1, 0, -1, -1]
        delta_j = [-1, 0, 1, 1, 0, -1]

        while queue:
            path = queue.pop(0)
            i_cur = path[-1][0]
            j_cur = path[-1][1]

            if visited[i_cur][j_cur] == 0:
                for k in range(len(delta_i)):
                    i_next, j_next = i_cur + delta_i[k], j_cur + delta_j[k]
                    if self.is_valid(i_next, j_next, asteroids, asteroids) and visited[i_next][j_next] == 0:
                        new_path = list(path)
                        new_path.append((i_next, j_next))
                        queue.append(new_path)
                    if i_next == i_end and j_next == j_end:
                        path.append((i_end, j_end))
                        return path, asteroids # next move
                visited[i_cur][j_cur] = 1


    def is_valid(self, i, j, n_asteroids, asteroids=False):
        # Provera da li su i,j van mape
        if i < 0 or i > 28 or j < 0:
            return False
        if i <= 14 and j > 14 + i:
            return False
        if i > 14 and j > 42 - i:
            return False
        # Provera dal su opasna
        if asteroids:
            if self.map.get_tile_type(i, j) == "ASTEROID":
                asteroids.append(self.map.tiles[i][j]['entity']['health'])
            if self.map.get_tile_type(i, j) in ["BOSS", "BLACKHOLE"]:
                return False
        else:
            if self.map.get_tile_type(i, j) in ["BOSS", "ASTEROID", "BLACKHOLE"]:
                return False
        return True

    def convert_to_rq(self, i, j):
        return [j - i, i - 14]
    
    def convert_to_ij(self, r, q):
            return q+14, q+r+14

    def turn(self):
        '''Vraca serveru sledecu akciju'''
        r, q = self.get_position()
        i, j = self.convert_to_ij(r, q)
        path, _ = self.bfs_path(i, j, 10, 10)
        path_a, asteroids = self.bfs_path(i, j, 10, 10, True)

        print(asteroids)
        print(len(path))
        print(len(path_a))
        next_i, next_j = 0, 0
        if path < path_a + sum(asteroids)/self.get_power():
            next_i, next_j = path[1]
        else:
            next_i, next_j = path_a[1]
            if self.map.get_tile_type(next_i, next_j) == "ASTEROID":
                next_r, next_q = self.convert_to_rq(next_i, next_j)
                return {"action":"attack,"+str(next_q)+","+str(next_r)}

        next_r, next_q = self.convert_to_rq(next_i, next_j)
        turn = {"action":"move," + str(next_q) + "," + str(next_r)}

        return turn
    
    def tiles_distance(self, a: dict, b: dict) -> float:
        return (abs(a['q'] - b['q']) 
            + abs(a['q'] + a['r'] - b['q'] - b['r'])
            + abs(a['r'] - b['r'])) / 2
            
    def get_zone(self) -> int:
        '''
        Prva: 2-4, Druga 5-10, Treca 11-14
        '''  
        # {'r': 0, 'q': 0}
        r, q = self.get_position()
        dist = self.tiles_distance({'r': 0, 'q': 0}, {'r': r, 'q': q})
        if dist >= 2 and dist <= 4:
            return 1
        if dist >= 5 and dist <= 10:
            return 2
        if dist >= 11 and dist <= 14:
            return 3
        else:
            return None


"""
    turn = {
        "action":"move,q,r"
    }
"""

if __name__ == "__main__":
    with open('game_state.json', 'r') as f:
        game_state = json.load(f)
    with open('map.json', 'r') as f:
        map_data = json.load(f)
    map = Map(map_data)
    player = Player(game_state['gameState']['player1'], map)

    #print(player.create_empty_map())
    print(player.bfs_path(0, 0, 0, 5))
