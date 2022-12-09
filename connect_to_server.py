import requests
import json
import pickle

SERVER_IP = "http://aibg22.com:"
username = "Hiperparametri"
password = "#@YyRQt3Fk"


login_data = {
    'username' : username,
    'password' : password
}
token = requests.post(url =  SERVER_IP+"8081"+"/user/login",json = login_data).json()

header_g = {
    'Authorization' : 'Bearer ' + token["token"]
}
g_params ={
    'mapName':"test1.txt",
    "playerIdx":"1" ,
    "time":"10"}
    
join_game = requests.post(url =SERVER_IP +"8081" +"/game/train",headers = header_g,json = g_params)


# TEST AKCIJA: MOVE SA POLJA (-7,-7) na polje (-7,-6)
action_0 = {
    "action":"move,-7,-6"
}
start_action  = requests.post(url =SERVER_IP + "8081"+"/game/actionTrain",headers = header_g, json = action_0 )

print(join_game.json())
print(start_action.json())

start_action_dict = start_action.json()
print(type(start_action_dict))

with open('generated_game_state.json', 'w', encoding='utf-8') as f:
    json.dump(start_action_dict, f)

with open('generated_game_state.pkl', 'wb') as f:
    pickle.dump(start_action_dict, f)