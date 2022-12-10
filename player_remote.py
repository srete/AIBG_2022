import requests

#Za rucno pomeranje igraca

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


#RUCNO UKUCATI ZELJENU AKCIJU
action = {
    "action":"move,-7,-6"
}

start_action  = requests.post(url =SERVER_IP + "8081"+"/game/actionTrain",headers = header_g, json = action)
print(start_action.json())