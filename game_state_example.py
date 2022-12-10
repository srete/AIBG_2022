import json

with open('game_state.json', 'r') as f:
    game_state = json.load(f)

print('Game state:', game_state.keys())
print('Game state data:', game_state['gameState'].keys())
print('Player data:', game_state['gameState']['player1'].keys())
print('Map data:', game_state['gameState']['map'].keys())

# game_state['gameState']['map']['tiles'] je lista, gde je svaki element nova lista sa podacima o poljima koja imaju isto r 
print('One tile data:', game_state['gameState']['map']['tiles'][0][0])

print('Boss data: ', game_state['gameState']['boss'].keys())
print('Boss action: ', game_state['gameState']['boss']['bossAction'], ', boss AttackedTiles: ', game_state['gameState']['boss']['bossAttackedTiles'])

print('ScoreBoard:', game_state['gameState']['scoreBoard'].keys())
print(game_state['gameState']['scoreBoard']['players'][0].keys())