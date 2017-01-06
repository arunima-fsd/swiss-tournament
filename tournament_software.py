import datetime
import texttable as tt
from tournament import *



tournamentId = None
def welcomeScreen():
    print "*** Welcome to the Swiss Tournament Software."
    tournamentChoice()






def tournamentOptions(choice):
    print choice
    if choice == '1':
        createTournament()

    elif choice == '2':
        tournamentId = raw_input("*** Enter your tournament id. ")
        tournament_name = isTournament(tournamentId)
        if tournament_name:
            print ("*** Access to '%s' database is granted.")%(tournament_name[1])
        else:
            print "*** No tournament with id = %s exists."%(tournamentId)
            tournamentChoice()
    elif choice == '3':
        showTournaments()
    else:
        print "*** You have entered a wrong choice."
        
        
        





def createTournament():
    name = raw_input("*** Please enter the tournament name. ")
    start_date = raw_input("*** Please enter the start date of the tournament. ")
    country = raw_input("*** Please enter the country name of the venue. ")
    country_id = registerCountry(country)
    tournament_id = registerTournament(name, start_date, country_id)
    print ("*** Your new %s is successfully created. ")%(name)
    print ("*** The tournament id is: %s")%(tournament_id)
    print ("*** Please make a note of it.")
    
    
def showTournaments():
    tournament_list = displayTournaments()
    if(tournament_list):
        tab = tt.Texttable()
        header = ['ID', 'Name', 'Start date', 'Country']
        tab.header(header)
        for row in tournament_list:
            tab.add_row(list(row))
        tab.set_cols_width([5,35,15,18])
        tab.set_cols_align(['c', 'c', 'c', 'c'])
        tab.set_cols_valign(['m', 'm', 'm', 'm'])
        s = tab.draw()
        print s
    else:
        print "*** There are no tournaments in database to show."
    tournamentChoice()
        
        


def tournamentChoice():
    print "*** Press 1 to create a new tournament."
    print "*** Press 2 to work on existing tournament."
    print "*** Press 3 to browse existing tournaments."
    choice = raw_input()
    tournamentOptions(choice)
    
    

    




welcomeScreen()
deleteTournament()



        

        
    
    
    



def all_same(items):
    return all(x == items[0] for x in items)