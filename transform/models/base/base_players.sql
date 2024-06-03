with base as (

    select * from {{ source("base", "players") }}

),

base_incremental as (

    select * from {{ source("base_incremental", "players") }}

)

select * from base
union
select * from base_incremental
