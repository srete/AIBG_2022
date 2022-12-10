import json
from map import Map
import pickle

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

    def move_to_center(self):
        r, q = self.get_position()
        next_r, next_q = r, q+1

        return next_r, next_q

    def turn(self):
        r, q = self.move_to_center()
        turn = {"action":"move," + str(r) + "," + str(q)}

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
        


if __name__ == "__main__":
    with open('generated_game_state.pkl', 'rb') as f:
        game_state = pickle.load(f)
        game_state = json.loads(game_state['gameState'])
        game_state = {'gameState': game_state}

        data = game_state['gameState']['player1']
        map = game_state['gameState']['map']
        player = Player(data, map)
        print(player.get_zone())
        print(player.get_position())

"""
    turn = {
        "action":"move,r,q"
    }
"""