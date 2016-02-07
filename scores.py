import sys
import argparse
import requests
import pprint
import datetime

def main():
    parser = argparse.ArgumentParser("See live scores in your terminal")
    parser.add_argument("-nfl", action='store_true', help="NFL flag") #action='store_true' allows flag without argument
    parser.add_argument("-nhl", action='store_true', help="NHL flag")
    parser.add_argument("-nba", help="NBA flag") #argument must be in mm/dd/yyyy format
    args = parser.parse_args()
    if len(sys.argv) > 3:
        parser.print_help()
    elif args.nfl:
        print("You want scores for the NFL")
    elif args.nhl:
        print("You want scores for the NHL")
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
    if count > 2 or int(month) > 12 or int(month) < 1 or int(day) < 1 or int(day) > 31 or int(year) < 1947: #unsure about year cutoff. this seems to be as far back as possible
        return False
    return True


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
            pp = pprint.PrettyPrinter(indent=4) #testing
            # pp.pprint(i)
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
                print("===================================")
        # print(data)
        # pp = pprint.PrettyPrinter(indent=4) #testing
        # pp.pprint(data) #testing
    except Exception as e:
        print(e)

main()
