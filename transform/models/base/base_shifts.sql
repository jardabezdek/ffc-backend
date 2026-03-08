with base as (

    select * from {{ source("base", "shifts") }}

),

base_incremental as (

    select * from {{ source("base_incremental", "shifts") }}

)

select * from base
union
select * from base_incremental
