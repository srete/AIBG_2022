import json

class Npc:
    def __init__(self, npc) -> None:
        self.npc = npc

    def update(self, npc):
        self.npc = npc

    def get_position(self):
        return(self.npc["q"], self.npc["r"])

    def get_health(self):
        return(self.npc["health"])

    def get_power(self):
        return(self.npc["power"])

    def get_level(self):
        return(self.npc["level"])

    def get_score(self):
        return(self.npc["score"])

    def get_trapped(self):
        return(self.npc["trapped"])

    def get_trap_duration(self):
        return(self.npc["trapDuration"])