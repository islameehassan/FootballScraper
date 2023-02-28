#!/usr/bin/env python3
import argparse
import requests
from Scraper import Scraper

# parse request
leagues = ["Serie", "Liga", "Ligue", "Bundesliga", "Premier"]
countries = ["Italy", "Spain", "France", "Germany", "England"]
def parseRequest():
    parse = argparse.ArgumentParser(description="A CLI program to fetch the match schedules of a date of your choice from fbref Website")
    parse.add_argument("date", type=str, help="Date formated as \"YY-MM-DD\"")
    parse.add_argument("-l", "--league", default=leagues, nargs="*",  choices = leagues, help="a league to display its results")
    parse.add_argument('-c', "--country", default=[], nargs="*", choices=countries, help="a country to display the results of all its leagues and cups (this will overwrite the league)")
    parse.add_argument('-a', "--all", default = False, action="store_true", help="display all the results of all leagues and cups (this will overwrite the league and country)")
    args = parse.parse_args()
    return args

args = parseRequest()
# feed the date to the scraper object to fetch all the info needed
OneFootball = Scraper(args)
OneFootball.run()