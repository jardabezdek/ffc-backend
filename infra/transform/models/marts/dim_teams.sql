with teams as (

	select * from {{ ref("seed_teams") }}

),

current_season as (

    select * from {{ ref("seed_current_season") }}

),

team_ids as (

    select distinct
        home_team_id as team_id,
        home_team_abbrev as team_abbrev

    from {{ ref("base_games") }}
    
    cross join current_season
    
    where season = current_season_long::integer

)

select 
    team_ids.team_id as id,
    teams.*

from teams

left join team_ids
  on teams.team_abbrev_name = team_ids.team_abbrev

order by 1