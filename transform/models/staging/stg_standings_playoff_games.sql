with playoff_games as (

	select
		*,
		substring(id::char, 1, 9) as matchup_id,
		substring(id::char, 10, 1) as match_idx,
		substring(id::char, 8, 1) as round,
		substring(id::char, 9, 1) as matchup,
		substring(id::char, 10, 1) as match,
		strftime(date::date, '%d.%m.') as day_month
	
	from {{ ref("stg_games") }}
	
	where season_type = 3
),

games_per_team as (
	
	select
		matchup_id,
		match_idx,
		home_team_id as team_id,
		case when home_team_id = win_team_id then 1 else 0 end as match_point
	from playoff_games
	
	union
	
	select
		matchup_id,
		match_idx,
		away_team_id as team_id,
		case when away_team_id = win_team_id then 1 else 0 end as match_point
	from playoff_games
	
), 

team_match_points as (
	
	select
		matchup_id,
		match_idx,
		team_id,
		sum(match_point) over (
			partition by matchup_id, team_id 
			order by match_idx
		) as team_match_point 
		
	from games_per_team

)

select 

	-- id as game_id,
	season,
	season || '/' || season + 1 as season_long,
	-- season_type,
	substring(id, 8, 1)::int as playoff_round,
	substring(id, 9, 1)::int as matchup,
	substring(id, 10, 1)::int as match,
	strftime(date::date, '%d.%m.') as day_month,
	home_team_id,
	away_team_id,
	home_team_score,
	away_team_score,
	period_type,
	home_match_points.team_match_point::int as home_team_match_score,
	away_match_points.team_match_point::int as away_team_match_score

from playoff_games

left join team_match_points as home_match_points
  on home_match_points.matchup_id = substring(id, 1, 9)
 and home_match_points.match_idx = substring(id, 10, 1)
 and home_match_points.team_id = playoff_games.home_team_id
 
left join team_match_points as away_match_points
  on away_match_points.matchup_id = substring(id, 1, 9)
 and away_match_points.match_idx = substring(id, 10, 1)
 and away_match_points.team_id = playoff_games.away_team_id
