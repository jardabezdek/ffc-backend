/*
Official NHL standings criteria: https://www.nhl.com/standings/

The standing of the clubs is determined in the following order:
	- points (descending),
	- games played (ascending),
	- games won, excluding games won in Overtime or by Shootout (descending),
	- games won, excluding games won by Shootout (descending),
	- games won in any manner (descending),
	- points earned in games against each other (descending), -- skipped in this implementation (!)
	- differential between goals for and against (descending),
	- goals scored (descending).
*/

with games as (

    select * from {{ ref("stg_standings_regular_games") }}

),

goals as (

    select * from {{ ref("stg_standings_regular_goals") }}

),

teams as (

	select * from {{ ref("dim_teams") }}

)

select 
    games.season,
	games.season_long,
    games.team_id,
	teams.team_full_name,
	teams.team_abbrev_name,
	games.games_played,
	games.wins,
	games.losses,
	games.ots,
	games.points,
	games.points_pct,
	games.wins_reg,
	games.wins_ot,
	games.wins_so,
	games.wins_reg_ot,
	games.losses_reg,
	games.losses_ot,
	games.losses_so,
	games.wins_home,
	games.losses_home,
	games.ots_home,
	games.wins_away,
	games.losses_away,
	games.ots_away,
	games.wins_last_10,
	games.losses_last_10,
	games.ots_last_10,
    goals.goals_for,
    goals.goals_against,
    goals.goals_diff,
	games.wins_home || '-' || games.losses_home || '-' || games.ots_home as record_home,
	games.wins_away || '-' || games.losses_away || '-' || games.ots_away as record_away,
	games.wins_last_10 || '-' || games.losses_last_10 || '-' || games.ots_last_10 as record_last_10,
	games.wins_so || '-' || games.losses_so as record_so,
	teams.conference,
	teams.conference_abbrev,
	teams.division,
	teams.division_abbrev,
	teams.team_logo_url

from games

left join goals
  on games.season = goals.season
 and games.team_id = goals.team_id

left join teams
  on games.team_id = teams.id

order by 
	games.season desc, 
	games.points desc, 
	games.games_played asc, 
	games.wins_reg desc,
	games.wins_reg_ot desc,
	games.wins desc, 
	goals.goals_diff desc,
	goals.goals_for desc