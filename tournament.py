#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("host= 'localhost' user= 'arunimasrivastava'  dbname = 'tournament' ")



def deleteTournament():
    """Remove all the tournaments records"""
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM swiss_tournament.tournament;")
    conn.commit()
    cur.close()
    conn.close()
    
def deleteTeams():
    """Remove all the teams records"""
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM swiss_tournament.teams;")
    conn.commit()
    cur.close()
    conn.close()
    
def deletePlayers():
    """Remove all the player records from the database."""
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM swiss_tournament.player_info;")
    conn.commit()
    cur.close()
    conn.close()
    


def deleteMatches(tournamentId, matchId = None):
    """Remove all the match records from the database. Deleting this automatically deletes all the records in 
    'match' table as per the cascade deletion 
    ARGS:
    tournamentId: used to delete the matches from a particular tournament(mandatory)
    matchId: used to delete a particular match"""
    
    if matchId is not None:
        # In this case, user wants to delete one particular match
        # the tournament_id passed in this argument is of no use.
        # This case again has two other cases when the match is draw
        # and when the match has a clear winner.
        
        query = "SELECT is_draw FROM swiss_tournament.match where id = %s;"
        data = (matchId,)
        conn = connect()
        cur = conn.cursor()
        cur.execute(query, data)
        is_draw = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close() 
        
        if is_draw:
            # match draw
            query = """SELECT first_player, second_player
                       FROM
	               swiss_tournament.match_schedule e
                       WHERE id = %s;"""
            conn = connect()
            cur = conn.cursor()
            cur.execute(query, data)
            row = cur.fetchone()
            first_player = row[0]
            second_player = row[1]
            conn.commit()
            cur.close()
            conn.close() 
            
            query = """UPDATE swiss_tournament.player_stats SET draws = draws - 1,
                       total_points = total_points - 1
                       WHERE id IN(%s, %s);"""
            data = (first_player, second_player)
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
            cur.close()
            conn.close()            
        else:
            # clear winner
            query = """SELECT winner, loser
                       FROM swiss_tournament."match" e
                       WHERE id = %s;"""
            data = (matchId,)
            conn = connect()
            cur = conn.cursor()
            cur.execute(query, data)
            row = cur.fetchone()
            winner = row[0]
            loser = row[1]
            conn.commit()
            cur.close()
            conn.close()
            conn = connect()
            query = """UPDATE swiss_tournament.player_stats
                       SET  wins = CASE 
                       WHEN id = %s THEN wins - 1
                       WHEN id = %s THEN wins
                       END,
                       losses = CASE
                       WHEN id = %s THEN losses
                       WHEN id = %s THEN losses - 1
                       END,
                       total_points = CASE
                       WHEN id = %s THEN  total_points - 3 
                       WHEN id = %s THEN total_points
                       END
                       WHERE id IN(%s, %s);
                    """
            data = (winner, loser, winner, loser, winner, loser, winner, loser)
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
            cur.close()
            conn.close() 
    else:
        query = """UPDATE swiss_tournament.player_stats SET wins = 0,
                    losses = 0, draws = 0, total_points = 0
                       FROM   swiss_tournament.player_stats ps 
                         INNER JOIN swiss_tournament.player_info pi ON ( ps.id = pi.id  )  
                           INNER JOIN swiss_tournament.teams t ON ( pi.team_id = t.id  )  
                              WHERE tournament_id = %s;"""
        data = (tournamentId,)
        conn = connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()        
        
        conn = connect()
        cur = conn.cursor()
        query = "DELETE FROM swiss_tournament.match_schedule WHERE tournament_id = %s;"
        data = (tournamentId,)
        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()


def deleteAllMatches():
    """ Delete all the match records irrespective of particular tournament.
        This in return cascade delete 'match' relation's rows too. """
    conn = connect()
    cur = conn.cursor()
    query = "DELETE FROM swiss_tournament.match_schedule;"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()    
    


def deleteCountry():
    """Removes all the country details. Country id is foreign key to two tables 'Tournament' and 'Team' 
    Deletion is only possible when there is no data in those table"""
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM swiss_tournament.country;")
    conn.commit()
    cur.close()
    conn.close()    
    


def countPlayers(tournamentId):
    """Returns the number of players currently registered."""
    
    conn = connect()
    cur = conn.cursor()
    query = """SELECT count(*)
       FROM
           swiss_tournament.player_info o, swiss_tournament.teams t
       WHERE 
           o.team_id = t.id 
       AND
           t.tournament_id = %s ;"""
    
    cur.execute(query, (tournamentId,))
    player_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    return player_count
    
    
    
    
def registerCountry(name):
    "Registers the country names belonging to various participating teams and players"
    
    query = """SELECT name
               FROM swiss_tournament.country y;"""
    
    conn = connect()
    cur = conn.cursor()
    cur.execute()
    country_list = cur.fetchall()
    cur.close()
    conn.close()
    
    countryExists = False
    for row in coutry_list:
        if name == row[0]:
            countryExists = True
            break
    if countryExists:
        query = """SELECT id
                   FROM swiss_tournament.country y
                   WHERE name = %s; """
        data = (lower(name.title()),)
        cur.execute(query, data)
        country_id = cur.fetchone()[0]
        conn.commit()
        conn.close()        
    else:
        query = "INSERT INTO swiss_tournament.country( name) VALUES ( %s ) RETURNING id;"
        cur.execute(query, (name.title(), ))
        country_id = cur.fetchone()[0]
        conn.commit()
        conn.close()        
        
    return country_id    
    
    

def registerTournament(name, start_date, country_id):
    """ Adds a tournament into the database. 
    Args:
    name: Name of the tournament (mandatory)
    start_date: The date when the tournament begins
    country_id: the Id of the country where it is taking place.(mansatory)
    
    Returns the tournament Id of the currently registered tournament"""
    
    conn = connect()
    cur = conn.cursor()
    query = "INSERT INTO swiss_tournament.tournament (start_date, name, origin_country) VALUES (%s, %s, %s) RETURNING id;"
    cur.execute(query, (start_date, name, country_id))
    tournament_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return tournament_id




def registerTeam(name, tournament_id, country_id ):
    """ Registers a particular team and returns its ID
    Args: 
    name: Team name (mandatory)
    tournament_id: (mandatory
    country_id: The country name where it belongs(mandatory)"""
    
    conn = connect()
    cur = conn.cursor()
    query = "INSERT INTO swiss_tournament.teams( tournament_id, name, country) VALUES (%s, %s, %s) RETURNING id;"
    cur.execute(query, (tournament_id, name, country_id))
    team_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return team_id    
    
    


def registerPlayer(name, team_id):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    full_name = name.split()
    first_name = full_name[0]
    if len(full_name) == 2:
        last_name = full_name[1]
        query = "INSERT INTO swiss_tournament.player_info( first_name, last_name, team_id) VALUES (  %s, %s, %s ) RETURNING id;"
        data = ( first_name, last_name, team_id)
    else:
        query = "INSERT INTO swiss_tournament.player_info( first_name, team_id) VALUES (  %s, %s) RETURNING id;"
        data = ( first_name, team_id)
    
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, data)
    player_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    
    query = "INSERT INTO swiss_tournament.player_stats( id, wins, losses, draws, total_points) VALUES (%s, %s, %s, %s, %s);"
    data = (player_id, 0, 0, 0, 0)
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    cur.close()
    conn.close()    
    

def registerMatch(tournament_id, first_player, second_player, match_date):
    """ Registers a match in 'match_schedule' relation. This query 
     just registers a match its occurence and results is recorded in 'match' relation
     which is updated in reportMatch() function."""
    
    query = """INSERT INTO swiss_tournament.match_schedule
	(tournament_id, first_player, second_player, match_date) VALUES ( %s, %s, %s, %s) RETURNING id;"""
    data = (tournament_id, first_player, second_player, match_date)
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, data)
    match_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return match_id
    
    


def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    
    conn = connect()
    cur = conn.cursor()
    query = """ SELECT id, first_name, last_name, wins, matches 
                FROM swiss_tournament.player_standings
                WHERE tournament_id = %s """
    data = (tournament_id,)
    cur.execute(query, data)
    players_list = []
    for row in cur.fetchall():
        players_list.append(row)
    conn.close()
    return players_list
    
    
    


def reportMatch(winner, loser, matchId):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      
    Here, two cases arises, first when match has got the result and second
    when its draw. In each case we are updating two tables namely 'player_stats' 
    and 'match'. I assume that whenever a match is draw winner and loser arguments 
    are passed as NULL. 
     
    We don't need a tournament id here as there is no chance that for two tournaments
    there is one player with same id.
    """
    if(winner is not None):
        #Match is not draw therefore the 'match' relation's 'is_draw'
        #column is automatically set to False 
        
        query = """INSERT INTO swiss_tournament."match"
	         ( id, winner, loser) VALUES ( %s, %s, %s);"""
        
        data = (matchId, winner, loser)
        conn = connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()        
        
        
        query = """UPDATE swiss_tournament.player_stats
        SET  wins = CASE 
               WHEN id = %s THEN wins + 1
               WHEN id = %s THEN wins
             END,
             losses = CASE
               WHEN id = %s THEN losses
               WHEN id = %s THEN losses +1
             END,
             total_points = CASE
               WHEN id = %s THEN  total_points + 3 
               WHEN id = %s THEN total_points
             END
        WHERE id IN(%s, %s);
        """        
        data = (winner, loser, winner, loser, winner, loser, winner, loser)
        conn = connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()
    else:
        
        # In case, match is draw then 'isDraw' column of 'match' relation
        # will automaticaly be set to true and there is no winner
        # hence, winner is null
        
        query = """INSERT INTO swiss_tournament."match"
                         ( id, winner) VALUES ( %s);"""
                
        data = (matchId)
        conn = connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()        
        
        query = """UPDATE swiss_tournament.player_stats
                SET  draws = CASE 
                       WHEN id = %s THEN draws + 1
                       WHEN id = %s THEN draws + 1
                     END,
                     total_points = CASE
                       WHEN id = %s THEN total_points + 1 
                       WHEN id = %s THEN total_points + 1
                    END
                WHERE id IN(%s, %s);
                """        
        data = (winner, loser, winner, loser, winner, loser, winner, loser)
        conn = connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        cur.close()
        conn.close()        
        
    
    
 
 
def swissPairings( tournamentId):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    # This database design requires to have any even number of teams
    # with equal amount of players without which pairing can not be done.
    # The below query obtains the total number of teams.
    query = """SELECT count(id)
             FROM swiss_tournament.teams s
             WHERE tournament_id = %s;"""
    data = (tournamentId,)
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, data)
    count = cur.fetchone()
    cur.close()
    conn.close() 
    if (int(count[0]) % 2 == 0):
        # If there are even number of teams. Then we need to check if 
        # there are equal number of players in each team. The following
        # query fetches the number of players in each team.
        
        query = """SELECT count(id)
                       FROM swiss_tournament.player_standings
                       WHERE tournament_id = %s
                       GROUP BY team_id;"""
        data = (tournamentId,)
        conn = connect()
        cur = conn.cursor()
        cur.execute(query, data)
        
        team_counts = []
        for row in cur.fetchall():
            team_counts.append(row[0])
        
        cur.close()
        conn.close()
        
        if all_same(team_counts):
            # if there are equal number of players then we can pair the 
            # players.
            query = """ SELECT id, first_name, last_name, team_id 
                        FROM swiss_tournament.player_standings
                        WHERE tournament_id = %s"""
            data = (tournamentId,)
            conn = connect()
            cur = conn.cursor()
            cur.execute(query, data)
            players = []
            for row in cur.fetchall():
                players.append(list(row))
        
            pairings = []
            players_ids = []
            for index, row in enumerate(players):
                if(row[0] not in players_ids):
                    for item in players[index+1:]:
                        if(row[2] != item[2] and (item[0] not in players_ids)):
                            players_ids.append(item[0])
                            players_ids.append(row[0])
                            pair = (row[0], row[1], row[2], item[0], item[1], item[2])
                            pairings.append(pair)
                            break
            return pairings 
        else:
            raise ValueError("Players in each team are not equal")
    
    else:
        raise ValueError("There are odd numbers of teams")
    
    


def isTournament(tournamentId):
    query = """SELECT id, name
               FROM swiss_tournament.tournament t
               WHERE id = %s;
            """
    data = (tournamentId,)
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, data)
    id_list = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()  
    if id_list:
        return id_list
    else:
        return False
    



def displayTournaments():
    query = """SELECT t.id, t.name, t.start_date,  c1.name
               FROM swiss_tournament.tournament t 
	       INNER JOIN swiss_tournament.country c1 ON ( t.origin_country = c1.id  )  
                """
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    id_list = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close() 
    return id_list 
    
    
    




def all_same(items):
    return all(x == items[0] for x in items)




