with years as (
	select
		cast(date_part('year', current_date()) - 1 as varchar) as last_year,
		cast(date_part('year', current_date()) as varchar) as this_year,
		cast(date_part('year', current_date()) + 1 as varchar) as next_year
)

select
	case
		when date_part('month', current_date()) >= 9 then this_year
		else last_year
	end as current_season_short,
	case
		when date_part('month', current_date()) >= 9 then this_year || next_year
		else last_year || this_year 
	end as current_season_long
	
from years