with games as (
    
	select * from {{ ref("stg_games") }}

),

points as (
	select 
		win_team_id as team_id,
		date,
		season,
		period_type,
		2 as points,
		case when win_team_id = home_team_id then home_team_score else away_team_score end as team_score,
		case when win_team_id = home_team_id then true else false end as is_team_home
	from games
	
	union all
	
	select 
		loss_team_id as team_id,
		date,
		season,
		period_type,
		0 as points,
		case when win_team_id = home_team_id then home_team_score else away_team_score end as team_score,
		case when loss_team_id = home_team_id then true else false end as is_team_home
	from games
	where loss_team_id is not null
	
	union all
	
	select 
		ot_team_id as team_id,
		date,
		season,
		period_type,
		1 as points,
		case when win_team_id = home_team_id then home_team_score else away_team_score end as team_score,
		case when ot_team_id = home_team_id then true else false end as is_team_home
	from games
	where ot_team_id is not null
),

points_with_row_number as (
	select 
		*,
		row_number() over (
			partition by season, team_id
			order by date desc
		) as row_num

	from points
)

select
	season,
	team_id,

	-- general
	count(team_id) as games_played,
	sum(case when points = 2 then 1 else 0 end) as wins,
	sum(case when points = 0 then 1 else 0 end) as losses,
	sum(case when points = 1 then 1 else 0 end) as ots,

	-- points
	sum(points) as points,
	round(sum(points) / (count(team_id) * 2), 3) as points_pct,

	-- record by period type
	sum(case when points = 2 and period_type = 'REG' then 1 else 0 end) as wins_reg,
	sum(case when points = 2 and period_type = 'OT' then 1 else 0 end) as wins_ot,
	sum(case when points = 2 and period_type = 'SO' then 1 else 0 end) as wins_so,
	sum(case when points = 0 and period_type = 'REG' then 1 else 0 end) as losses_reg,
	sum(case when points = 1 and period_type = 'OT' then 1 else 0 end) as losses_ot,
	sum(case when points = 1 and period_type = 'SO' then 1 else 0 end) as losses_so,

	-- home record
	sum(case when points = 2 and is_team_home is true then 1 else 0 end) as wins_home,
	sum(case when points = 0 and is_team_home is true then 1 else 0 end) as losses_home,
	sum(case when points = 1 and is_team_home is true then 1 else 0 end) as ots_home,
	
	-- away record
	sum(case when points = 2 and is_team_home is false then 1 else 0 end) as wins_away,
	sum(case when points = 0 and is_team_home is false then 1 else 0 end) as losses_away,
	sum(case when points = 1 and is_team_home is false then 1 else 0 end) as ots_away,
	
	-- last 10 games record
	sum(case when points = 2 and row_num <= 10 then 1 else 0 end) as wins_last_10,
	sum(case when points = 0 and row_num <= 10 then 1 else 0 end) as losses_last_10,
	sum(case when points = 1 and row_num <= 10 then 1 else 0 end) as ots_last_10

from points_with_row_number

group by 1, 2
order by 1, 7 desc
