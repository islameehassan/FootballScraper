from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import date
from datetime import timedelta
from datetime import datetime
from colorama import Fore, Back, Style
from colorama import init

# Scraper Class
# scraps fbref.com to get matches info either by league or by country
# Leagues Supported:
# Serie A, La Liga, Premier League, Ligue 1, Bundesliga
# Countries Supported:
# Italy, Spain, France, Germany, England

fbref_url = 'https://fbref.com/en/matches/'
class scraper:
    # init the scraper object
    def __init__(self, args):
        self.date = args.date
        self.days = args.fbd
        self.leagues = args.league
        self.countries = args.country
        self.searchmethod = "all" if args.all else "league" if len(self.countries) == 0 else "country"
        self.CountriesLeagues = {}    
    
    # parse the date for validation purposes and special functionalities, like allowing to type "yesterday" instead of the date formated "YY-MM-DD"
    def parseDate(self):
        datetime_object = date.today() # get today's date, default value

        if self.date == "yesterday":
            datetime_object = datetime_object + timedelta(days=-1)
        elif self.date == "tomorrow":
            datetime_object = datetime_object + timedelta(days=1)
        elif self.date != "today" and self.date != None:
            try:
                datetime_object = date.fromisoformat(self.date) # check validity of the date
            except:
                print("Invalid Date")
                exit()  
        datetime_object = datetime_object + timedelta(days=self.days)
        self.date = datetime_object.strftime('%Y-%m-%d') 
        
    # use selenium to get the html source code and pass it to BeautifulSoup
    def sendRequest(self):
        self.parseDate()
        fire_foptions = Options()
        fire_foptions.add_argument("--headless")
        self.driver = webdriver.Firefox(options=fire_foptions)
        self.driver.get(fbref_url + self.date)
        htmlsource = self.driver.page_source
        self.soup = BeautifulSoup(htmlsource, 'lxml')
        self.tables = self.soup.find_all("div", class_= lambda text: False if text is None else "table_wrapper" in text.lower()) # get all the tables to be parsed later
    
    # parse leagues names
    def parseLeagues(self):
        for i in range(len(self.leagues)):
            if "Serie" == self.leagues[i]:
                self.leagues[i] = "Serie A"
            elif "Liga" == self.leagues[i]:
                self.leagues[i] = "La Liga"
            elif "ligue" == self.leagues[i]:
                self.leagues[i] = "Ligue 1"
            elif "Premier" == self.leagues[i]:
                self.leagues[i] = "Premier League"
            elif "bundesliga" == self.leagues[i]:
                self.leagues[i] = "Bundesliga"

    # parse countries names
    def parseCountries(self):
        for i in range(len(self.countries)):
            if "England" == self.countries[i]:
                self.countries[i] = "eng"
            elif "Italy" == self.countries[i]:
                self.countries[i] = "it"
            elif "Spain" == self.countries[i]:
                self.countries[i] = "es"
            elif "France" == self.countries[i]:
                self.countries[i] = "fr"
            elif "Germany" == self.countries[i]:
                self.countries[i] = "de"
    
    # in case of search by country, map all the leagues to their countries
    def getCountriesLeagues(self):
        self.parseCountries()
        self.CountriesLeagues = {country: [] for country in self.countries}
        for country in self.countries:
            for row in self.tables:
                tags = row.find("h2").find_all("span", class_= lambda text: False if text is None else "f-i" in text.lower())
                for tag in tags:
                    if tag.text == country:
                        self.CountriesLeagues[country].append(row)

    # get the details of the matches
    def get_matches_info(self, matches):
        for i, match in enumerate(matches, 0):
            match_details = match.find("td")
            for match_details in match:
                if match_details['data-stat'] == "home_team":
                    HomeTeam = match_details.find('a').text
                elif match_details['data-stat'] == "away_team":
                    AwayTeam = match_details.find('a').text
                elif match_details['data-stat'] == "score":
                    try:
                        Score = match_details.find("a").text
                    except:
                        Score = ""
                elif match_details['data-stat'] == "start_time":
                    try:
                        Time = match_details.find("span", {"class": "localtime"}).text
                        # print(match_details.find_all("span", class_="venuetime"))[1].text
                    except:
                        Time = "Local Time Not Available"
                elif match_details['data-stat'] == "notes":
                    try:
                        Notes = match_details.text
                    except:
                        Notes = ""
            print(str(i+1) + ") " + HomeTeam + " vs " + AwayTeam + " " + Fore.GREEN + Score)
            if Time != "":
                print(Fore.BLUE + Time)
            else:
                print(Fore.RED + "Time not available")
            if Notes != "":
                print(Fore.RED + Notes)
            if i != len(matches)-1:
                print("-"*15)

    # get matches by country 
    def get_matches_info_by_country(self):
        self.getCountriesLeagues()
        print("-"*15)
        for j, country in enumerate(self.CountriesLeagues, 0):
            if len(self.CountriesLeagues[country]) == 0:
                print(Fore.RED + f"No matches found on {self.date} for " + country)
                continue
            if j != 0:
                print()
            print(Fore.RED + country)
            print("-"*15)
            for i, league in enumerate(self.CountriesLeagues[country], 0):
                league_title = league.find('a')
                print(Fore.CYAN + league_title.text)
                print("-"*15)
                matches = league.find_all("tr")
                matches.pop(0)
                self.get_matches_info(matches)
                if i != len(self.CountriesLeagues[country])-1:
                    print("") # seperate between leagues and cups
            if j != len(self.CountriesLeagues)-1:
                print("-"*15) # seperate between countries

    # get matches by league    
    def get_matches_info_by_league(self):
        self.parseLeagues()
        leagues_found = {league: False for league in self.leagues} # check if the league is found or not to print a message
        # get the data of each league
        for row in self.tables:
            league_title = row.find('a')
            if (league_title.text in self.leagues or self.searchmethod == "all"):
                if league_title.text == "Serie A":      # corner case: italian and and ecuadorian leagues have the same name
                    country_name = row.find("h2").find("span", {"class" : "f-i"}) 
                    if country_name.text == "ec":
                        continue
                if self.searchmethod == "league":       # corner case: some women and men leagues have the same name, so print any of them, probably men
                    if leagues_found[league_title.text]:
                        continue
                leagues_found[league_title.text] = True
                print(Fore.CYAN + league_title.text)
                print("-"*15)
                matches = row.find_all("tr")
                matches.pop(0) # keys row
                self.get_matches_info(matches)
                print()
        # print a message if the league is not found
        if self.searchmethod == "league":
            for league in self.leagues:
                if not leagues_found[league]:
                    print(Fore.RED + f"No matches found on {self.date} for " + league)
                    print(end="-"*15)
                    print()
    # main function
    def run(self):
        init(autoreset=True)
        self.sendRequest()
        print(Fore.YELLOW + f"Matches on {self.date}:", end="\n"*2)
        if self.searchmethod == "league" or self.searchmethod == "all":
            self.get_matches_info_by_league()
        else:
            self.get_matches_info_by_country()
