with games as (

    select * from {{ ref("stg_games") }}

),

goals as (
	select 
		home_team_id as team_id,
		season, 
		home_team_score as goals_for,
		away_team_score as goals_against
	from games
	
	union all
	
	select
		away_team_id as team_id,
		season,
		away_team_score as goals_for,
		home_team_score  as goals_against
		
	from games
)

select 
    team_id,
    season,
    sum(goals_for) as goals_for,
    sum(goals_against) as goals_against,
    sum(goals_for) - sum(goals_against) as goals_diff

from goals
group by 1, 2