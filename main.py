import argparse
from scraper import scraper


leagues = ["Serie", "Liga", "Ligue", "Bundesliga", "Premier"]
countries = ["Italy", "Spain", "France", "Germany", "England"]

# parse the arguments
def parseRequest():
    parse = argparse.ArgumentParser(description="A command line tool to get the results of previous matches and schedules of upcoming matches of all the leagues and cups as foound on fbref.com")
    parse.add_argument("date", type=str, nargs = "?", help="Date formated as \"YY-MM-DD\" or \"today\" or \"yesterday\" or \"tomorrow\", in case of no date provided, today's date will be used")
    parse.add_argument("-l", "--league", default=leagues, nargs="*", choices = leagues, help="a league to display its results, if no league is provided, all the leagues will be displayed")
    parse.add_argument('-c', "--country", default=[], nargs="*", choices=countries, help="a country to display the results of all its leagues and cups (this will overwrite the league)")
    parse.add_argument("--fbd", default=0, type=int, help="number of days to go forwards or backwards from the date provided, such that negative numbers will go backwards")
    parse.add_argument('-a', "--all", default = False, action="store_true", help="display all the results of all leagues and cups (this will overwrite the league and country)")
    args = parse.parse_args()
    return args

args = parseRequest()
# # feed the date to the scraper object to fetch all the info needed
fbref = scraper(args)
fbref.run()