# Futbl
## A Command-Line Interface to scrap football data from [fbref](https://fbref.com/en/matches/) and present it by **league**, **country**, or **all**.
## Usage
``` 
Usage: main.py [-h] [-l [{Serie,Liga,Ligue,Bundesliga,Premier} ...]]
               [-c [{Italy,Spain,France,Germany,England} ...]] [-a]
               date

A CLI program to fetch the match schedules of a date of your choice
from fbref Website

positional arguments:
  date                  Date formated as "YY-MM-DD"

options:
  -h, --help            show this help message and exit
  -l [{Serie,Liga,Ligue,Bundesliga,Premier} ...], --league [{Serie,Liga,Ligue,Bundesliga,Premier} ...]
                        a league to display its results
  -c [{Italy,Spain,France,Germany,England} ...], --country [{Italy,Spain,France,Germany,England} ...]
                        a country to display the results of all its
                        leagues and cups (this will overwrite the
                        league)
  -a, --all             display all the results of all leagues and
                        cups (this will overwrite the league and
                        country)
```
## CLI in action
![alt text](images/Schedule_England_Feb28.png)
