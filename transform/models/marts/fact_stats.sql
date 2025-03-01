with players as (

    select * from {{ ref("stg_players_general_info") }}

),

teams as (
	
    select * from {{ ref("dim_teams") }}

),

skaters as (

    select * from {{ ref("stg_stats_skaters") }}

),

goalies as (

    select * from {{ ref("stg_stats_goalies") }}

),

toi as (

    select * from {{ ref("stg_players_toi") }}

)

select 
    players.season,
    players.season_long,
    players.season_type,
    players.season_type_long,
    players.team_id,
    teams.team_full_name,
    teams.team_abbrev_name,
    teams.team_logo_url,
    players.player_id,
    players.first_name,
    players.last_name,
    players.full_name,
    players.sweater_number,
    players.position_code,
    players.headshot_url,
    players.games_played,
    toi.toi_seconds,
    toi.toi_minutes,
    toi.toi,

    -- skaters
    ifnull(skaters.points, 0) as points,
    ifnull(skaters.goals, 0) as goals,
    ifnull(skaters.assists, 0) as assists,
    ifnull(skaters.even_strength_points, 0) as even_strength_points,
    ifnull(skaters.even_strength_goals, 0) as even_strength_goals,
    ifnull(skaters.power_play_points, 0) as power_play_points,
    ifnull(skaters.power_play_goals, 0) as power_play_goals,
    ifnull(skaters.shorthanded_points, 0) as shorthanded_points,
    ifnull(skaters.shorthanded_goals, 0) as shorthanded_goals,
    ifnull(skaters.ot_goals, 0) as ot_goals,
    ifnull(skaters.game_winning_goals, 0) as game_winning_goals,
    ifnull(skaters.shots, 0) as shots,
    ifnull(skaters.shoot_pct, 0) as shoot_pct,
    ifnull(skaters.plus_minus, 0) as plus_minus,
    ifnull(skaters.pim, 0) as pim,

    -- goalies
    ifnull(goalies.shots_against, 0) as shots_against,
    ifnull(goalies.goals_against, 0) as goals_against,
    goalies.save_pct,
    goalies.xg_against,
    goalies.xg_against_per_shot,
    goalies.saved_goals_above_expected,
    goalies.saved_goals_above_expected_per_60,
    goalies.gaa,
    goalies.xgaa,
    ifnull(goalies.shutouts, 0) as shutouts,
	
from players

left join teams
  on players.team_id = teams.id

left join skaters
  on skaters.player_id = players.player_id
 and skaters.season = players.season
 and skaters.season_type = players.season_type

left join goalies
  on goalies.player_id = players.player_id
 and goalies.season = players.season
 and goalies.season_type = players.season_type

left join toi
  on toi.player_id = players.player_id
 and toi.season_short = players.season
 and toi.season_type = players.season_type

where toi_seconds > 0

order by
    players.season desc,
    players.season_type desc,
    skaters.points desc,
    players.games_played asc
