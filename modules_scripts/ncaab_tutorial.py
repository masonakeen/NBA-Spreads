# %%
# We're importing the teams and conferences modules from within the NCAAB package in the SportsIPY API
# Modules are basically collections of predefined functions and classes that we can use instead of writing 
#   them ourselves
# In order to do something with the functions and classes, we need to call them. This is called instantition
# 
# You call classes by creating an object that instiates the class. 
#     x = Teams()    <-- this calls the Teams class and now every time you call x, it'll reflect the 
#                        code within the Teams class
# You have class objects, function objects, and method objects
#   Class Object
#   Function Objects: called by specifying the class and function (e.g. Conferences.team_conference)
#   Method Objects are just Function objects that are part of a class


#Import Teams module, which contains a bunch of classes
from sportsipy.ncaab.teams import *
# This distinction is important - there is a class Teams in the Teams module
from sportsipy.ncaab.teams import Teams 

from sportsipy.ncaab.conferences import Conferences

# Creating an object that represents the Teams class - calling the Teams class returns a bunch of info
# about all 300-some teams. It includes stuff like name, assists, conference, etc.
teams = Teams()

# A team is a variable that we've just declared. It can be i, j, zebra for all we care
# the Teams module lets us connect to the database table/matrix that the API shields
# name is a function that we are able to call 
for team in teams:
    print(team.name)




# %%
# Our goal is to use this API to pull grab data using Python, which typically comes back to us as a JSON dictionary
# Dictionaries are basically key:value pairs of data, and can be manipulated as such.
# In this case, the dictionary is basically a team:X, schedule: x, year: x, etc
# Counting the number of teams in the dictionary using len is a good test 

from sportsipy.ncaab.teams import *

teams = Teams()

print(len(teams))

# we can expand our data pull to include additional values from the dictionary if we specify more keys:
for team in teams:
    print(team.name, team.abbreviation, sep=" ")


# %%
# Getting an entire dictionary is great, but how do we extract the valuable data?

# Let's choose a season and print out all its methods and properties
# Specifying a parameter allows us to get away from the default for this class, which is the current year
teams2010 = Teams(year='2010')
print(len(teams))
print(len(teams2010))

# We can see that dataframees is the only public property of the Teams class
# It's basically a dataframe where every NCAAB team is represented by a row
print(dir(teams2010))

# %%
# Now, let's incorporate a different module - we have only dealt with Teams up to now
from sportsipy.ncaab.schedule import Schedule

#Create an instance of the class for the Hokies' 2019 season and return a dataframe with basic game info
hokiesSchedule = Schedule('VIRGINIA-TECH',year = '2019')
hokiesSchedule.dataframe.head()
#Once we create this dataframe, we can reference it whenever we want to in our code and it's much faster
wins = 0
losses = 0
for game in hokiesSchedule:
    if game.result == 'Win':
        wins = wins + 1
    else: losses = losses + 1

print("Record: " ,wins, losses, sep="-")

# %%
# games in Schedule are indexed by boxscore URI. We can use that with the Boxscore class to get more detail
hokiesSchedule.dataframe.head()

from sportsipy.ncaab.boxscore import Boxscore
game_data = Boxscore('2018-11-09-19-virginia-tech')

game_data.dataframe

# Let's keep digging towards a full traditioanl box score

# %%




