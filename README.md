# swiss-tournament
tournament.sql : Creates all the relations and views required to run the code.

tournament.py: Presents an interface to interact with the database and run queries on various relations. 
               Uses psycopg2 module.
               
tournament_test.py: Presents some tests to check the various functions as given
                    by Udacity.

tournament_software.py: Its a CLI which lets you access the database.

schema.jpg: Entity relationship diagram to give the better picture of the database design.



Steps to run the software:

1. Run tournament.sql.

2. Run tournament_software.py

3. On command line, you will be presented with 'tournament' menu. You can create/delete/access

   any particular tournament.
   
4. Working on a particular tournament lets you access:

   a.'Team' Menu
   
   b. 'Player' Menu
   
   c. 'Match' Menu
   
   consecutively.
 
Rules:

1. This is a swiss style tournament. There is no elimination.

2. Each tournament consists of EVEN number of teams.

3. You can't register a player if his/her team is not registered.

4. Each team should have equal number of players.

5. You can't schedule/pair matches if the teams are not even or 
   players in each team are not equal.
   
6. There will be log(total no of players) (base 2) rounds. Each round
   is scheduled after the previous round finishes.
   
7. The point is rewarded as follows:

   Win: 3
   
   Loss: 0
   
   Draw: 1


Upcoming features:

1. Update feature from command line.

2. More error handling.

3. More user friendly interface.


Note:

a. I tested the project to the best of my knowledge. Feel free
   to report any bugs.
   
Credits: 

a. I have used texttable module designed by author Gerome Fournier.
