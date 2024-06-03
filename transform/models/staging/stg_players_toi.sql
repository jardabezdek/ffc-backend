with stg_players as (

    select * from {{ ref("stg_players") }}

),

toi as (
	
    select
        season,
        season_short,
        season_type,
        player_id,
        sum(toi_seconds) as toi_seconds,
		
    from stg_players

    group by 
        season,
        season_short,
        season_type,
        player_id,

)

select 
    season,
    season_short,
    season_type,
    player_id,
    toi_seconds,
    (toi_seconds // 60)::int as toi_minutes,
    toi_minutes || ':' || lpad((toi_seconds % 60)::char, 2, '0') as toi,

from toi
