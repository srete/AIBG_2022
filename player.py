import json
from map import Map

class Player:

    def __init__(self, _data, _map:Map) -> None:
        self.data = _data
        self.map = _map

    def update_player(self, new_data, new_map):
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

    def bfs(self, i_start, j_start, i_end, j_end):
        '''NOT IN USE'''
        visited = self.create_empty_map()
        parent_map = {}

        queue = []
        queue.append([i_start, j_start])

        visited[i_start][j_start] = 1
        delta_i = [0, 1, 1, 0, -1, -1]
        delta_j = [-1, 0, 1, 1, 0, -1]
        while queue:

            pos = queue.pop(0)
            i_cur, j_cur = pos[0], pos[1]

            for k in range(len(delta_i)):
                i_next, j_next = i_cur + delta_i[k], j_cur + delta_j[k]
                if i_next == i_end and j_next == j_end:
                    parent_map[str(i_next)+str(j_next)] = [i_cur, j_cur]
                    self.print_path(parent_map, i_end, j_end, i_start, j_start)
                    return
                if self.is_valid(i_next, j_next) and visited[i_next][j_next]==0:
                    queue.append([i_next, j_next])
                    parent_map[str(i_next)+str(j_next)] = [i_cur, j_cur]
                    visited[i_next][j_next] = 1
    
    def bfs_path(self, i_start, j_start, i_end, j_end):
        visited = self.create_empty_map()
        queue = [[(i_start, j_start)]]

        delta_i = [0, 1, 1, 0, -1, -1]
        delta_j = [-1, 0, 1, 1, 0, -1]

        while queue:
            path = queue.pop(0)
            i_cur = path[-1][0]
            j_cur = path[-1][1]

            if visited[i_cur][j_cur] == 0:
                for k in range(len(delta_i)):
                    i_next, j_next = i_cur + delta_i[k], j_cur + delta_j[k]
                    if self.is_valid(i_next, j_next) and visited[i_next][j_next] == 0:
                        new_path = list(path)
                        new_path.append((i_next, j_next))
                        queue.append(new_path)
                    if i_next == i_end and j_next == j_end:
                        print(path)
                        return 
                visited[i_cur][j_cur] = 1

    def print_path(self, parent_map, i_end, j_end, i_start, j_start):
        '''NOT IN USE'''
        curr = [i_end, j_end]
        while (curr != None):
            print(curr)
            if curr[0] == i_start and curr[1] == j_start:
                return
            curr = parent_map[str(curr[0]) + str(curr[1])]

    def is_valid(self, i, j):
        # Provera da li su i,j van mape
        if i < 0 or i > 28 or j < 0:
            return False
        if i <= 14 and j > 14 + i:
            return False
        if i > 14 and j > 42 - i:
            return False
        # Provera dal su opasna
        if self.map.get_tile_type(i, j) in ["BOSS", "ASTEROID", "BLACKHOLE"]:
            return False
        return True
        

    def turn(self):
        i_end, j_end = 0, 0
        r, q = self.get_position()
        i, j = self.convert_to_ij(r, q)
        next_r, next_q = self.convert_to_rq(self.bfs(i, j, i_end, j_end))
        turn = {"action":"move," + str(next_r) + "," + str(next_q)}

        return turn

    def convert_to_ij(r, q):
        return [r+14, q+r+14]

    def convert_to_rq(self, i, j):
        return [i - 14, j - i]

"""
    turn = {
        "action":"move,r,q"
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
    print(map.get_tile_type(26, 10))
    player.bfs_path(7, 6, 3, 7)
