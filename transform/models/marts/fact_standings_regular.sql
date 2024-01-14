/*
Official NHL standings criteria: teams are ordered by
	- points, 
	- then wins, 
	- then losses (ascending), 
	- then by games played (ascending), 
	- and then goal differential.
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
	games.wins desc, 
	games.losses asc, 
	games.games_played asc, 
	goals.goals_diff desc