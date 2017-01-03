-- Table definitions for the tournament project.
--



CREATE DATABASE tournament;

CREATE SCHEMA swiss_tournament;


-- 'country' stores the country names belonging to various teams and tournaments.
CREATE TABLE swiss_tournament.country ( 
        id                   serial  NOT NULL,
        name                 char(60)  NOT NULL,
        CONSTRAINT pk_country PRIMARY KEY ( id )
 );


-- 'tournament' table stores the information regarding a tournament in its begining.
CREATE TABLE swiss_tournament.tournament ( 
        id                   serial  NOT NULL,
        start_date           date DEFAULT current_date ,
        name                 varchar(100)  ,
        origin_country       integer  NOT NULL,
        CONSTRAINT pk_tournament PRIMARY KEY ( id ),
        CONSTRAINT fk_tournament_country FOREIGN KEY ( origin_country ) REFERENCES swiss_tournament.country( id ) ON DELETE RESTRICT ON UPDATE CASCADE
);


-- 'teams' table constitutes of the basic information related to each time. I assumed different sets of team participates in each tornament for 
-- less complexity.
CREATE TABLE swiss_tournament.teams ( 
        id                   serial  NOT NULL,
        tournament_id        integer  NOT NULL,
        name                 varchar(50)  ,
        country              integer  NOT NULL ,
        CONSTRAINT pk_teams PRIMARY KEY ( id ),
        CONSTRAINT fk_team_info_tournament FOREIGN KEY ( tournament_id ) REFERENCES swiss_tournament.tournament( id ) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT fk_teams_country FOREIGN KEY ( country ) REFERENCES swiss_tournament.country( id ) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE INDEX idx_team_info ON swiss_tournament.teams ( tournament_id );




-- 'player_info' table reflects the basic information about a player at the time of registration in the tournament.
CREATE TABLE swiss_tournament.player_info ( 
        id                   serial  NOT NULL,
        first_name           char(50)  NOT NULL,
        last_name            char(50)  ,
        team_id              integer  NOT NULL,
        CONSTRAINT pk_player_info PRIMARY KEY ( id ),
        CONSTRAINT fk_player_info_teams FOREIGN KEY ( team_id ) REFERENCES swiss_tournament.teams( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE INDEX idx_player_info_a ON swiss_tournament.player_info ( team_id );


-- 'tournament_stats' table stores the short statistics after each tournament gets over.
CREATE TABLE swiss_tournament.tournament_stats ( 
        id                   integer  NOT NULL,
        end_date             date DEFAULT current_date ,
        winner               integer  NOT NULL,
        CONSTRAINT pk_tournament_stats PRIMARY KEY ( id ),
        CONSTRAINT fk_tournament_stats FOREIGN KEY ( winner ) REFERENCES swiss_tournament.player_info( id ) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT fk_tournament_stats_tournament FOREIGN KEY ( id ) REFERENCES swiss_tournament.tournament( id )
        
 );

CREATE INDEX idx_tournament_stats ON swiss_tournament.tournament_stats ( winner );





-- 'player_stats' shows the performance of each player in the tournament. This table needs to be updated after each match.
CREATE TABLE swiss_tournament.player_stats ( 
        id                   integer  NOT NULL,
        wins                 integer DEFAULT 0 ,
        losses               integer DEFAULT 0 ,
        draws                integer DEFAULT 0 ,
        total_points         integer DEFAULT 0 ,
        CONSTRAINT pk_player_stats PRIMARY KEY ( id ),
        CONSTRAINT fk_player_stats_player_info FOREIGN KEY ( id ) REFERENCES swiss_tournament.player_info( id ) ON DELETE CASCADE ON UPDATE CASCADE

);



-- 'match_schedule' stores the pairing of two players in each round along with the match schedule. It should be updated after the end of each round.
-- If there are 2^n players, there must be n rounds.
CREATE TABLE swiss_tournament.match_schedule ( 
        id                   serial  NOT NULL,
        tournament_id        integer  NOT NULL,
        first_player         integer  NOT NULL,
        second_player        integer  NOT NULL,
        match_date           date  ,
        round                integer  ,
        isfinished           bool DEFAULT False ,
        CONSTRAINT pk_match_schedule PRIMARY KEY ( id ),
        CONSTRAINT fk_match_schedule_player_info FOREIGN KEY ( first_player ) REFERENCES swiss_tournament.player_info( id ) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT fk_match_schedule_player_info_a FOREIGN KEY ( second_player ) REFERENCES swiss_tournament.player_info( id ) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT fk_match_schedule_tournament FOREIGN KEY ( tournament_id ) REFERENCES swiss_tournament.tournament( id ) ON DELETE CASCADE ON UPDATE CASCADE

 );

CREATE INDEX idx_match_schedule_a ON swiss_tournament.match_schedule ( first_player );

CREATE INDEX idx_match_schedule_b ON swiss_tournament.match_schedule ( second_player );

CREATE INDEX idx_match_schedule ON swiss_tournament.match_schedule ( tournament_id );



-- 'match' stores the result of each match. The 'player_stats' table should be updated after each entry in this table.
CREATE TABLE swiss_tournament."match" ( 
        id                   integer  NOT NULL,
        winner               integer DEFAULT NULL ,
        is_draw              bool DEFAULT False NOT NULL,
        CONSTRAINT pk_match PRIMARY KEY ( id ),
        CONSTRAINT fk_match_match_schedule FOREIGN KEY ( id ) REFERENCES swiss_tournament.match_schedule( id ) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT fk_match_player_info FOREIGN KEY ( winner ) REFERENCES swiss_tournament.player_info( id ) ON DELETE CASCADE ON UPDATE CASCADE
        CONSTRAINT is_draw CHECK ( is_draw = CASE WHEN (winner IS NULL) THEN true ELSE false END ) 
);

CREATE INDEX idx_match ON swiss_tournament."match" ( winner );



CREATE MATERIALIZED VIEW standings
AS
SELECT ps.id, pi.first_name, pi.last_name, pi.team_id, t.tournament_id, ps.wins + ps.losses + ps.draws as matches, ps.wins, ps.losses, ps.draws, ps.total_points
FROM swiss_tournament.player_stats ps 
        INNER JOIN swiss_tournament.player_info pi ON ( ps.id = pi.id  )  
                INNER JOIN swiss_tournament.teams t ON ( pi.team_id = t.id  )  
ORDER BY total_points DESC
WITH [NO] DATA;











