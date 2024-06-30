with schedule as (

	select * from {{ ref("base_schedule") }}

),

teams as (

	select * from {{ ref("dim_teams") }}

)

select

    schedule.start_time_utc,
    schedule.venue,
    home_teams.team_full_name as home_team_full_name,
    home_teams.team_abbrev_name as home_team_abbrev_name,
    home_teams.team_logo_url as home_team_logo_url,
    away_teams.team_full_name as away_team_full_name,
    away_teams.team_abbrev_name as away_team_abbrev_name,
    away_teams.team_logo_url as away_team_logo_url

from schedule

left join teams as home_teams
  on schedule.home_team_id = home_teams.id

left join teams as away_teams
  on schedule.away_team_id = away_teams.id
