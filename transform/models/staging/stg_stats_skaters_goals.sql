with shots as (

    select * from {{ ref("base_shots") }}

),

goals as (

    select
        substring(game_id::varchar, 1, 4)::int as season,
        substring(game_id::varchar, 6, 1)::int as season_type, 
        *, 

    from shots
    
    where event_type = 'goal'

),

assists as (

    select 
        season,
        season_type,
        assist_1_player_id as player_id,
        event_owner_team_id as team_id,
        'A1' as assist_type
		
    from goals
    
    where assist_1_player_id is not null
    
    union all
    
    select 
        season,
        season_type,
        assist_2_player_id as player_id,
        event_owner_team_id as team_id,
        'A2' as assist_type
    	
    from goals
    
    where assist_2_player_id is not null
	
),

assist_stats as (

    select
        season,
        season_type,
        player_id,
        -- team_id,
        count(*) as assists,
        ifnull(sum(case when assist_type = 'A1' then 1 else 0 end), 0) as assists_1,
        ifnull(sum(case when assist_type = 'A2' then 1 else 0 end), 0) as assists_2
    
    from assists
    
    group by
        season,
        season_type,
        player_id,
        -- team_id,

),

goal_stats as (

    select 
        season,
        season_type,
        shooting_player_id as player_id,
        -- event_owner_team_id as team_id,
        count(*) as goals,
        sum(case when goalie_in_net_id is null then 1 else 0 end) as empty_net_goals,
        sum(case when assist_1_player_id is null and assist_2_player_id is null then 1 else 0 end) as individual_goals
    	
    from goals
    
    group by
        season,
        season_type,
        player_id,
        -- team_id,

)

select 
    goals.season,
    goals.season_type,
    goals.player_id,
    ifnull(goals.goals, 0) + ifnull(assists.assists, 0) as points,
    ifnull(goals.goals, 0) as goals,
    ifnull(assists.assists, 0) as assists, 
    ifnull(goals.empty_net_goals, 0) as empty_net_goals,
    ifnull(goals.individual_goals, 0) as individual_goals,
    ifnull(assists.assists_1, 0) as assists_1,
    ifnull(assists.assists_2, 0) as assists_2,
	
from goal_stats as goals

left join assist_stats as assists
  on assists.player_id = goals.player_id
 and assists.season = goals.season
 and assists.season_type = goals.season_type
