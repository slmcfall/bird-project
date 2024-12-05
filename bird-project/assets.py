from dagster import AssetExecutionContext, EnvVar
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline

from dlt_sources.birdweather import birdweather_source


@dlt_assets(
    dlt_source=birdweather_source(
        access_token=EnvVar("BIRDWEATHER_API_TOKEN").get_value()
    ),
    dlt_pipeline=pipeline(
        pipeline_name="birdweather_pipeline",
        destination="duckdb",
        dataset_name="birdweather",
        progress="log",
    ),
    name="birdweather",
    group_name="birdweather",
)
def dagster_birdweather_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)
