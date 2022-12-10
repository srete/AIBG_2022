import json
import pickle

class Boss:

    def __init__(self, boss):

        self.boss = boss
        self.position = [{"q":0, "r":0}, {"q":0, "r":-1}, {"q":1, "r":-1}, {"q":-1, "r":0}, {"q":1, "r":0}, {"q":-1, "r":1}, {"q":0, "r":1}]
        self.state_of_pattern1 = 0
        self.state_of_pattern2 = 0

        self.number_of_attacks = 0
        self.last_attack = 0 #nijedan napad bosa se do sada nije desio

    def update_boss(self, boss):
        self.boss = boss

        if (self.number_of_attacks != 0):
            self.number_of_attacks += 1


        if (len(self.boss["bossAttackedTiles"]) == 8):
            for dic in self.boss["bossAttackedTiles"]:

                if((dic["q"] == 8) and (dic["r"] == -2)):
                    self.state_of_pattern1 = 1
                    self.number_of_attacks = 0

                if ((dic["q"] == 8) and (dic["r"] == -4)):
                    self.state_of_pattern1 = 2
                    self.number_of_attacks = 0

                if((dic["q"] == 8) and (dic["r"] == -6)):
                    self.state_of_pattern1 = 3
                    self.number_of_attacks = 1
                    self.last_attack = 1
        else:
            for dic in self.boss["bossAttackedTiles"]:
                if ((dic["q"] == 6) and (dic["r"] == 0)):
                    self.state_of_pattern2 = 1
                    self.number_of_attacks = 1
                    self.last_attack = 2
                    break

                if((dic["q"] == 8) and (dic["r"] == 0)):
                    self.pattern2 = True
                    self.state_of_pattern2 = 2
                    self.number_of_attacks = 1
                    self.last_attack = 2
                    break


                if((dic["q"] == 10) and (dic["r"] == 0)):
                    self.pattern2 = True
                    self.state_of_pattern2 = 3
                    self.number_of_attacks = 1
                    self.last_attack = 2
                    break

    def boss_next_attack(self):

        if (self.state_of_pattern1 == 1):
            return [(8, -4), (8, -5), (4, 4), (3, 5), (-3, -5), (-4, -4), (-8, 4), (-8, 5)]

        if (self.state_of_pattern1 == 2):
            return[(8, -6), (8, -7), (2, 6), (1, 7), (-1, -7), (-2, -6), (-8, 6), (-8, 7)]

        if (self.state_of_pattern1 == 3):

            self.state_of_pattern1 = 0

            if(self.state_of_pattern2 == 1):
                index = []
                for j in range(0, -9, -1):
                    index.append((8, j))
                for j in range(7, -1, -1):
                    index.append((j, -8))
                for j in range(0, 9):
                    index.append((-8, j))
                for j in range(-7, 1):
                    index.append((8, j))

                for i in range(-8, 8):
                    for j in range(-8, 8):
                        if ((abs(i) + abs(j) == 8) and ((i < 0 and j < 0) or (i > 0 and j > 0) and (abs(i) != 8))):
                            index.append((i, j))


            if(self.state_of_pattern2 == 2):
                index = []
                for j in range(0, -11, -1):
                    index.append((10, j))
                for j in range(9, -1, -1):
                    index.append((j, -10))
                for j in range(0, 11):
                    index.append((-10, j))
                for j in range(-9, 1):
                    index.append((10, j))

                for i in range(-10, 10):
                    for j in range(-10, 10):
                        if ((abs(i) + abs(j) == 10) and ((i < 0 and j < 0) or (i > 0 and j > 0) and (abs(i) != 10))):
                            index.append((i, j))

            if(self.state_of_pattern2 == 3 or self.state_of_pattern2 == 0):
                index = []
                for j in range(0, -7, -1):
                    index.append((6, j))
                for j in range(5, -1, -1):
                    index.append((j, -6))
                for j in range(0, 7):
                    index.append((-6, j))
                for j in range(-5, 1):
                    index.append((6, j))

                for i in range(-6, 6):
                    for j in range(-6, 6):
                        if ((abs(i) + abs(j) == 6) and ((i < 0 and j < 0) or (i > 0 and j > 0) and (abs(i) != 6))):
                            index.append((i, j))
            return index

        if (self.state_of_pattern2 == 1):
            return [(8, -3), (8, -2), (6, 2), (5, 3), (-5, -3), (-6, -2), (-8, 3), (-8, 2)]

        if (self.state_of_pattern2 == 2):
            return [(8, -3), (8, -2), (6, 2), (5, 3), (-5, -3), (-6, -2), (-8, 3), (-8, 2)]

        if (self.state_of_pattern2 == 3):
            return [(8, -3), (8, -2), (6, 2), (5, 3), (-5, -3), (-6, -2), (-8, 3), (-8, 2)]


#with open('boss.json') as json_file:
#    boss = json.load(json_file)

if __name__ == "__main__":

    with open('generated_game_state.pkl', 'rb') as f:
        game_state = pickle.load(f)
        game_state = json.loads(game_state['gameState'])
        game_state = {'gameState': game_state}


        boss = game_state["gameState"]["boss"]
        print(boss)
        #print(len(boss["bossAttackedTiles"]))
        boss1 = Boss(boss)
        #print(boss1)

        #print(boss1.pattern2)
        #print(boss1.state_of_pattern)

        # for dic in boss["bossAttackedTiles"]:
        #     if(dic["q"] == 1 and dic["r"] == -6):
        #         print("aaa")
