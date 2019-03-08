class league:

    MAX_NUMBER_OF_TEAMS = 16

    def __init__(self,name):
        self.teamCount = 0
        self.name = name
        self.teams = []
        self.zips = []
    
    def __repr__(self):
        self.printOut = "\nThe " + self.name + "League"
        for i in range(self.teamCount):
            length = len(self.teams[i])
            dashes = " " + ("-" * (50-length)) + " "
            self.printOut = self.printOut + "\n\t" + str(self.teams[i] + dashes + self.zips[i])
        return(self.printOut)

    def addTeam(self, teamIn, zip, overrideMax):
        if self.teamCount < self.MAX_NUMBER_OF_TEAMS:
            self.teamCount += 1
            self.teams.append(teamIn)
            self.zips.append(zip)
            return True
        elif overrideMax:
            self.teamCount += 1
            self.teams.append(teamIn)
            self.zips.append(zip)
            return True
        else:
            return False

    def getArray(self):
        outputArray = [["Team Name","Zip"]]
        for i in range(self.teamCount):
            outputArray.append([self.teams[i],self.zips[i]])
        return outputArray
    
    def getName(self):
        return self.name

    def getTeams(self):
        return self.teams

    def getZips(self):
        return self.zips

    def isFull(self):
        if self.teamCount >= 16:
            return True
        else:
            return False