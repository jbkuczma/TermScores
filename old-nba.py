'''
This file serves no actual purpose to TermScores. This was the old implementation of accessing the NBA scores for each
quarter and a game's final score. I really didn't want to get rid of it.
'''

from scores import getDate
import colors
import pprint
import requests

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