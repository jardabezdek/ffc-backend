with base_shifts as (

    select * from {{ ref("base_shifts") }}

),

players as (

    select
    
        game_id, 
        away_team_id,
        home_team_id,
        player_id,
        team_id,
        position_code,
        
    from {{ ref("stg_players") }}

),

time_in_seconds as (

    select

        game_id,
        player_id,
        team_id,
        shift_number,
        (period - 1) * 1200 as seconds_in_previous_periods,
        left(start_time, 2)::int * 60 + right(start_time, 2)::int as start_seconds_in_period,
        left(end_time, 2)::int * 60 + right(end_time, 2)::int as end_seconds_in_period,
        seconds_in_previous_periods + start_seconds_in_period as start_time,
        seconds_in_previous_periods + end_seconds_in_period as end_time,

    from base_shifts

    where shift_number > 0

),

start_times as (

    select game_id, start_time from time_in_seconds
    union
    select game_id, end_time as start_time from time_in_seconds

),

end_times as (

    select
        game_id, 
        start_time,
        lead(start_time, 1, 0) over (partition by game_id order by start_time) as end_time,
        end_time - start_time as duration,

    from start_times

),

ids as (
    select
        game_id,
        start_time,
        end_time,
        duration,
        -- newly created shift id to better handle strengths and game situations computation
        row_number() over (partition by game_id order by start_time) + game_id * 10000 as shift_id,

    from end_times
    
    where end_time > 0

),

shifts as (

    select distinct
        time_in_seconds.game_id,
        time_in_seconds.team_id,
        time_in_seconds.player_id,
        ids.shift_id,
        ids.start_time,
        ids.end_time,
        ids.duration,
        players.position_code = 'G' as is_goalie,
        players.position_code != 'G' as is_skater,
        players.team_id = players.away_team_id as is_away_team_player,
        players.team_id = players.home_team_id as is_home_team_player,

    from time_in_seconds

    left join ids
        on time_in_seconds.game_id = ids.game_id
        and time_in_seconds.start_time <= ids.start_time
        and time_in_seconds.end_time >= ids.end_time
        
    left join players
        on time_in_seconds.game_id = players.game_id 
        and time_in_seconds.player_id = players.player_id

)

select * from shifts
