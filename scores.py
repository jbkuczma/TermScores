import sys
import argparse
import requests
import pprint
import json
import colors

def main():
    parser = argparse.ArgumentParser("See live scores in your terminal")
    parser.add_argument("-nfl", action='store_true', help="NFL flag") #action='store_true' allows flag without argument
    parser.add_argument("-nhl", help="Get game scores for NHL games on given date")
    parser.add_argument("-nba", help="Get game scores for NBA games on given date") #argument must be in mm/dd/yyyy format
    args = parser.parse_args()
    if len(sys.argv) > 3:
        parser.print_help()
    elif args.nfl:
        print("You want scores for the NFL")
    elif args.nhl:
        nhlScores(args.nhl,"nhl")
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

def nbaScores(date,league):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        url = 'http://data.nba.com/data/1h/json/cms/noseason/scoreboard/%s/games.json' % makeNBADate(date)  #date must be yyyymmdd
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.text
        data = json.loads(data)
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data['sports_content']['games']['game']) #for testing
        for game in range(0,15):
            try:
                gameClock = data['sports_content']['games']['game'][game]['period_time']['game_clock']
                # quarter = data['sports_content']['games']['game'][game]['period_time']['period_name']
                quarterStatus = data['sports_content']['games']['game'][game]['period_time']['period_status'] #ex: final , 7:00 pm
                quarterNumber = data['sports_content']['games']['game'][game]['period_time']['period_value']

                homeTeamCity = data['sports_content']['games']['game'][game]['home']['city']
                awayTeamCity = data['sports_content']['games']['game'][game]['visitor']['city']
                homeTeamNickName = data['sports_content']['games']['game'][game]['home']['nickname']
                awayTeamNickName = data['sports_content']['games']['game'][game]['visitor']['nickname']
                homeTeamAbrv = data['sports_content']['games']['game'][game]['home']['abbreviation']
                awayTeamAbrv = data['sports_content']['games']['game'][game]['visitor']['abbreviation']
                try:
                    if int(quarterNumber) == 0:
                        h1Score = '0'
                        h2Score = '0'
                        h3Score = '0'
                        h4Score = '0'
                        hFinalScore = '0'
                        a1Score = '0'
                        a2Score = '0'
                        a3Score = '0'
                        a4Score = '0'
                        aFinalScore = '0'
                    elif int(quarterNumber) == 1:
                        h1Score = data['sports_content']['games']['game'][game]['home']['linescores']['period']['score']
                        h2Score = '0'
                        h3Score = '0'
                        h4Score = '0'
                        hFinalScore = str(int(h1Score) + int(h2Score) + int(h3Score) + int(h4Score))
                        a1Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period']['score']
                        a2Score = '0'
                        a3Score = '0'
                        a4Score = '0'
                        aFinalScore = str(int(a1Score) + int(a2Score) + int(a3Score) + int(a4Score))
                    elif int(quarterNumber) == 2:
                        h1Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][0]['score']
                        h2Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][1]['score']
                        h3Score = '0'
                        h4Score = '0'
                        hFinalScore = str(int(h1Score) + int(h2Score) + int(h3Score) + int(h4Score))
                        a1Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][0]['score']
                        a2Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][1]['score']
                        a3Score = '0'
                        a4Score = '0'
                        aFinalScore = str(int(a1Score) + int(a2Score) + int(a3Score) + int(a4Score))
                    elif int(quarterNumber) == 3:
                        h1Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][0]['score']
                        h2Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][1]['score']
                        h3Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][2]['score']
                        h4Score = '0'
                        hFinalScore = str(int(h1Score) + int(h2Score) + int(h3Score) + int(h4Score))
                        a1Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][0]['score']
                        a2Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][1]['score']
                        a3Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][2]['score']
                        a4Score = '0'
                        aFinalScore = str(int(a1Score) + int(a2Score) + int(a3Score) + int(a4Score))
                    elif int(quarterNumber) == 4:
                        h1Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][0]['score']
                        h2Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][1]['score']
                        h3Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][2]['score']
                        h4Score = data['sports_content']['games']['game'][game]['home']['linescores']['period'][3]['score']
                        hFinalScore = data['sports_content']['games']['game'][game]['home']['score']
                        a1Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][0]['score']
                        a2Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][1]['score']
                        a3Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][2]['score']
                        a4Score = data['sports_content']['games']['game'][game]['visitor']['linescores']['period'][3]['score']
                        aFinalScore = data['sports_content']['games']['game'][game]['visitor']['score']
                except ValueError as e: #if quarterNumber == ''
                    h1Score = '0'
                    h2Score = '0'
                    h3Score = '0'
                    h4Score = '0'
                    hFinalScore = '0'
                    a1Score = '0'
                    a2Score = '0'
                    a3Score = '0'
                    a4Score = '0'
                    aFinalScore = '0'
                try:
                    if int(quarterNumber) == 0:
                        pp.pprint(awayTeamNickName + " vs " + homeTeamNickName)
                        pp.pprint("Tipoff at " + quarterStatus)
                        pp.pprint("==============================")
                    elif int(quarterNumber) >= 1 and int(quarterNumber) <= 3:
                        pp.pprint(awayTeamNickName + " vs " + homeTeamNickName)
                        pp.pprint(awayTeamAbrv + ' => ' + a1Score + "|" + a2Score + "|" + a3Score + "|" + a4Score + "|" + aFinalScore)
                        pp.pprint(homeTeamAbrv + ' => ' + h1Score + "|" + h2Score + "|" + h3Score + "|" + h4Score + "|" + hFinalScore)
                        pp.pprint(quarterStatus + ' | ' + gameClock + " remaining")
                        pp.pprint("==============================")
                    else:
                        pp.pprint(awayTeamNickName + " vs " + homeTeamNickName)
                        pp.pprint(awayTeamAbrv + ' => ' + a1Score + "|" + a2Score + "|" + a3Score + "|" + a4Score + "|" + aFinalScore)
                        pp.pprint(homeTeamAbrv + ' => ' + h1Score + "|" + h2Score + "|" + h3Score + "|" + h4Score + "|" + hFinalScore)
                        pp.pprint(quarterStatus)
                        pp.pprint("==============================")
                except ValueError as e: #if quarterNumber == ''
                    pp.pprint(awayTeamNickName + " vs " + homeTeamNickName)
                    pp.pprint("Tipoff at " + quarterStatus)
                    pp.pprint("==============================")
            except IndexError:
                break
    except requests.exceptions.RequestException as e:
        print(e)
        # print("Data cannot be retrieved for this date at the moment")


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
                    print("Period: " + str(period))
                elif homeTeamScore > awayTeamScore:
                    print(awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots))
                    print(colors.bcolors.OKGREEN + homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots) + colors.bcolors.ENDC)
                    print("Period: " + str(period))
                else:
                    print(awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots))
                    print(homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots))
                    print("Puck drop at " + str(period))

                print("===================")
            except IndexError:
                break
    except Exception as e:
        print(e)

main()
