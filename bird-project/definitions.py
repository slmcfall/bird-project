from dagster import Definitions

from .assets import (
    dagster_birdweather_assets,
    distinct_species_names,
    station_species_metadata,
)
from .dbt.assets import my_dbt_assets
from .resources import dlt_resource, duckdb_birdweather_resource, dbt_resource

defs = Definitions(
    assets=[
        dagster_birdweather_assets,
        distinct_species_names,
        station_species_metadata,
        my_dbt_assets,
    ],
    resources={
        "dlt": dlt_resource,
        "birdweather_db": duckdb_birdweather_resource,
        "dbt": dbt_resource,
    },
)
