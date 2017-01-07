#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

import datetime
from tournament import *

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    
    country_id = registerCountry("India")
    start_date = datetime.date.today()
    tournament_id = registerTournament('Test', start_date , country_id)
    c = countPlayers(tournament_id)
    
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."
    
    
    team_id = registerTeam('Test Team 2', tournament_id, country_id)
    registerPlayer("Chandra Nalaar", team_id)
    c = countPlayers(tournament_id)
    
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "2. countPlayers() returns 1 after one player is registered."
    
    
    team_id = registerTeam('Test Team 2', tournament_id, country_id)
    registerPlayer("Jace Beleren", team_id)
    c = countPlayers(tournament_id)
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    
    deletePlayers(tournament_id)
    c = countPlayers(tournament_id)
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."
    
    deleteTournament()
       
    
    
    
    

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    
    country_id = registerCountry("India")
    start_date = datetime.date.today()
    tournament_id = registerTournament('Test', start_date , country_id) 
    team_a = registerTeam('Test Team 2', tournament_id, country_id)
    team_b = registerTeam('Test Team 3', tournament_id, country_id)                      
    registerPlayer("Melpomene Murray", team_a)
    registerPlayer("Randy Schwartz", team_b)
    standings = playerStandings(tournament_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(id1, first_name1, last_name1, wins1, matches1), (id2, first_name2, last_name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    
    if set([first_name1.strip(), first_name2.strip(), last_name1.strip(), last_name2.strip()]) != set(["Melpomene", "Randy", "Murray", "Schwartz"]):


        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."
    
    deleteAllMatches()
    deletePlayers(tournament_id)    
    
    
    

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    
    deleteTournament()
    
    country_id = registerCountry("India")
    start_date = datetime.date.today()
    tournament_id = registerTournament('Test', start_date , country_id) 
    team_a = registerTeam('Test Team 2', tournament_id, country_id)
    team_b = registerTeam('Test Team 3', tournament_id, country_id)    
    
    registerPlayer("Bruno Walton", team_a)
    registerPlayer("Boots O'Neal", team_a)
    registerPlayer("Cathy Burton", team_b)
    registerPlayer("Diane Grant", team_b)
    
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    
    match_id1 = registerMatch(tournament_id, id1, id2, start_date)
    match_id2 = registerMatch(tournament_id, id3, id4, start_date)
    
    
    reportMatch(match_id1, id1, id2)
    reportMatch(match_id2, id3, id4)
    
    standings = playerStandings(tournament_id)
    
    for (i, fn, ln, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
        
    print "7. After a match, players have updated standings."
    
    
    deleteMatches(tournament_id, match_id1)
    deleteMatches(tournament_id, match_id2)
    standings = playerStandings(tournament_id)
    
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, fn, ln, w, m) in standings:
        if m != 0:
            
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."
    
    
    


def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    
    deleteTournament()
    
    country_id = registerCountry("India")
    start_date = datetime.date.today()
    tournament_id = registerTournament('Test', start_date , country_id) 
    team_a = registerTeam('Test Team 2', tournament_id, country_id)
    team_b = registerTeam('Test Team 3', tournament_id, country_id)
    team_c = registerTeam('Test Team 4', tournament_id, country_id)
    team_d = registerTeam('Test Team 5', tournament_id, country_id)    
    
    registerPlayer("Twilight Sparkle", team_a)
    registerPlayer("Fluttershy", team_b)
    registerPlayer("Applejack", team_c)
    registerPlayer("Pinkie Pie", team_d)
    registerPlayer("Rarity", team_a)
    registerPlayer("Rainbow Dash", team_b)
    registerPlayer("Princess Celestia", team_c)
    registerPlayer("Princess Luna", team_d)
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings(tournament_id)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    mi1 = registerMatch(tournament_id, id1, id2, start_date)
    mi2 = registerMatch(tournament_id, id3, id4, start_date)
    mi3 = registerMatch(tournament_id, id5, id6, start_date)
    mi4 = registerMatch(tournament_id, id7, id8, start_date)
    reportMatch(mi1, id1, id2)
    reportMatch(mi2, id3, id4)
    reportMatch(mi3, id5, id6)
    reportMatch(mi4, id7, id8)
    pairings = swissPairings(tournament_id)
    
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    
    [(pid1, fname1, lname1, pid2, fname2, lname2), (pid3, fname3, lname3, pid4, fname4, lname4), (pid5, fname5, lname5, pid6, fname6, lname6), (pid7, fname7, lname7, pid8, fname8, lname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
