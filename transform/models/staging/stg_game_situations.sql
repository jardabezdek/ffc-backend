with shifts as (

    select * from {{ ref("stg_shifts") }}

),

player_counts as (

    select
        game_id,
        shift_id,
        start_time,
        end_time,
        duration,
        team_id,
        is_away_team_player as is_away_team,
        is_home_team_player as is_home_team,
        sum(is_goalie::int) as goalie_count,
        sum(is_skater::int) as skaters_count,
        
    from players_shifts
    
    group by 
        game_id,
        shift_id,
        start_time,
        end_time,
        duration,
        team_id,
        is_away_team_player,
        is_home_team_player

),

player_counts_per_shift as (
    
    select

        game_id,
        shift_id,
        start_time,
        end_time,
        duration,
        max(goalie_count)  filter (where is_home_team) as home_goalies,
        max(skaters_count) filter (where is_home_team) as home_skaters,
        max(goalie_count)  filter (where is_away_team) as away_goalies,
        max(skaters_count) filter (where is_away_team) as away_skaters

    from player_counts

    group by game_id, shift_id, start_time, end_time, duration

),

game_situations as (

    select

        game_id,
        shift_id,
        start_time,
        end_time,
        duration,
        concat(
            away_goalies::varchar,
            away_skaters::varchar,
            home_skaters::varchar,
            home_goalies::varchar
        ) as situation_code,
        concat(home_skaters, 'v', away_skaters) as home_team_strength,
        concat(away_skaters, 'v', home_skaters) as away_team_strength,
        case
            when (home_skaters, away_skaters) in ((5, 5), (4, 4), (3, 3)) then 'es'
            when (home_skaters, away_skaters) in ((5, 4), (5, 3), (6, 5), (6, 4), (4, 3)) then 'pp'
            when (home_skaters, away_skaters) in ((4, 5), (3, 5), (5, 6), (4, 6), (3, 4)) then 'pk'
            else 'unknown'
        end as home_team_situation,
        case
            when (home_skaters, away_skaters) in ((5, 5), (4, 4), (3, 3)) then 'es'
            when (home_skaters, away_skaters) in ((5, 4), (5, 3), (6, 5), (6, 4), (4, 3)) then 'pp'
            when (home_skaters, away_skaters) in ((4, 5), (3, 5), (5, 6), (4, 6), (3, 4)) then 'pk'
            else 'unknown'
        end as away_team_situation

    from player_counts_per_shift
    
    where (home_skaters, away_skaters) in (
        (5, 5), (4, 4), (3,3),
        (5, 4), (5, 3), (6, 5), (6, 4), (4, 3),
        (4, 5), (3, 5), (5, 6), (4, 6), (3, 4)
  )

)

select * from game_situations
order by game_id, shift_id
