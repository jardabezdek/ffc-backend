with base as (

    select * from {{ source("base", "games") }}

),

base_incremental as (

    select * from {{ source("base_incremental", "games") }}

)

select * from base
union
select * from base_incremental