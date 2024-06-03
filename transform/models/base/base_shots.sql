with base as (

    select * from {{ source("base", "shots") }}

),

base_incremental as (

    select * from {{ source("base_incremental", "shots") }}

)

select * from base
union
select * from base_incremental
