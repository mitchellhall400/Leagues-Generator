import csv
import datetime
import os
from league import league

NUMBER_OF_LEAGUES = 16

teamLeagueAssignmentIndex = {}

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

with open('allZips.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    allZips = []
    for row in csv_reader:
        if int(row[0]) <= 69000:     #Remove lines to include far west NE
            allZips.append(row[0])
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
    allLeagues = [["Team Number","Zip","League"]]
    d = datetime.datetime.today()
    path = "./League_Generation_" + str(d.hour) + "_" + str(d.minute) + "_" + str(d.second) + "_" + str(d.microsecond)
    os.mkdir(path)
    for league in leagues:
        leagueArray = league.getArray()
        filename = path + "/" + league.getName() + ".csv"
        with open(filename, 'w+', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(leagueArray)
        csv_file.close()
        for team in leagueArray:
            if team[0] != "Team Number":
                team.append(league.getName())
                allLeagues.append(team)
    with open(path + "/all_leagues.csv", 'w+', newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(allLeagues)
    csv_file.close()

def fillLeague(league,centralBasis,teamsList,allZips):
    output = 1
    delCount = 0
    league.clear()

    #Add any teams if their zip is the basis
    for i in range(len(teamsList)):
        if int(teamsList[i-delCount][1]) == int(centralBasis):
            output = league.addTeam(teamsList[i-delCount][0],teamsList[i-delCount][1],True)
            del teamsList[i-delCount]
            delCount += 1

    #Go down zipDB sorted finding lowest pairs that are teams to basis
    for zipDB in zipCodesDBSortedByDist:
        if output == 1:     #If league isn't full
            #If the first zip is the basis
            if zipDB[0] == centralBasis:
                delCount = 0
                for i in range(len(teamsList)):
                    if teamsList[i-delCount][1] == zipDB[1]:
                        output = league.addTeam(teamsList[i-delCount][0],teamsList[i-delCount][1],True)
                        del teamsList[i-delCount]
                        delCount += 1
                delCount = 0
            #If the second zip is basis
            if zipDB[1] == centralBasis:
                delCount = 0
                for i in range(len(teamsList)):
                    if teamsList[i-delCount][1] == zipDB[0]:
                        output = league.addTeam(teamsList[i-delCount][0],teamsList[i-delCount][1],True)
                        del teamsList[i-delCount]
                        delCount += 1    
                delCount = 0
    zipsAssigned = league.getZips()
    zipsAssigned.append(centralBasis)
    delCount = 0
    for i in range(len(allZips)):
        if allZips[i-delCount] in zipsAssigned:
            del allZips[i-delCount]
            delCount += 1

    
def checkAllZips():
    return 0

##### Main Program #####

# checkAllZips() #Uncomment to run with first time data, will return if any arnt in DB

teamsCopy = teams[:]
delCount = 0
bestScore = 1000000000.0
score = 0
percent = 0
bestLeagues = []

tempArray = []
for team in teamsCopy:
    tempArray.append(team[1])

#Remove far west NE
for i in range(len(teamsCopy)):
    if int(teamsCopy[i-delCount][1]) >= 69000:
        del teamsCopy[i-delCount]
        delCount += 1

teamsCopyReset = teamsCopy[:]
allZipsReset = allZips[:]

#Find best fill by testing all combinations
#League 1
for zipOne in allZips:
    fillLeague(leagues[0],zipOne,teamsCopy,allZips)
    
    #League 2
    for zipTwo in allZips:
        fillLeague(leagues[1],zipTwo,teamsCopy,allZips)

        #League 3
        for zipThree in allZips:
            fillLeague(leagues[2],zipThree,teamsCopy,allZips)

            #League 4
            for zipFour in allZips:
                fillLeague(leagues[3],zipFour,teamsCopy,allZips)
                
                #League 5
                for zipFive in allZips:
                    fillLeague(leagues[4],zipFive,teamsCopy,allZips)

                    #League 6
                    for zipSix in allZips:
                        fillLeague(leagues[5],zipSix,teamsCopy,allZips)

                        #League 7
                        for zipSeven in allZips:
                            fillLeague(leagues[6],zipSeven,teamsCopy,allZips)
                            
                            #League 8
                            for zipEight in allZips:
                                fillLeague(leagues[7],zipEight,teamsCopy,allZips)

                                #League 9
                                for zipNine in allZips:
                                    fillLeague(leagues[8],zipNine,teamsCopy,allZips)

                                    #League 10
                                    for zipTen in allZips:
                                        fillLeague(leagues[9],zipTen,teamsCopy,allZips)

                                        #League 11
                                        for zipEleven in allZips:
                                            fillLeague(leagues[10],zipEleven,teamsCopy,allZips)

                                            #League 12
                                            for zipTwelve in allZips:
                                                fillLeague(leagues[11],zipTwelve,teamsCopy,allZips)

                                                #League 13
                                                for zipThirteen in allZips:
                                                    fillLeague(leagues[12],zipThirteen,teamsCopy,allZips)

                                                    #League 14
                                                    for zipFourTeen in allZips:
                                                        fillLeague(leagues[13],zipFourTeen,teamsCopy,allZips)

                                                        #League 15
                                                        for zipFifteen in allZips:
                                                            fillLeague(leagues[14],zipFifteen,teamsCopy,allZips)

                                                            #League 16
                                                            for zipSixteen in allZips:
                                                                fillLeague(leagues[15],zipSixteen,teamsCopy,allZips)

                                                                #Compute score
                                                                for league in leagues:
                                                                    score += computeAvgDist(league.getZips())

                                                                #Set to bestLeagues if best score and used all teams
                                                                if score < bestScore and not teamsCopy:
                                                                    bestScore = score
                                                                    bestLeagues = leagues[:]
                                                                    writeLeaguesCSV(leagues)
                                                                    print(teamsCopy)
                                                                    print(score)
                                                                percent += 1
                                                                print(percent)

                                                                #Reset
                                                                teamsCopy = teamsCopyReset[:]
                                                                allZips = allZipsReset[:]
                                                                score = 0
                                                                leagues[15].clear()
                                                            #Reset
                                                            teamsCopy = teamsCopyReset[:]
                                                            allZips = allZipsReset[:]
                                                            score = 0
                                                            leagues[14].clear()
                                                        #Reset
                                                        teamsCopy = teamsCopyReset[:]
                                                        allZips = allZipsReset[:]
                                                        score = 0
                                                        leagues[13].clear()
                                                    #Reset
                                                    teamsCopy = teamsCopyReset[:]
                                                    allZips = allZipsReset[:]
                                                    score = 0
                                                    leagues[12].clear()
                                                #Reset
                                                teamsCopy = teamsCopyReset[:]
                                                allZips = allZipsReset[:]
                                                score = 0
                                                leagues[11].clear()
                                            #Reset
                                            teamsCopy = teamsCopyReset[:]
                                            allZips = allZipsReset[:]
                                            score = 0
                                            leagues[10].clear()
                                        #Reset
                                        teamsCopy = teamsCopyReset[:]
                                        allZips = allZipsReset[:]
                                        score = 0
                                        leagues[9].clear()
                                    #Reset
                                    teamsCopy = teamsCopyReset[:]
                                    allZips = allZipsReset[:]
                                    score = 0
                                    leagues[8].clear()
                                #Reset
                                teamsCopy = teamsCopyReset[:]
                                allZips = allZipsReset[:]
                                score = 0
                                leagues[7].clear()
                            #Reset
                            teamsCopy = teamsCopyReset[:]
                            allZips = allZipsReset[:]
                            score = 0
                            leagues[6].clear()
                        #Reset
                        teamsCopy = teamsCopyReset[:]
                        allZips = allZipsReset[:]
                        score = 0
                        leagues[5].clear()
                    #Reset
                    teamsCopy = teamsCopyReset[:]
                    allZips = allZipsReset[:]
                    score = 0
                    leagues[4].clear()
                #Reset
                teamsCopy = teamsCopyReset[:]
                allZips = allZipsReset[:]
                score = 0
                leagues[3].clear()
            #Reset
            teamsCopy = teamsCopyReset[:]
            allZips = allZipsReset[:]
            score = 0
            leagues[2].clear()
        #Reset
        teamsCopy = teamsCopyReset[:]
        allZips = allZipsReset[:]
        score = 0
        leagues[1].clear()
    #Reset
    teamsCopy = teamsCopyReset[:]
    allZips = allZipsReset[:]
    score = 0
    leagues[0].clear()
                                                                
print(bestLeagues)
writeLeaguesCSV(bestLeagues)