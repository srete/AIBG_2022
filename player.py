import json
from map import Map
import pickle
from BOSS import Boss
from NPC import Npc

class Player:

    def __init__(self, _data, _map: Map, _boss: Boss, _other_players: list) -> None:
            self.data = _data
            self.map = _map
            self.boss = _boss
            self.other_players =_other_players

    def update(self, new_data, new_map):
        ''' Updates player atributes'''
        self.data = new_data
        self.map = new_map

    def get_position(self):
        return(self.data["q"], self.data["r"])

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

    def convert_to_qr(self, i, j):
        '''return q, r'''
        return (j-i, i - 14) if i <= 14 else (j-14, i-14)
    
    def convert_to_ij(self, r, q):
            ''' return i, j '''
            return (r+14, q+r+14) if r<=0 else (r+14 ,q+14)

    def turn(self):
        '''Vraca serveru sledecu akciju'''
        q, r = self.get_position()
        i, j = self.convert_to_ij(r, q)
        path, _ = self.bfs_path(i, j, 10, 10)
        path_a, asteroids = self.bfs_path(i, j, 10, 10, True)

        print(asteroids)
        #print(len(path))
        #print(len(path_a))
        next_i, next_j = 0, 0
        if len(path) < len(path_a) + sum(asteroids)/self.get_power():
            next_i, next_j = path[1]
        else:
            next_i, next_j = path_a[1]
            if self.map.get_tile_type(next_i, next_j) == "ASTEROID":
                next_q, next_r = self.convert_to_qr(next_i, next_j)
                return {"action":"attack,"+str(next_q)+","+str(next_r)}

        next_q, next_r = self.convert_to_qr(next_i, next_j)
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
        q, r = self.get_position()
        dist = self.tiles_distance({'r': 0, 'q': 0}, {'r': r, 'q': q})
        if dist >= 2 and dist <= 4:
            return 1
        if dist >= 5 and dist <= 10:
            return 2
        if dist >= 11 and dist <= 14:
            return 3
        else:
            return None

    def next_move(self):
        zone_5 = [{"q": 5, "r": 0}, {"q": 5, "r": -1}, {"q": 5, "r": -2}, {"q": 5, "r": -3}, {"q": 5, "r": -4},
                  {"q": 5, "r": -5}, {"q": 4, "r": -5}, {"q": 3, "r": -5}, {"q": 2, "r": -5},
                  {"q": 1, "r": -5}, {"q": 0, "r": -5}, {"q": -1, "r": -4}, {"q": -2, "r": -3}, {"q": -3, "r": -2},
                  {"q": -4, "r": -1}, {"q": -5, "r": 0}, {"q": -5, "r": 1}, {"q": -5, "r": 2}, {"q": -5, "r": 3},
                  {"q": -5, "r": 4}
            , {"q": -5, "r": 5}, {"q": -4, "r": 5}, {"q": -3, "r": 5}, {"q": -2, "r": 5}, {"q": -1, "r": 5},
                  {"q": 0, "r": 5}, {"q": 1, "r": 4}, {"q": 2, "r": 3}, {"q": 3, "r": 2}, {"q": 4, "r": 1}]

        wormholes = self.map.get_all_tiles_type("WORMHOLE")
        xp = self.map.get_all_tiles_type("EXPERIENCE")
        health = self.map.get_all_tiles_type("HEALTH")
        black_holes = self.map.get_all_tiles_type("BLACK HOLE")

        attack_of_boss = self.boss.boss_next_attack()

        for dic in self.boss.position:
            if (self.tiles_distance(self.data, dic) <= 3):
                return {"action": "attack," + str(dic["q"]) + "," + str(dic["r"])}

        zero_position = {"q": 0, "r": 0}

        if (self.tiles_distance(self.data, zero_position) == 5 and self.get_health() > 250):
            path = self.bfs_path(self.convert_to_ij(self.data["r"], self.data["q"]), self.convert_to_ij(0, 0))
            q, r = self.convert_to_qr(path[1][0], path[1][1])
            return {"action": "move" + str(q) + "," + str(r)}

        if (self.tiles_distance(self.data, zero_position) == 5 and self.get_health() < 250):
            distances = []

            for player in self.other_players:
                if ((self.tiles_distance(self.data, player) <= 3) and (self.get_health() > player.get_health())):
                    return {"action": "attack" + str(player["q"]) + "," + str(player["r"])}

            for i in range(len(health)):
                if ((health[i]["q"], health[i]["r"]) not in attack_of_boss):
                    distances.append(self.tiles_distance(self.data, health[i]))
                    min = distances[0]
                    j = 0
                    for i in range(1, len(distances)):
                        if (min > distances[i]):
                            j = i
                            min = distances[i]

                    path = self.bfs_path(self.convert_to_ij(self.data["r"], self.data["q"]),
                                         self.convert_to_ij(health[j]["r"], health[j]["q"]))
                    q, r = self.convert_to_qr(path[1][0], path[1][1])
                    return {"action": "move" + str(q) + "," + str(r)}

        for player in self.other_players:
            if ((self.tiles_distance(self.data, player) <= 4) and (player.get_trap_duration() == 2)):
                path = self.bfs_path(self.convert_to_ij(self.data["r"], self.data["q"]),
                                     self.convert_to_ij(player["r"], player["q"]))
                q, r = self.convert_to_qr(path[1][0], path[1][1])
                return {"action": "move" + str(q) + "," + str(r)}

            if (self.tiles_distance(self.data, player) <= 3):
                return {"action": "attack" + str(player["q"]) + str(player["r"])}

            if ((self.tiles_distance(self.data, player)) <= 5 and player.get_health() + 300 <= self.get_health()):
                if ((player["q"], player["r"]) not in attack_of_boss):
                    path = self.bfs_path(self.convert_to_ij(self.data["r"], self.data["q"]),
                                         self.convert_to_ij(player["r"], player["q"]))
                    q, r = self.convert_to_qr(path[1][0], path[1][1])
                    return {"action": "move" + str(q) + "," + str(r)}

        # proveravanje za wormhole
        flag = 0
        for i in range(len(wormholes)):
            dic = {"q": wormholes[i]["q"], "r": wormholes[i]["r"]}
            if (self.tiles_distance(self.data, dic) <= 2):
                for j in range(i + 1, len(wormholes)):
                    if (wormholes[i]["id"] == wormholes[j]["id"]):
                        for k in zone_5:
                            dic1 = {"q": wormholes[j]["q"], "r": wormholes[j]["r"]}
                            if ((self.tiles_distance(dic1, zone_5) <= 3) and (
                                    (dic1["q"], dic1["r"]) not in attack_of_boss)):
                                flag = 1
                                break
                    if (flag):
                        path = self.bfs_path(self.convert_to_ij(self.data["r"], self.data["q"]),
                                             self.convert_to_ij(wormholes[i]["r"], wormholes[i]["q"]))
                        q, r = self.convert_to_qr(path[1][0], path[1][1])
                        return {"action": "move" + str(q) + "," + str(r)}

        distances = []
        for i in range(len(zone_5)):
            distances.append(self.tiles_distance(self.data, zone_5[i]))
        min_distance = distances[0]
        min_idx = 0
        for i in range(1, len(distances)):
            if (min_distance > distances[i]):
                min_idx = i
                min_distance = distances[i]
        path = self.bfs_path(self.convert_to_ij(self.data["r"], self.data["q"]),
                             self.convert_to_ij(zone_5[min_idx]["r"], zone_5[min_idx]["q"]))
        q, r = self.convert_to_qr(path[1][0], path[1][1])
        
        if ((r, q) not in attack_of_boss):
            pass

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
