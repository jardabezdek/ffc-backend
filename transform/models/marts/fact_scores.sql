with games as (

    select * from {{ ref("base_games") }}

),

teams as (

	select * from {{ ref("dim_teams") }}

),

last_games_dates as (

	select distinct date
	from games
	order by date desc
	limit 7 * 4 -- last 4 week

)

select 

	games.id,
    games.date,
    games.start_time_utc,
    games.venue,
    games.period,
    games.period_type,
    games.home_team_id,
	home_teams.team_full_name as home_team_full_name,
	home_teams.team_abbrev_name as home_team_abbrev_name,
    home_teams.team_logo_url as home_team_logo_url,
    games.away_team_id,
	away_teams.team_full_name as away_team_full_name,
	away_teams.team_abbrev_name as away_team_abbrev_name,
	away_teams.team_logo_url as away_team_logo_url,
    games.home_team_score,
	games.away_team_score

from games

left join teams as home_teams
  on games.home_team_id = home_teams.id

left join teams as away_teams
  on games.away_team_id = away_teams.id

where games.date in (select date from last_games_dates)

order by 
	games.date desc, 
	games.start_time_utc asc