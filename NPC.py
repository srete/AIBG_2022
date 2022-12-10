import json

class Npc:

    def update_npc(self, npc):
        self.npc = npc

    def get_position(self):
        return(self.npc["r"], self.npc["q"])

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


with open('player2.json') as json_file:
    player2 = json.load(json_file)

with open('player3.json') as json_file:
    player3 = json.load(json_file)

with open('player4.json') as json_file:
    player4 = json.load(json_file)


npc = Npc()
npc.update_npc(player2)
print(npc.get_trapped())
