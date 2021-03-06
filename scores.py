import requests
import pprint
import json
from colorama import Fore, Back, Style


def checkDate(date):
    count = 0
    month = ""
    day = ""
    year = ""
    try:
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
    except ValueError:
        print("Date provided is not valid. Proper format is MM/DD/YYYY")
        exit()
    return True

#nhl takes date in a different format. same code as checkDate() but this returns a string while checkDate() returns bool
def makeNHLDate(date):
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

def nbaScores(date):
    allGames = {}
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        url = 'http://data.nba.com/data/1h/json/cms/noseason/scoreboard/%s/games.json' % makeNBADate(date)
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.text
        data = json.loads(data)
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data['sports_content']['games']['game']) #for testing
        for game in range(0,15):
            gameToAdd = {}
            try:
                gameStatus = data['sports_content']['games']['game'][game]['period_time']['game_status'] #1 = hasn't started, 2 = in progressed, 3 = ended
                gameClock = data['sports_content']['games']['game'][game]['period_time']['game_clock']
                quarterStatus = data['sports_content']['games']['game'][game]['period_time']['period_status'] #ex: final , 7:00 pm
                quarterNumber = data['sports_content']['games']['game'][game]['period_time']['period_value']
                homeTeamCity = data['sports_content']['games']['game'][game]['home']['city']
                awayTeamCity = data['sports_content']['games']['game'][game]['visitor']['city']
                homeTeamNickName = data['sports_content']['games']['game'][game]['home']['nickname']
                awayTeamNickName = data['sports_content']['games']['game'][game]['visitor']['nickname']
                homeTeamAbrv = data['sports_content']['games']['game'][game]['home']['abbreviation']
                awayTeamAbrv = data['sports_content']['games']['game'][game]['visitor']['abbreviation']
                homeScore = data['sports_content']['games']['game'][game]['home']['score']
                awayScore = data['sports_content']['games']['game'][game]['visitor']['score']
                ###
                gameToAdd = {"away team":awayTeamAbrv,"away team score":awayScore,"home team":homeTeamAbrv,"home team score":homeScore,"status":quarterStatus, "clock": gameClock}
                allGames["Game "+str(game+1)] = gameToAdd
                ### hopefully storing the data for each game will allow me to have them constantly update
                if gameStatus == "1" or gameStatus == "3" or quarterStatus == "Halftime":
                    print('{}   {:>3} : {:<3}   {} [{}]'.format(awayTeamAbrv, awayScore, homeScore, homeTeamAbrv, quarterStatus))
                else:
                    print('{}   {:>3} : {:<3}   {} [{}-{} remaining]'.format(awayTeamAbrv, awayScore, homeScore, homeTeamAbrv, quarterStatus, gameClock))
            except IndexError:
                break
    except requests.exceptions.RequestException as e:
            print(e)

def nbaQuarterScores(date):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        url = 'http://data.nba.com/data/1h/json/cms/noseason/scoreboard/%s/games.json' % makeNBADate(date)
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.text
        data = json.loads(data)
        pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data['sports_content']['games']['game']) #for testing
        for game in range(0,15):
            try:
                gameClock = data['sports_content']['games']['game'][game]['period_time']['game_clock']
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
                        print('{} vs {}'.format(awayTeamNickName, homeTeamNickName))
                        print('Tipoff at {}'.format(quarterStatus))
                        print("=======================")
                    elif int(quarterNumber) >= 1 and int(quarterNumber) <= 3:
                        print('{} vs {}'.format(awayTeamNickName, homeTeamNickName))
                        print('{} => {}|{}|{}|{}|{}'.format(awayTeamAbrv,a1Score,a2Score,a3Score,a4Score,aFinalScore))
                        print('{} => {}|{}|{}|{}|{}'.format(homeTeamAbrv,h1Score,h2Score,h3Score,h4Score,hFinalScore))
                        print('{} | {} remaining'.format(quarterStatus,gameClock))
                        print("=======================")
                    else:
                        print('{} vs {}'.format(awayTeamNickName, homeTeamNickName))
                        print('{} => {}|{}|{}|{}|{}'.format(awayTeamAbrv,a1Score,a2Score,a3Score,a4Score,aFinalScore))
                        print('{} => {}|{}|{}|{}|{}'.format(homeTeamAbrv,h1Score,h2Score,h3Score,h4Score,hFinalScore))
                        print('{}'.format(quarterStatus))
                        pp.pprint("=======================")
                except ValueError as e: #if quarterNumber == ''
                    print('{} vs {}'.format(awayTeamNickName, homeTeamNickName))
                    print('Tipoff at {}'.format(quarterStatus))
                    print("=======================")
            except IndexError:
                break
    except requests.exceptions.RequestException as e:
        print(e)


def nhlScores(date):
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
                print(Fore.LIGHTYELLOW_EX + awayTeam + " vs " + homeTeam + Style.RESET_ALL)
                if awayTeamScore > homeTeamScore:
                    print(Fore.GREEN + awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots) + Style.RESET_ALL)
                    print(homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots))
                    print("Period: " + str(period))
                elif homeTeamScore > awayTeamScore:
                    print(awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots))
                    print(Fore.GREEN + homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots) + Style.RESET_ALL)
                    print("Period: " + str(period))
                else:
                    if "PM" not in str(period): #game has started but scores are tied 
                        print(awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots))
                        print(homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots))
                        print("Period: " + str(period))
                    else: #game hasn't started
                        print(awayTeamAbbreviation + " => " + str(awayTeamScore) + "| Shots: " + str(awayTeamShots))
                        print(homeTeamAbbreviation + " => " + str(homeTeamScore) + "| Shots: " + str(homeTeamShots))
                        print("Puck drop at " + str(period) + " ET")

                print("===================")
            except IndexError:
                break
    except Exception as e:
        print(e)

