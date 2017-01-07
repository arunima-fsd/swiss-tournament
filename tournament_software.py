import datetime
import texttable as tt
import math
from tournament import *




def welcomeScreen():
    print "*** Welcome to the Swiss Tournament Software."
    tournamentChoice()






def tournamentOptions(choice):
    if choice == '1':
        createTournament()
        tournamentChoice()

    elif choice == '2':
        while(True):
            try:
                tournamentId = int(raw_input("*** Enter your tournament ID: "))
                break
            except ValueError:
                print "Oops!  That was no valid number.  Try again..."  
                
        tournament_name = isTournament(tournamentId)
        if tournament_name:
            print ("*** Access to '%s' database is granted.")%(tournament_name[1])
            teamsChoice(tournamentId)
        else:
            print "*** No tournament with id = %s exists."%(tournamentId)
            tournamentChoice()
            
    elif choice == '3':
        showTournaments()
        tournamentChoice()
        
    elif choice == '4':
        tournamentId = raw_input("**** Enter the tournament Id you want to delete")
        delete_tournament(tournamentId)
        
    elif choice == '5':
        user_input = raw_input("*** Warning: This action will delete all the tournament's information. Continue? Y/N ")
        if user_input in ['Y' , 'y']:
            delete_tournament()
        elif user_input in ['N', 'n']:
            tournamentChoice()
        else:
            print "*** Wrong Choice"
            tournamentChoice()

    else:
        print "*** You have entered a wrong choice."
        tournamentChoice()
        
       
       
        
        
def teamOptions(choice, tournamentId):
    if choice == '1':
        createTeam(tournamentId)
        teamsChoice(tournamentId)
        
    elif choice == '2':
        showTeams(tournamentId)
        teamsChoice(tournamentId)
        
    elif choice == '3':
        teamId = raw_input("*** Enter the ID of the team you wish to delete. ")
        if isTeam(teamId):
            deleteOneTeam(teamId)
            print "*** Successfully deleted the team."
            teamsChoice(tournamentId)
        else:
            print "*** No such team exists. "
            teamsChoice(tournamentId)
    elif choice == '4':
        if isTournament(tournamentId):
            deleteTeams(tournamentId)
            print "*** Successfully deleted the team."
            teamsChoice(tournamentId)            
            
        else:
            print "*** No such tournament exists. "
            teamsChoice(tournamentId) 
            
    elif choice == '5':
        playersChoice(tournamentId)
        
    elif choice == '6':
        tournamentChoice()
    else: 
        print "*** You have entered a wrong option."
        teamsChoice(tournamentId)
            



def playerOptions(choice, tournamentId):
    if choice == '1':
        name = raw_input("*** Enter player's full name. (<first name> <last name>): ")
        
        while(True):
            while(True):
                try:
                    team_id = int(raw_input("*** Enter the team id he/she represents: "))
                    break
                except ValueError:
                    print "Oops!  That was no valid number.  Try again..." 
            
            if isTeam(team_id):
                registerPlayer(name, team_id)
                break
            else:
                print "Oops! You have entered a wrong team. Try again..."
                print "There are currently following teams in the database."
                showTeams(tournamentId)
            
        print ("*** %s is successfully registered. ")%(name.title())
        playersChoice(tournamentId)
        
    elif choice == '2':
        showPlayers(tournamentId)
        playersChoice(tournamentId)
    
    elif choice == '3':
        while(True):
            try:
                player_id = raw_input("*** Enter player's Id.")
                break
            except ValueError:
                print "Oops!  That was no valid number.  Try again..."         
        
        if isPlayer(player_id):
            deletePlayers(tournamentId, player_id)
        else:
            print "*** No such player exists. "
        playersChoice(tournamentId)
        
    elif choice == '4':
        deletePlayers(tournamentId)
        print "*** Successful Deletion"
        playersChoice(tournamentId)
    
    elif choice == '5':
        matchesChoice(tournamentId)
    
    elif choice == '6':
        teamsChoice(tournamentId)
    
    else:
        print "*** Oops! Wrong Choice"
        playersChoice(tournamentId)
        


def matchesOptions(choice, tournamentId):
    if choice == '1':
        showMatchesSchedule(tournamentId)
        matchesChoice(tournamentId)
        
    elif choice == '2':
        if isScheduleExists(tournamentId):
            result = raw_input("Hit 'D' if match is draw else hit 'N' ")
            if result in ['D', 'd']:
                while(True):
                    try:
                        match = int(raw_input("*** Enter match id. "))
                        break
                    except ValueError:
                        print "Oops!  That was no valid number.  Try again..." 
                if isMatch(match):
                    reportMatch(match)
                    print "*** Match report successfully saved."
                else:
                    print "Invalid Match ID." 
                
            elif result in ['N', 'n']:
                createMatchReport()
                print "*** Details Saved."
            else:
                print "**** Invalid Choice" 
        else:
            print "**** Please Schedule the matches first"
        matchesChoice(tournamentId)

    
    elif choice == '3':
        playersCount = countPlayers(tournamentId)
        max_round = math.ceil(math.log(playersCount,2))
        while(True):
            try:
                round_no = int(raw_input("*** Enter the round. "))
                break
            except ValueError:
                print "Oops!  That was no valid number.  Try again..." 
        if round_no > 0:
            if round_no <= max_round:
                rounds = getAllRounds(tournamentId)
                temp_round = []
                for row in rounds:
                    temp_round.append(row[0])
                    
                if round_no == 1 and round_no not in temp_round:
                    createMatches(tournamentId, round_no)
                    print "**** Successfully Scheduled"
                    
                elif round_no != 1:
                    if isRoundFinished(tournamentId):
                        createMatches(tournamentId, round_no)
                        print "*** Scheduled Successfully!!"
                    else:
                        print "*** Can't schedule until all the matches are finished"            
                elif round_no in temp_round :
                    print "*** Pairing for this round is already done"
            else:
                print ("*** Exceeded the number of rounds allowed. Maximum %s rounds allowed for %s players")%(max_round, playersCount)
        else:
            print "*** Invalid round"
            
        matchesChoice(tournamentId)
        
    elif choice == '4':
        while(True):
            try:
                matchId = int(raw_input("*** Enter the match ID "))
                break
            except ValueError:
                print "Oops!  That was no valid number.  Try again..." 
        if isMatch(matchId):
            deleteMatches(tournamentId, matchId)
            print "*** Match successfully deleted."
        else:
            print "*** Invalid Match Id"
        matchesChoice(tournamentId)
    elif choice == '5':
        deleteMatches(tournamentId)
        print "*** Successfully deleted all the matches."
        matchesChoice(tournamentId)
            
    elif choice == '6':
        playersChoice(tournamentId)
    
    else:
        print "*** Invalid choice."
        matchesChoice(tournamentId)
        
    
    
    
    
        
        
    
# #########################################################################



def createTournament():
    name = raw_input("*** Please enter the tournament name. ")
    start_date = raw_input("*** Please enter the start date of the tournament. (yyyy-mm-dd) ")
    country = raw_input("*** Please enter the country name of the venue. ")
    country_id = registerCountry(country)
    tournament_id = registerTournament(name, start_date, country_id)
    print ("*** Your new %s is successfully created. ")%(name)
    print ("*** Tournament id: %s")%(tournament_id)
    print ("*** Please make a note of it.")
    




def createTeam(tournament_id):
    name = raw_input("*** Please enter the team name. ")
    country = raw_input("*** Please enter the country it represents. ")
    country_id = registerCountry(country)
    tournament_id = registerTeam(name, tournament_id, country_id) 
    print ("*** Your new %s team is successfully created. ")%(name)
    print ("*** The team id is: %s")%(tournament_id)


        

def createMatches(tournamentId, round_no):
    if scheduleMatches(tournamentId, round_no):
        print "*** Matches Scheduled Successfully"
    else:
        print "*** No players to schedule Matches"    
    

def createMatchReport():
    while(True):
        while(True):
            try:
                winner = int(raw_input("*** Enter winner id. "))
                break
            except ValueError:
                print "Oops!  That was no valid number.  Try again..." 
        if isPlayer(winner):
            while(True):
                try:
                    loser = int(raw_input("*** Enter loser id. "))
                    break
                except ValueError:
                    print "Oops!  That was no valid number.  Try again..." 
            if isPlayer(loser):
                while(True):
                    try:
                        match = int(raw_input("*** Enter match id. "))
                        break
                    except ValueError:
                        print "Oops!  That was no valid number.  Try again..." 
                if isMatch(match):
                    break
                else:
                    print "Invalid Match ID."
                    
            else:
                print "Invalid Id"
        else:
            print "Invalid Winner Id"
    reportMatch(match, winner, loser)
                
            
       
    


# ####################################################################

    
    
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

    
    
    
        
        
def showTeams(tournamentId):
    
    team_list = displayTeams(tournamentId)
    if(team_list):
        tab = tt.Texttable()
        header = ['ID', 'Name', 'Country']
        tab.header(header)
        for row in team_list:
            tab.add_row(list(row))
            tab.set_cols_width([5,35,15])
            tab.set_cols_align(['c', 'c', 'c'])
            tab.set_cols_valign(['m', 'm', 'm'])
        s = tab.draw()
        print s
    else:
        print "*** There are no teams entry in database to show."
        

def showPlayers(tournamentId):
    players_list = displayPlayers(tournamentId)
    if(players_list):
        tab = tt.Texttable()
        header = ['ID', 'First Name', 'Last Name', 'Team Id', 'Matches', 'Wins', 'Losses', 'Draws', 'Total Points']
        tab.header(header)
        for row in players_list:
            tab.add_row(list(row))
            tab.set_cols_width([5, 20, 20, 5, 5, 5, 5, 5, 5])
            tab.set_cols_align(['c', 'c', 'c','c', 'c', 'c','c', 'c','c'])
            tab.set_cols_valign(['m', 'm', 'm','m', 'm', 'm', 'm', 'm', 'm'])
        s = tab.draw()
        print s  
    else:
        print "*** There are no players to show."
   
    
    
def showMatchesSchedule(tournamentId):
    matches_list = displayMatches(tournamentId)
    if(matches_list):
        tab = tt.Texttable()
        header = ['Match Id', 'Player Id', 'Name', 'Player Id', 'Name', 'Match Date', 'Finished']
        tab.header(header)
        
        for row in matches_list:
            if row[8] == 0:
                temp = "No"
            elif row[8] == 1:
                temp = "Yes"
            mod_row = [row[0], row[1], row[2].strip() + " " + row[3].strip(), row[4], row[5].strip() + " " + row[6].strip(), row[7], temp]
            tab.add_row(list(mod_row))
            tab.set_cols_width([10, 10, 20, 10 , 20, 8, 5])
            tab.set_cols_align(['c', 'c', 'c','c', 'c', 'c','c'])
            tab.set_cols_valign(['m', 'm', 'm','m', 'm', 'm', 'm'])
        s = tab.draw()
        print s  
    else:
        print "*** There are no matches scheduled. Please schedule it for each round."    
    
            
    
# #################################################################



def delete_tournament(tournamentId = None):
    if tournamentId:
        deleteTournament(tournamentId)
        print "*** Successfully deleted the tournament."
    else:
        deleteTournament()
        print "*** Successfully deleted all the tournaments."
    tournamentChoice()







# ##################################################################

def tournamentChoice():
    print "-" * 80
    print "*** 1. CREATE  NEW tournament."
    print "*** 2. WORK on EXISTING tournament."
    print "*** 3. BROWSE existing tournaments."
    print "*** 4. DELETE a tournament."
    print "*** 5. DELETE ALL the tournaments "
    print "-" * 80
    choice = raw_input()
    tournamentOptions(choice)
    
    

def teamsChoice(tournamentId):
    print "-" * 80
    print "*** 1. CREATE a new team."
    print "*** 2. BROWSE existing teams."
    print "*** 3. DELETE a team."
    print "*** 4. DELETE ALL teams of one particular tournament."
    print "*** 5. PLAYERS menu"
    print "*** 6. TOURNAMENT menu"
    print "-" * 80
    choice = raw_input()
    teamOptions(choice,tournamentId)


def playersChoice(tournamentId):
    print "-" * 80
    print "*** 1. REGISTER a player in some team."
    print "*** 2. BROWSE existing players"
    print "*** 3. DELETE ONE player"
    print "*** 4. DELETE ALL players"
    print "*** 5. MATCHES Menu "
    print "*** 6. TEAMS Menu"
    print "-" * 80
    choice = raw_input()
    playerOptions(choice, tournamentId)
    


def matchesChoice(tournamentId):
    print "-" * 80
    print "*** 1. MATCH SCHEDULE"
    print "*** 2. REGISTER match RESULT"
    print "*** 3. SCHEDULE next round matches"
    print "*** 4. DELETE match"
    print "*** 5. DELETE ALL matches "
    print "*** 6. PLAYERS Menu"
    print "-" * 80
    choice = raw_input()
    matchesOptions(choice, tournamentId)    
    
    


# ####################################################################

welcomeScreen()




        

        
    
    
    





