import requests
import json

import player
import map
import NPC

# Funkcija koja igra igru

SERVER_IP = "http://aibg22.com:"
username = "Hiperparametri"
password = "#@YyRQt3Fk"

login_data = {
    'username' : username,
    'password' : password
}

class Server:
    '''
    Atributi:
    * token
    * join_game
    * Player player
    * NPC npcs
    * Map map
    * Boss boss
    '''
    def __init__(self, map_name:str, _player_id:int, time:int) -> None:
        '''
        * player_id: id pocetne pozicije 
        * time - trajanje igre u minutima
        '''
        self.__game_init__(map_name, _player_id, time)
        # Prva akcija
        # TODO: Samo za train slucaj, promeniti za pravu igru
        action_0 = {
            "action":"move,-7,-6"
        }
        start_action_r  = requests.post(url =SERVER_IP + "8081"+"/game/actionTrain",headers = self.token_header, json = action_0)
        #print(start_action_r.json())
        start_action = json.loads(start_action_r.json()['gameState'])  # formatiranje
        
        # TODO: Inicijalizuj mapu, Playera itd.... smisleno za pravu igru
        self.map = map.Map(start_action['map'])
        self.player = player.Player(start_action[f'player{self.player_id}'], self.map)  # Nas player, tj. pobednik :)
        self.npc = {str(idx): NPC.Npc({}) for idx in self.npc_ids} # Gubitniciii
        for idx, p in self.npc.items():
            p.update(start_action[f'player{idx}'])

    def __game_init__(self,  map_name: str, _player_id: int, time: int):
        # Inicijalizacija igre
        self.player_id = _player_id  # TODO: promeni za pravu igru
        self.npc_ids = [i for i in range(1, 5) if i != self.player_id]
        token = requests.post(url =  SERVER_IP+"8081"+"/user/login",json = login_data).json()
        self.token_header = {
            'Authorization' : 'Bearer ' + token["token"]
        }
        g_params = {
            'mapName': map_name,
            "playerIdx": str(_player_id) ,
            "time": str(time)
            }
            
        self.join_game = requests.post(url =SERVER_IP +"8081" +"/game/train", headers = self.token_header, json = g_params)
        print(self.join_game.json())

    def get_state(self) -> None:
        turn = self.player.turn()
        # turn = {
        #     "action":"move,-7,-7"
        # }
    
        new_state_r = requests.post(url =SERVER_IP + "8081"+"/game/actionTrain", headers = self.token_header, json = turn)
        print('Staaa', new_state_r.json())
        new_state = json.loads(new_state_r.json()['gameState'])  # formatiranje
        
        # Update mape, playera, NPCa i Boss-a
        self.map.update(new_state['map'])
        self.player.update(new_state[f'player{self.player_id}'], self.map)
        for idx, p in self.npc.items():
            p.update(new_state[f'player{idx}'])

if __name__ == "__main__":
    server = Server('test1.txt', 1, 1)
    server.get_state()
    
    def play_game(self):
        while(True):
            self.get_state()
    


server = Server('test1.txt', 1, 1)
#server.get_state()
server.play_game()


#### Try except da stampa greske