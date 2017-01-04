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
    deleteAllMatches()
    deletePlayers()
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
    
    deletePlayers()
    c = countPlayers(tournament_id)
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."
    deleteTeams()
    deleteTournament()
    deleteCountry()
    
    
    
    

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteAllMatches()
    deletePlayers()
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
    
    
    
    
    

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteAllMatches()
    deletePlayers()
    deleteTeams()
    deleteTournament()
    deleteCountry()
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
    
    
    reportMatch(id1, id2, match_id1)
    reportMatch(id3, id4, match_id2)
    
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
    deleteAllMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
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
