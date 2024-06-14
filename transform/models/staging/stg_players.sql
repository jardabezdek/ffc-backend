with base_players as (

    select * from {{ ref("base_players") }}

)

select
    game_id,
    game_date,
    away_team_id,
    home_team_id,
    season,
    substring(season::varchar, 1, 4)::int as season_short,
    season_short || '/' || season_short + 1 as season_long,
    substring(game_id::varchar, 6, 1)::int as season_type,
    case
        when season_type = 2 then 'Regular Season'
        when season_type = 3 then 'Playoffs'
    end as season_type_long,
    player_id,
    team_id,
    trim(strip_accents(first_name)) as first_name,
    trim(strip_accents(last_name)) as last_name,
    trim(strip_accents(first_name)) || ' ' || trim(strip_accents(last_name)) as full_name,
    sweater_number,
    position_code,
    headshot as headshot_url,
    goals,
    assists,
    points,
    pim,
    toi,
    case 
        when toi is null then 0
        else split_part(toi, ':', 1)::int * 60 + split_part(toi, ':', 2)::int
    end as toi_seconds,
    games_started,
    shots_against,
    goals_against,
    save_pctg as save_pct,
    shutouts,
    plus_minus,
    power_play_goals,
    power_play_points,
    game_winning_goals,
    ot_goals,
    shots,
    shifts,
    shorthanded_goals,
    shorthanded_points,

from base_players
