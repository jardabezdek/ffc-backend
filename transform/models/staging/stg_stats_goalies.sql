with shots as (

    select 
        substring(game_id::varchar, 1, 4)::int as season,
        substring(game_id::varchar, 6, 1)::int as season_type,
        game_id,
        goalie_in_net_id as player_id,
        event_type,

    from {{ ref("base_shots") }}
	
    where event_type in ('goal', 'shot-on-goal') 
      and goalie_in_net_id is not null

),

stg_players as (

    select * from {{ ref("stg_players") }}
    where position_code = 'G'

),

toi as (

    select * from {{ ref("stg_players_toi") }}

),

goals_against as (

    select 
        season,
        season_type,
        player_id,
        count(*) as shots_against,
        sum(case when event_type = 'goal' then 1 else 0 end) as goals_against,
	
    from shots
	
    group by
        season,
        season_type,
        player_id,

),

goals_against_per_game as (

    select 
        season,
        season_type,
        player_id,
        game_id,
        sum(case when event_type = 'goal' then 1 else 0 end) as goals_against
		
    from shots
	
    group by
        season,
        season_type,
        player_id,
        game_id

),

shutouts as (

    select
        season_short as season,
        season_type,
        player_id,
        sum(shutouts) as shutouts
    	
    from stg_players
    
    group by 
        season_short,
        season_type,
        player_id,
		
)

select 
    goals_against.season,
    goals_against.season_type,
    goals_against.player_id,
    shots_against,
    goals_against,
    round((shots_against - goals_against) / shots_against * 100, 1) as save_pct,
    round(goals_against * 60 * 60 / toi_seconds, 2) as gaa,
    ifnull(shutouts, 0)::int as shutouts,

from goals_against

left join shutouts
  on goals_against.season = shutouts.season
 and goals_against.season_type = shutouts.season_type
 and goals_against.player_id = shutouts.player_id

left join toi
  on goals_against.season = toi.season_short
 and goals_against.season_type = toi.season_type
 and goals_against.player_id = toi.player_id
 
order by 
    goals_against.season desc,
    goals_against.season_type desc,
    save_pct desc
