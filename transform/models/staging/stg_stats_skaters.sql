with stg_players as (

    select * from {{ ref("stg_players") }}

),

stats as (

    select
        season_short as season,
        season_type,
        player_id,
        sum(points)::int as points,
        sum(goals)::int as goals,
        sum(assists)::int as assists,
        (sum(points) - sum(power_play_points) - sum(shorthanded_points))::int as even_strength_points,
        (sum(goals) - sum(power_play_goals) - sum(shorthanded_goals))::int as even_strength_goals,
        sum(power_play_points)::int as power_play_points,
        sum(power_play_goals)::int as power_play_goals,
        sum(shorthanded_points)::int as shorthanded_points,
        sum(shorthanded_goals)::int as shorthanded_goals,
        sum(ot_goals)::int as ot_goals,
        sum(game_winning_goals)::int as game_winning_goals,
        sum(shots)::int as shots,
		round(sum(goals) / sum(shots) * 100, 1) as shoot_pct,
        sum(plus_minus)::int as plus_minus,
        sum(pim)::int as pim,

    from stg_players

    group by 
        season_short,
        season_type,
        player_id,

)

select 
    season,
    season_type,
    player_id,
    ifnull(points, 0) as points,
    ifnull(goals, 0) as goals,
    ifnull(assists, 0) as assists,
    ifnull(even_strength_points, 0) as even_strength_points,
    ifnull(even_strength_goals, 0) as even_strength_goals,
    ifnull(power_play_points, 0) as power_play_points,
    ifnull(power_play_goals, 0) as power_play_goals,
    ifnull(shorthanded_points, 0) as shorthanded_points,
    ifnull(shorthanded_goals, 0) as shorthanded_goals,
    ifnull(ot_goals, 0) as ot_goals,
    ifnull(game_winning_goals, 0) as game_winning_goals,
    ifnull(shots, 0) as shots,
    ifnull(shoot_pct, 0) as shoot_pct,
    ifnull(plus_minus, 0) as plus_minus,
    ifnull(pim, 0) as pim,
	
from stats
