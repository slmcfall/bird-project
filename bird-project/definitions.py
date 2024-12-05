from dagster import Definitions

from .assets import dagster_birdweather_assets, dagster_birdweather_species_asset
from .resources import dlt_resource

defs = Definitions(
    assets=[dagster_birdweather_assets, dagster_birdweather_species_asset],
    resources={
        "dlt": dlt_resource,
    },
)
