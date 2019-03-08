import csv
import datetime
import os
from league import league

NUMBER_OF_LEAGUES = 16

# Create leagues
leagueNames = ["Armstrong","Clark","Hammel","Lovell","Galileo","Porco","Rubin","Whitson"
              ,"Johnson","Roman","Faber","Glenn","Sagan","Van Allen","Aldrin","Burnell","Hubble","Vaughan"]
leagues = []
for i in range(len(leagueNames)):
    leagues.append(league(leagueNames[i]))

# Get csv data
with open('.zipCodesDB.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    zipCodesDB = [[]]
    for row in csv_reader:
        zipCodesDB.append(row)
    zipCodesDB = zipCodesDB[2:]
csv_file.close()

with open('.zipCodesDBSortedByDist.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    zipCodesDBSortedByDist = [[]]
    for row in csv_reader:
        zipCodesDBSortedByDist.append(row)
    zipCodesDBSortedByDist = zipCodesDBSortedByDist[2:]
csv_file.close()

with open('teams.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    teams = [[]]
    for row in csv_reader:
        teams.append(row)
    teams = teams[2:]
csv_file.close()
    
#Create zipsAndCounts
zipsAndCounts = {}
for team in teams:
    zipsAndCounts[team[1]] = []
    zipsAndCounts[team[1]].append(team)

#Shorten zipCodesDBSortedByDist to only necesary zips
count = 0
zipsDBSortedShort = []
for zipPair in zipCodesDBSortedByDist:
    count += 1
    if count%2 == 0:
        if zipPair[0] in zipsAndCounts and zipPair[1] in zipsAndCounts:
            zipsDBSortedShort.append(zipPair)

# User Defined Functions

def findDistance(zipOne,zipTwo):

    #Find zipOne
    low, high = 0, len(zipCodesDB)-1
    valueFound = False
    while low <= high and not valueFound:
        mid = low + (high - low) // 2
        midValue = zipCodesDB[mid][0]
        if midValue == zipOne:
            valueFound = True
        elif midValue < zipOne:
            low = mid + 1
        else:
            high = mid - 1

    #Find zipTwo
    valueFound = False
    zipTwoTest = zipCodesDB[mid][1]
    if  zipTwoTest == zipTwo:       #Value found
        return zipCodesDB[mid][2]

    elif zipTwoTest < zipTwo:       #Iterate up  
        iteration = 1
        while not valueFound:
            iteration += 1
            if zipCodesDB[mid+iteration][1] == zipTwo:
                return zipCodesDB[mid+iteration][2]
            if zipCodesDB[mid+iteration][0] != zipOne:
                return False

    else:                           #Iterate down
        iteration = -1
        while not valueFound:
            iteration -= 1
            if zipCodesDB[mid+iteration][1] == zipTwo:
                return zipCodesDB[mid+iteration][2]
            if zipCodesDB[mid+iteration][0] != zipOne:
                return False

def computeAvgDist(zipArray):
    sum = 0.0
    length = len(zipArray)
    count = 0
    for i in range(length):
        for j in range(i+1,length):
            sum += float(findDistance(zipArray[i],zipArray[j]))
            count += 1
    if count != 0:
        return float(sum)/count
    else:
        return sum

def writeLeaguesCSV(leagues):
    allLeagues = [["Team Name","Zip","League"]]
    d = datetime.datetime.today()
    path = "./League_Generation_" + str(d.hour) + "_" + str(d.minute) + "_" + str(d.second)
    os.mkdir(path)
    for league in leagues: 
        leagueArray = league.getArray()
        filename = path + "/" + league.getName() + ".csv"
        with open(filename, 'w+', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(leagueArray)
        csv_file.close()
        for team in leagueArray:
            if team[0] != "Team Name":
                team.append(league.getName())
                allLeagues.append(team)
    with open(path + "/all_leagues.csv", 'w+', newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(allLeagues)
    csv_file.close()

def fillLeagues():

    #Assigning by lowest distance
    numberTeamsAdded = 0
    nextEmptyLeague = 0
    teamLeagueAssignmentIndex = {}
    for zips in zipsDBSortedShort:

        if zips[0] in teamLeagueAssignmentIndex and not zips[1] in teamLeagueAssignmentIndex:           #Second zip not assigned and first assigned
            if not leagues[teamLeagueAssignmentIndex[zips[0]]].isFull():
                for team in teams:
                    if team[1] == zips[1]:
                        leagues[teamLeagueAssignmentIndex[zips[0]]].addTeam(team[0],zips[1],True)
                        numberTeamsAdded += 1
                teamLeagueAssignmentIndex[zips[1]] = teamLeagueAssignmentIndex[zips[0]]

        if not zips[0] in teamLeagueAssignmentIndex and zips[1] in teamLeagueAssignmentIndex:           #First zip not assigned and second assigned
            if not leagues[teamLeagueAssignmentIndex[zips[1]]].isFull():
                for team in teams:
                    if team[1] == zips[0]:
                        leagues[teamLeagueAssignmentIndex[zips[1]]].addTeam(team[0],zips[0],True)
                        numberTeamsAdded += 1
                    teamLeagueAssignmentIndex[zips[0]] = teamLeagueAssignmentIndex[zips[1]]

        if not zips[0] in teamLeagueAssignmentIndex and not zips[1] in teamLeagueAssignmentIndex:       #Neither assigned
            if(nextEmptyLeague < len(leagues)):
                for team in teams:
                    if team[1] == zips[0]:
                        leagues[nextEmptyLeague].addTeam(team[0],zips[0],True)
                        numberTeamsAdded += 1
                teamLeagueAssignmentIndex[zips[0]] = nextEmptyLeague
                for team in teams:
                    if team[1] == zips[1]:
                        leagues[nextEmptyLeague].addTeam(team[0],zips[1],True)
                        numberTeamsAdded += 1
                teamLeagueAssignmentIndex[zips[1]] = nextEmptyLeague
                nextEmptyLeague += 1
    print(str(numberTeamsAdded) + " teams have been assigned")
    


def checkAllZips():
    return 0

##### Main Program #####

# checkAllZips() #Uncomment to run with first time data, will return if any arnt in DB

fillLeagues()
writeLeaguesCSV(leagues)