import json

import polars as pl
import requests
from dagster import (
    AssetExecutionContext,
    AssetKey,
    DailyPartitionsDefinition,
    EnvVar,
    Output,
    asset,
)
from dagster_duckdb import DuckDBResource
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dlt import pipeline

from dlt_sources.birdweather import birdweather_source

daily_partitions = DailyPartitionsDefinition(start_date="2024-09-14")


@dlt_assets(
    dlt_source=birdweather_source(),
    dlt_pipeline=pipeline(
        pipeline_name="birdweather_pipeline",
        destination="duckdb",
        dataset_name="birdweather",
        progress="log",
    ),
    partitions_def=daily_partitions,
    name="birdweather",
    group_name="birdweather",
)
def dagster_birdweather_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    from_date = context.partition_key
    yield from dlt.run(
        context=context,
        dlt_source=birdweather_source(
            access_token=EnvVar("BIRDWEATHER_API_TOKEN").get_value(),
            from_date=from_date,
        ),
    )


@asset(deps=AssetKey("dlt_birdweather_detections"), group_name="birdweather")
def distinct_species_names(
    context: AssetExecutionContext, birdweather_db: DuckDBResource
) -> Output:
    with birdweather_db.get_connection() as conn:
        query = """select distinct species__scientific_name || '_' || species__common_name as species from birdweather.detections;"""
        species_df = conn.execute(query).pl()
        species_list = species_df["species"].to_list()
    return Output(species_list, metadata={"species_list": species_list})


@asset(group_name="birdweather")
def station_species_metadata(
    context: AssetExecutionContext,
    birdweather_db: DuckDBResource,
    distinct_species_names,
):
    url = "https://app.birdweather.com/api/v1/species/lookup"
    headers = {"Content-Type": "application/json"}
    data = {
        "species": distinct_species_names,
        "fields": [
            "id",
            "commonName",
            "scientificName",
            "color",
            "imageUrl",
            "thumbnailUrl",
            "infoUrl",
            "wikipediaUrl",
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    json_data = str(response.json()["species"])
    json_data = json_data.replace("'", '"')

    bird_dict = json.loads(json_data)

    bird_list = list(bird_dict.values())
    df = pl.DataFrame(bird_list)

    with birdweather_db.get_connection() as conn:
        query = """create or replace table birdweather.species as select * from df"""
        conn.execute(query)
    return Output("birdweather.species")
