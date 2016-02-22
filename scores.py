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
    elif args.nba:
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
        if int(day) >= 1 and int(day) <= 9:
            day = str(0) + day
        if int(month) >= 1 and int(month) <= 9:
            month = str(0) + month
        return year + "-" + month + "-" + day
    else:
        print("The date provided is not valid")
        exit(0)

def makeNBADate(date):
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
        if int(day) >= 1 and int(day) <= 9:
            day = str(0) + day
        if int(month) >= 1 and int(month) <= 9:
            month = str(0) + month
        return year + month + day
    else:
        print("The date provided is not valid")
        exit(0)
# def getDate(date):
#     if checkDate(date):
#         return date
#     else:
#         print("The date provided is not valid")
#         exit(0)
#     # return time.strftime("%x") #returns current date in month/day/year format

def nbaScores(date,league):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        # url = 'http://sports.espn.go.com/%s/bottomline/scores' % league
        # url = 'http://espn.go.com/nba/scoreboard/_/date/%s' % makeNBADate(date) #date must be yyyymmdd
        # probably won't use either above #
        url = 'http://data.nba.com/data/1h/json/cms/noseason/scoreboard/%s/games.json' % makeNBADate(date)  #date must be yyyymmdd
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        # use bs4 to parse
        data = response.text
        data = json.loads(data)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)
    except Exception as e:
        print(e)


def nhlScores(date,league):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        url = "http://live.nhle.com/GameData/GCScoreboard/%s.jsonp" % makeNHLDate(date)
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        data = response.text
        data = data.replace('loadScoreboard(', '')
        data = data[:-2]
        data = json.loads(data)
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data) #for testing
        for game in range(0,15): #worst case there are 15 games being played. unsure how else to determine
            try:
                homeTeam = data['games'][game]['htn']
                awayTeam = data['games'][game]['atn']
                homeTeamAbbreviation = data['games'][game]['hta']
                awayTeamAbbreviation = data['games'][game]['ata']
                gameState = data['games'][game]['bsc']
                period = data['games'][game]['bs']
                if gameState == 'progress' or 'final':
                    try:
                        homeTeamShots = data['games'][game]['htsog']
                        awayTeamShots = data['games'][game]['atsog']
                        homeTeamScore = data['games'][game]['hts']
                        awayTeamScore = data['games'][game]['ats']
                    except Exception as e: #if the game hasn't started these would not return a value so we need to set them to 0
                        homeTeamShots = 0
                        awayTeamShots = 0
                        homeTeamScore = 0
                        awayTeamScore = 0
                print(colors.bcolors.WARNING + awayTeam + " vs " + homeTeam + colors.bcolors.ENDC)
                if awayTeamScore > homeTeamScore:
                    print(colors.bcolors.OKGREEN + awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots) + colors.bcolors.ENDC)
                    print(homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots))
                elif homeTeamScore > awayTeamScore:
                    print(awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots))
                    print(colors.bcolors.OKGREEN + homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots) + colors.bcolors.ENDC)
                else:
                    print(awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots))
                    print(homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots))
                print("Period: " + str(period))
                print("===================")
            except IndexError:
                break
    except Exception as e:
        print(e)

main()
