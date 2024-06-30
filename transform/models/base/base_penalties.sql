with base as (

    select * from {{ source("base", "penalties") }}

),

base_incremental as (

    select * from {{ source("base_incremental", "penalties") }}

)

select * from base
union
select * from base_incremental
