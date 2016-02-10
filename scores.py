import sys
import argparse
import requests
import pprint
import json
import colors

def main():
    #scores seem to be updated every 20 minutes for nba
    parser = argparse.ArgumentParser("See live scores in your terminal")
    parser.add_argument("-nfl", action='store_true', help="NFL flag") #action='store_true' allows flag without argument
    parser.add_argument("-nhl", help="NHL flag")
    parser.add_argument("-nba", help="NBA flag") #argument must be in mm/dd/yyyy format
    args = parser.parse_args()
    if len(sys.argv) > 3:
        parser.print_help()
    elif args.nfl:
        print("You want scores for the NFL")
    elif args.nhl:
        nhlScores(args.nhl,"nhl")
        #http://live.nhle.com/GameData/GCScoreboard/2016-02-09.jsonp #date is yyyy-mm-dd
        #http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=?
        #http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812
        # print("You want scores for the NHL")
    elif args.nba:
        # print("You want scores for the NBA")
        nbaScores(args.nba,"nba")


def checkDate(date):
    count = 0
    month = ""
    day = ""
    year = ""
    for c in date:
        if count == 0:
            if c == '/':
                count+=1
            else:
                month+=c
        elif count == 1:
            if c == '/':
                count+=1
            else:
                day+=c
        elif count == 2:
            if c == '/':
                count+=1
            else:
                year+=c
    if count > 2 or int(month) > 12 or int(month) < 1 or int(day) < 1 or int(day) > 31 or int(year) < 1947: #unsure about year cutoff. this seems to be as far back as possible (for nba)
        return False
    return True


def makeNHLDate(date): #nhl takes date in a different format. same code as checkDate() but this returns a string while checkDate(0 returns bool
    count = 0
    if checkDate(date):
        month = ""
        day = ""
        year = ""
        for c in date:
            if count == 0:
                if c == '/':
                    count+=1
                else:
                    month+=c
            elif count == 1:
                if c == '/':
                    count+=1
                else:
                    day+=c
            elif count == 2:
                if c == '/':
                    count+=1
                else:
                    year+=c
        if int(day) >= 1 or int(day) <= 9:
            day = str(0) + day
        if int(month) >= 1 or int(month) <= 9:
            month = str(0) + month
        return year + "-" + month + "-" + day
    else:
        print("The date provided is not valid")
        exit(0)

def getDate(date):
    if checkDate(date):
        return date
    else:
        print("The date provided is not valid")
        exit(0)
    # return time.strftime("%x") #returns current date in month/day/year format

def nbaScores(date,league):
    maxTeamLength = 14 #Oklahoma City is the longest team city name
    spacesNeeded = 0
    try:
        count = 0
        # url = 'http://sports.espn.go.com/%s/bottomline/scores' % league #probably not using this for NBA
        ###
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        url = "http://stats.nba.com/stats/scoreboard/?GameDate=%s&LeagueID=00&DayOffset=0" % getDate(date)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()['resultSets'][1]['rowSet']
        for i in data:
            pp = pprint.PrettyPrinter(indent=4)
            team = i[5]
            if not i[7]:
                q1Score = 0
            else:
                q1Score = i[7]
            if not i[8]:
                q2Score = 0
            else:
                q2Score = i[8]
            if not i[9]:
                q3Score = 0
            else:
                q3Score = i[9]
            if not i[10]:
                q4Score = 0
            else:
                q4Score = i[10]
            if not i[21]:
                finalScore = 0
            else:
                finalScore = i[21]
            if len(team) < maxTeamLength:
                spacesNeeded = maxTeamLength - len(team)
            pp.pprint(team + ":" + " " * spacesNeeded + str(q1Score) +"|" + str(q2Score) + "|" + str(q3Score) + "|" + str(q4Score) + " => " + str(finalScore)) #testing
            count+=1
            if count % 2 == 0:
                print(colors.bcolors.OKGREEN + "===================================" + colors.bcolors.ENDC)
    except Exception as e:
        print(e)


def nhlScores(date,league):
    try:
        count = 0
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        url = "http://live.nhle.com/GameData/GCScoreboard/%s.jsonp" % makeNHLDate(date)

        response = requests.get(url,headers=headers)
        response.raise_for_status()
        data = response.text
        data = data.replace('loadScoreboard(', '')
        data = data[:-2]

        data = json.loads(data)
        pp = pprint.PrettyPrinter(indent=4) #for testing
        pp.pprint(data) #for testing
    except Exception as e:
        print(e)

main()
