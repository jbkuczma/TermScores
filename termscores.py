import argparse
import scores
import datetime as dt

def main():
    date = dt.datetime.now()
    dateStr = "{}/{}/{}".format(date.month,date.day,date.year)
    parser = argparse.ArgumentParser("See live scores in your terminal")
    parser.add_argument("-nfl", action='store_true', help="NFL flag") #action='store_true' allows flag without argument
    parser.add_argument("-nhl", nargs='?', const=dateStr, help="Get game scores for NHL games on provided date (default: TODAY)")
    parser.add_argument("-nba", nargs='?', const=dateStr, help="Get game scores for NBA games on provided date (default: TODAY)") #argument must be in mm/dd/yyyy format
    parser.add_argument("-nbaQ", nargs='?', const=dateStr, help="Get game scores per quarter for NBA games on provided date (default: TODAY)")
    args = parser.parse_args()
    if args.nba:
        scores.nbaScores(args.nba)
    elif args.nbaQ:
        scores.nbaQuarterScores(args.nbaQ)
    elif args.nhl:
        scores.nhlScores(args.nhl)
    elif args.nfl:
        print("NFL score feature coming soon")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()