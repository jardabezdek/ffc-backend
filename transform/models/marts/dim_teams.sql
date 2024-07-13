with teams as (

	select * from {{ ref("seed_teams") }}

),

team_ids as (

    select distinct
        home_team_id as team_id,
        home_team_abbrev as team_abbrev

    from {{ ref("base_games") }}

),

utah as (
	
    select
        59 as id,
        'Utah Hockey Club' as team_full_name,
        'UTA' as team_abbrev_name,
        'Utah' as team_common_name,
        'Western' as conference,
        'W' as conference_abbrev,
        'Central' as division,
        'C' as division_abbrev,
        'https://assets.nhle.com/logos/nhl/svg/UTA_light.svg' as team_logo_url

)

select 
    team_ids.team_id as id,
    teams.*

from teams

left join team_ids
  on teams.team_abbrev_name = team_ids.team_abbrev

-- order by 1

union select * from utah
