with base as (

    select * from {{ source("base", "situation-time") }}

),

base_incremental as (

    select * from {{ source("base_incremental", "situation_time") }}

)

select * from base
union
select * from base_incremental
