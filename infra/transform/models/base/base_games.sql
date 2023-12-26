with base as (

    select * from {{ source("base", "games") }}

)

select * from base