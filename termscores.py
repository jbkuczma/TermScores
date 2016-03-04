import sys
import argparse
import scores
import datetime as dt

def main():
    date = dt.datetime.now()
    dateStr = "{}/{}/{}".format(date.month,date.day,date.year)
    parser = argparse.ArgumentParser("See live scores in your terminal")
    parser.add_argument("-nfl", action='store_true', help="NFL flag") #action='store_true' allows flag without argument
    parser.add_argument("-nhl", action='store_true', help="Get game scores for NHL games")
    parser.add_argument("-nba", action='store_true', help="Get game scores for NBA games") #argument must be in mm/dd/yyyy format
    parser.add_argument("-nbaQ", action='store_true', help="Get game scores per quarter for NBA games")
    parser.add_argument("-d", nargs='?', const=dateStr, help="Date flag (default: TODAY)")
    args = parser.parse_args()
    if args.nba:
        scores.nbaScores(args.d)
    elif args.nbaQ:
        scores.nbaQuarterScores(args.d)
    elif args.nhl:
        scores.nhlScores(args.d)
    elif args.nfl:
        print("NFL score feature coming soon")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()