with seed_teams as (

    select * from {{ source("seeds", "teams") }}

)

select * from seed_teams