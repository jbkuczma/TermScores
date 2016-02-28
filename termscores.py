import sys
import argparse
import scores

def main():
    parser = argparse.ArgumentParser("See live scores in your terminal")
    parser.add_argument("-nfl", action='store_true', help="NFL flag") #action='store_true' allows flag without argument
    parser.add_argument("-nhl", help="Get game scores for NHL games on given date")
    parser.add_argument("-nba", help="Get game scores for NBA games on given date") #argument must be in mm/dd/yyyy format
    args = parser.parse_args()
    if len(sys.argv) > 3:
        parser.print_help()
    elif args.nfl:
        # http://www.nfl.com/liveupdate/scorestrip/ss.xml
        # http://www.nfl.com/liveupdate/scorestrip/postseason/ss.xml
        print("You want scores for the NFL")
    elif args.nhl:
        scores.nhlScores(args.nhl)
    elif args.nba:
        scores.nbaScores(args.nba)

if __name__ == '__main__':
    main()