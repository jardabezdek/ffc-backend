with stg_players as (

    select * from {{ ref("stg_players") }}

)

select
    season_short as season,
    season_long,
    season_type,
    season_type_long,
    player_id,
    first_name,
    last_name,
    full_name,
    -- NOTE: if a player changes clubs during the season, 
    -- we consider him as belonging to the most recent one
    last(team_id order by game_date) as team_id,
    last(sweater_number order by game_date) as sweater_number,
    last(position_code order by game_date) as position_code,
    last(headshot_url order by game_date) as headshot_url,
    sum(
        case 
            when toi is null then 0
            else 1
        end
    )::int as games_played,

from stg_players

group by
    season_short,
    season_long,
    season_type,
    season_type_long,
    player_id,
    first_name,
    last_name,
    full_name
