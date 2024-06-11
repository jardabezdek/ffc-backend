with base_games as (

    select * from {{ ref("base_games") }}

)

select
    id,
    date,
    home_team_id,
    away_team_id,
    substring(season::char, 1, 4)::int as season,
    type as season_type,
    home_team_score,
    away_team_score,
    period_type,
    case
        when home_team_score > away_team_score then home_team_id
        else away_team_id
    end as win_team_id,
    case
        when home_team_score < away_team_score and period <= 3 then home_team_id
        when period <= 3 then away_team_id
        else null
    end as loss_team_id,
    case
        when home_team_score < away_team_score and period > 3 then home_team_id
        when period > 3 then away_team_id
        else null
    end as ot_team_id

from base_games