with players as (

    select * from {{ ref("stg_players_general_info") }}

),

teams as (
	
    select * from {{ ref("dim_teams") }}

),

goals as (

    select * from {{ ref("stg_stats_skaters_goals") }}

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
    ifnull(goals.points, 0) as points,
    ifnull(goals.goals, 0) as goals,
    ifnull(goals.empty_net_goals, 0) as empty_net_goals,
    ifnull(goals.individual_goals, 0) as individual_goals,
    ifnull(goals.assists, 0) as assists,
    ifnull(goals.assists_1, 0) as assists_1,
    ifnull(goals.assists_2, 0) as assists_2,

    -- goalies
    goalies.shots_against,
    goalies.goals_against,
    goalies.gaa,
    goalies.save_pct,
    ifnull(goalies.shutouts, 0) as shutouts,
	
from players

left join teams
  on players.team_id = teams.id

left join goals
  on goals.player_id = players.player_id
 and goals.season = players.season
 and goals.season_type = players.season_type

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
    goals.points desc,
    players.games_played asc
