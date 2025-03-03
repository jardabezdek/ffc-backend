with stg_players as (

    select * from {{ ref("stg_players") }}

),

stg_shots as (

    select * from {{ ref("stg_shots") }}

),

shots as (

    select 
        season,
        season_type,
        game_id,
        shooting_player_id as player_id,
        event_type,
        xg,
        is_fenwick,

    from stg_shots

),

basic_stats as (

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
        sum(plus_minus)::int as plus_minus,
        sum(pim)::int as pim,

    from stg_players

    group by 
        season_short,
        season_type,
        player_id,

),

shot_stats as (
    
    select
        season,
        season_type,
        player_id,
        sum(case when event_type = 'goal' then 1 else 0 end) as goals,
        sum(case when event_type in ('goal', 'shot-on-goal') then 1 else 0 end)::int as shots_cnt,
        round(goals / shots_cnt * 100, 1) as shoot_pct,
        round(sum(xg), 1) as xg_sum,
        round(xg_sum / shots_cnt, 2) as xg_per_shot,
        round(xg_sum / count(distinct game_id), 2) as xg_per_game,
        goals - xg_sum as goals_above_expected,
    
	from shots
	
	group by
        season,
        season_type,
        player_id,

)

select 
    basic_stats.season,
    basic_stats.season_type,
    basic_stats.player_id,

    -- basic stats
    ifnull(basic_stats.points, 0) as points,
    ifnull(basic_stats.goals, 0) as goals,
    ifnull(basic_stats.assists, 0) as assists,
    ifnull(basic_stats.even_strength_points, 0) as even_strength_points,
    ifnull(basic_stats.even_strength_goals, 0) as even_strength_goals,
    ifnull(basic_stats.power_play_points, 0) as power_play_points,
    ifnull(basic_stats.power_play_goals, 0) as power_play_goals,
    ifnull(basic_stats.shorthanded_points, 0) as shorthanded_points,
    ifnull(basic_stats.shorthanded_goals, 0) as shorthanded_goals,
    ifnull(basic_stats.ot_goals, 0) as ot_goals,
    ifnull(basic_stats.game_winning_goals, 0) as game_winning_goals,
    ifnull(basic_stats.plus_minus, 0) as plus_minus,
    ifnull(basic_stats.pim, 0) as pim,

    -- shot stats
    ifnull(shot_stats.shots_cnt, 0) as shots,
    ifnull(shot_stats.shoot_pct, 0) as shoot_pct,
    ifnull(shot_stats.xg_sum, 0) as xg,
    ifnull(shot_stats.xg_per_shot, 0) as xg_per_shot,
    ifnull(shot_stats.xg_per_game, 0) as xg_per_game,
    ifnull(shot_stats.goals_above_expected, 0) as goals_above_expected,
	
from basic_stats

left join shot_stats
    on basic_stats.season = shot_stats.season
    and basic_stats.season_type = shot_stats.season_type
    and basic_stats.player_id = shot_stats.player_id
