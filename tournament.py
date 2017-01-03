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
    


def deleteMatches():
    """Remove all the match records from the database. Deleting this automatically deletes all the records in 
    'match' table as per the cascade deletion """
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM swiss_tournament.match_schedule;")
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
    conn = connect()
    cur = conn.cursor()
    query = "INSERT INTO swiss_tournament.country( name) VALUES ( %s ) RETURNING id;"
    cur.execute(query, (name, ))
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
        query = "INSERT INTO swiss_tournament.player_info( first_name, last_name, team_id) VALUES (  %s, %s, %s );"
        data = ( first_name, last_name, team_id)
    else:
        query = "INSERT INTO swiss_tournament.player_info( first_name, team_id) VALUES (  %s, %s);"
        data = ( first_name, team_id)
    
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    cur.close()
    conn.close()


def playerStandings():
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


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swissPairings():
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


