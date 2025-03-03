with shots as (

    select 
        season,
        season_type,
        game_id,
        goalie_in_net_id as player_id,
        event_type,
        xg,

    from {{ ref("stg_shots") }}
	
    where is_fenwick
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
        sum(xg) as xg_against,
        sum(xg) / count(*) as xg_against_per_shot,
        xg_against - goals_against as saved_goals_above_expected,
	
    from shots
	
    group by
        season,
        season_type,
        player_id,

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
    ifnull(shots_against, 0)::int as shots_against,
    ifnull(goals_against, 0)::int as goals_against,
    round(xg_against, 1) as xg_against,
    round(xg_against_per_shot, 2) as xg_against_per_shot,
    round(saved_goals_above_expected, 1) as saved_goals_above_expected,
    round((shots_against - goals_against) / shots_against * 100, 1) as save_pct,
    round(goals_against * 60 * 60 / toi_seconds, 2) as gaa,
    round(xg_against * 60 * 60 / toi_seconds, 2) as xgaa,
    round(saved_goals_above_expected * 60 * 60 / toi_seconds, 2) as saved_goals_above_expected_per_60,
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
