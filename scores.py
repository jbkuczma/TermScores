import sys
import argparse
import requests
import pprint

def main():
    parser = argparse.ArgumentParser("See live scores in your terminal")
    parser.add_argument("-nfl", action='store_true', help="NFL flag") #action='store_true' allows flag without argument
    parser.add_argument("-nhl", action='store_true', help="NHL flag")
    parser.add_argument("-nba", action='store_true', help="NBA flag")
    args = parser.parse_args()
    if len(sys.argv) > 2:
        parser.print_help()
    elif args.nfl:
        print("You want scores for the NFL")
    elif args.nhl:
        print("You want scores for the NHL")
    elif args.nba:
        # print("You want scores for the NBA")
        nbaScores("nba")

def nbaScores(league):
    count = 0
    try:
        # url = 'http://sports.espn.go.com/%s/bottomline/scores' % league #probably not using this for NBA
        ###
        # url = "http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=02%2F04%2F2016" #or this one either
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        url = "http://stats.nba.com/stats/scoreboard/?GameDate=02/6/2016&LeagueID=00&DayOffset=0" #02/4/2016 will have to be replaced with current date
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
            pp.pprint(team + ": " + str(q1Score) +"|" + str(q2Score) + "|" + str(q3Score) + "|" + str(q4Score) + " => " + str(finalScore)) #testing
            count+=1
            if count % 2 == 0:
                print("==============")
        # print(data)
        # pp = pprint.PrettyPrinter(indent=4) #testing
        # pp.pprint(data) #testing
    except Exception as e:
        print(e)

main()
