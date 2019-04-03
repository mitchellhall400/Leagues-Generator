class league:

    MAX_NUMBER_OF_TEAMS = 16

    def __init__(self,name):
        self.teamCount = 0
        self.name = name
        self.teams = []
        self.zips = []
    
    def __repr__(self):
        self.printOut = "\nThe " + self.name + " League"
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
            return 1
        elif overrideMax:
            self.teamCount += 1
            self.teams.append(teamIn)
            self.zips.append(zip)
            return 0
        else:
            return -1

    def getArray(self):
        outputArray = []
        for i in range(self.teamCount):
            zip = self.zips[i]
            if int(zip) < 60000:
                zipOut = zip + " IA"
            else:
                zipOut = zip + " NE"
            outputArray.append([self.teams[i],zipOut])
        return outputArray

    def clear(self):
        self.teams = []
        self.zips = []
        self.teamCount = 0
    
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