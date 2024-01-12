with games as (

    select * from {{ ref("stg_standings_playoff_games") }}

),

teams as (

	select * from {{ ref("dim_teams") }}

)

select 

    games.season,
	games.season_long,
	games.playoff_round,
	games.matchup,
	games.match,
	games.day_month,
	games.home_team_id,
	home_teams.team_full_name as home_team_full_name,
	home_teams.team_abbrev_name as home_team_abbrev_name,
	games.away_team_id,
	away_teams.team_full_name as away_team_full_name,
	away_teams.team_abbrev_name as away_team_abbrev_name,
    games.home_team_score,
	games.away_team_score,
	games.period_type,
	games.home_team_match_score,
	games.away_team_match_score,
	home_teams.team_logo_url as home_team_logo_url,
	away_teams.team_logo_url as away_team_logo_url

from games

left join teams as home_teams
  on games.home_team_id = home_teams.id

left join teams as away_teams
  on games.away_team_id = away_teams.id

order by 
    games.season,
	games.playoff_round,
	games.matchup,
	games.match