with base as (

    select * from {{ source("base", "shots") }}

)

select * from base