with teams as (

	select * from {{ ref("seed_teams") }}

),

team_ids as (

    select distinct
        home_team_id as team_id,
        home_team_abbrev as team_abbrev

    from {{ ref("base_games") }}

)

select 
    team_ids.team_id as id,
    teams.*

from teams

left join team_ids
  on teams.team_abbrev_name = team_ids.team_abbrev

order by 1
