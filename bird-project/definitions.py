from dagster import Definitions

from .assets import dagster_birdweather_assets
from .resources import dlt_resource

defs = Definitions(
    assets=[dagster_birdweather_assets],
    resources={
        "dlt": dlt_resource,
    },
)
