import json


def getAllPlayerData():
    with open('code\\playerData.json', 'r') as file: playerData = json.load(file)
    return playerData


class GameData:
    def __init__(self, playerName: str):
        self.playerHighscore = self.playerDaysAlive = 0
        self.playerName = playerName
        self.allPlayerData = getAllPlayerData()
        self.gameHighscore = self.getStats()

        if self.playerName not in self.allPlayerData:
            self.addNewPlayer(self.playerName)

        self.playerData = self.allPlayerData[self.playerName]

        print(json.dumps(self.allPlayerData, indent=1), self.playerHighscore, self.gameHighscore)

    def getStats(self):
        highscores = []
        for name in self.allPlayerData:
            currPlayerDate = self.allPlayerData[name]
            highscore = currPlayerDate['highscore']
            daysAlive = currPlayerDate['daysAlive']
            highscores.append(highscore)
            if name == self.playerName:
                self.playerHighscore = highscore
                self.playerDaysAlive = daysAlive

        return max(highscores)

    def addNewPlayer(self, playerName: str):
        self.allPlayerData[playerName] = {
            "playerHighscore": 0,
            "scores": [0],
            "daysAlive": 0
        }
