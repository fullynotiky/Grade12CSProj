import json


def getAllPlayerData():
    with open('code\\playerData.json', 'r') as file: playerData = json.load(file)
    return playerData


class GameData:
    def __init__(self, playerName: str):
        self.playerHighscore = 0
        self.playerName = playerName
        self.allPlayerData = getAllPlayerData()
        self.gameHighscore = self.getStats()

        if self.playerName not in self.allPlayerData: self.addNewPlayer(self.playerName)
        self.playerData = self.allPlayerData[self.playerName]

    def getStats(self):
        allHighscores = []
        for name in self.allPlayerData:
            currPlayerDate = self.allPlayerData[name]
            highscore = currPlayerDate['highscore']
            allHighscores.append(highscore)
            if name == self.playerName:
                self.playerHighscore = highscore

        return max(allHighscores)

    def addNewPlayer(self, playerName: str):
        self.allPlayerData[playerName] = {
            'highscore': 0,
            'scores': []
        }

    def updateHighscores(self):
        for name in self.allPlayerData:
            scores = []
            scores.extend(self.allPlayerData[name])

    def end(self, player):
        self.allPlayerData[self.playerName]['scores'].append(abs(player.score))
        newHighscore = max(self.allPlayerData[self.playerName]['scores'])
        self.allPlayerData[self.playerName]['highscore'] = newHighscore

        if newHighscore > self.playerHighscore:
            player.level.startMenu.highScoreSurf = player.level.startMenu.smallFont.render(f'HIGHSCORE: {self.playerHighscore}',
                                                                                           True,
                                                                                           'white')

        with open('code\\playerData.json', 'w') as file:
            json.dump(self.allPlayerData, file, indent=2)
            file.write('\n')
