import json
from map import Map

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

    def move_to_center(self):
        r, q = self.get_position()
        next_r, next_q = 0, 0
        if r > 0:
            next_r = r - 1
        elif r < 0:
            next_r = r + 1
        else:
            next_r = r

        if q > 0:
            next_q = q - 1
        elif q < 0:
            next_q = q + 1
        else:
            next_q = q

        return next_r, next_q

    def turn(self):
        r, q = self.move_to_center()
        turn = {"action":"move," + str(r) + "," + str(q)}

        return turn

"""
    turn = {
        "action":"move,r,q"
    }
"""