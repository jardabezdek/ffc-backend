create table shift_temp1 select GameID, playerId, shiftNumber, teamAbbrev as Team, 
	left(startTime,2)*60+right(startTime,2) + period*1200-1200 as Start,
    left(endTime,2)*60+right(endTime,2) + period*1200-1200 as End
	from shift
    where shiftNumber>0;

create table shift_temp2
select GameID, Start from shift_temp1
UNION
select GameID, End as Start from shift_temp1;

create table shift_temp3 
select *, lead(Start,1,0) over(partition by GameID order by GameID, Start) as End
	from shift_temp2
    order by GameID, Start;
    
create table shift_temp4 select *, row_number () over(partition by GameID order by GameID, Start) + GameID*10000 as ShiftIndex 
	from shift_temp3
    where End>0;
    
create table shift_temp5 select s1.GameID, playerId, shiftNumber, Team, ShiftIndex, s2.Start, s2.End 
	from shift_temp1 as s1
    left join shift_temp4 as s2
		on s1.GameID=s2.GameID and s1.Start<=s2.Start and s1.End>=s2.End;

create table shift_temp6 select s.GameID, s.PlayerId, shiftNumber, Team, ShiftIndex, Start, End, 
	CASE when Position='G' then 1 else 0 END as Goaltenders,
    CASE when Position='G' then 0 else 1 END as Skaters,
    CASE when left(Team,3)=HomeTeam then 'Home' when left(Team,3)=AwayTeam then 'Away' else '' END as Venue
	from shift_temp5 as s
    left join players as p
		on s.playerId=p.playerId
	left join schedule as sc
		on s.GameID=sc.GameID;
        
create table shift_temp7 select GameID, ShiftIndex, Start, End, Venue, SUM(Goaltenders) as Goalies, SUM(Skaters) as Skaters
	from shift_temp6
    group by GameID, ShiftIndex, Start, End, Venue;
    
create table shift_temp8 select *, SUM(Goalies) over (partition by ShiftIndex order by ShiftIndex) Total_Goalies,
	SUM(Skaters) over (partition by ShiftIndex order by ShiftIndex) Total_Skaters
	from shift_temp7;
    
create table shift_temp9 select GameID, ShiftIndex, Start, End, Venue, 
	CASE 
		when Total_Goalies>=2 then CONCAT(Skaters,'v',Total_Skaters-Skaters) 
		when Goalies=0 then 'ENF' 
		when Goalies=Total_Goalies 
		then 'ENA' 
	END as StrengthState
	
	from shift_temp8;
    
select StrengthState, Count(StrengthState), SUM(End)-SUM(Start) as Duration from shift_temp9 group by StrengthState;

create table shift_temp10 select GameID, ShiftIndex, Start, End, Venue,
	CASE 
		when StrengthState='5v4' or StrengthState='6v4' or StrengthState='7v4' then '5v4' 
		when StrengthState='4v5' or StrengthState='4v6' or StrengthState='4v7' then '4v5' 
        when StrengthState='5v3' or StrengthState='6v3' or StrengthState='7v3' then '5v3' 
		when StrengthState='3v5' or StrengthState='3v6' or StrengthState='3v7' then '3v5'
        when StrengthState='3v3' then '3v3' 
		when StrengthState='4v4' then '4v4' 
        when StrengthState='ENF' then 'ENF' 
		when StrengthState='ENA' then 'ENA' 
        when StrengthState='3v4' then '3v4' 
		when StrengthState='4v3' then '4v3' 
		else '5v5' 
	END as StrengthState
	from shift_temp9;
    
create table shift_temp11 select GameID, ShiftIndex, Start, End, 
	CASE when Venue='Away' then StrengthState else '' END as Away_StrengthState,
    CASE when Venue='Home' then StrengthState else '' END as Home_StrengthState
	from shift_temp10;
    
Insert Into ShiftIndex select GameID, ShiftIndex, Start, End, MAX(Away_StrengthState) as Away_StrengthState, MAX(Home_StrengthState) as Home_StrengthState
	from shift_temp11
    group by GameID, ShiftIndex, Start, End;
    
Insert Into PlayerShifts select PlayerId, Team, ShiftIndex, Venue from shift_temp6;

drop table shift_temp1;
drop table shift_temp2;
drop table shift_temp3;
drop table shift_temp4;
drop table shift_temp5;
drop table shift_temp6;
drop table shift_temp7;
drop table shift_temp8;
drop table shift_temp9;
drop table shift_temp10;
drop table shift_temp11;