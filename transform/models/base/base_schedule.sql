with base as (

    select * from {{ source("base", "schedule") }}

)

select * from base
