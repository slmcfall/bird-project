from typing import Any, Optional

import dlt
import pendulum
from dagster import get_dagster_logger
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)

logger = get_dagster_logger()


@dlt.source(name="birdweather")
def birdweather_source(
    access_token: Optional[str] = dlt.secrets.value,
    from_date: Optional[str] = "2024-09-14",
) -> Any:
    to_date = pendulum.parse(from_date).add(days=1).to_iso8601_string()
    logger.info(f"to date: {to_date}")
    logger.info(f"from date: {from_date}")
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://app.birdweather.com/api/v1",
        },
        # The default configuration for all resources and their endpoints
        "resource_defaults": {
            "endpoint": {
                "params": {
                    "token": access_token,
                },
            },
        },
        "resources": [
            {
                "name": "stations",
                "endpoint": {
                    "path": "stations/{token}/stats",
                    "params": {
                        "period": "week",
                        "since": "2024-09-14",
                    },
                },
            },
            {
                "name": "detections",
                "endpoint": {
                    "path": "stations/{token}/detections",
                    "paginator": {
                        "type": "offset",
                        "limit": 100,
                        "total_path": None,
                        "maximum_offset": 100,
                    },
                    "params": {
                        "from": from_date,
                        "to": to_date,
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


@dlt.source(name="birdweather_species")
def birdweather_species_source(species: Optional = None) -> Any:
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://app.birdweather.com/api/v1",
            "headers": {"Content-Type": "application/json"},
        },
        "resources": [
            {
                "name": "species",
                "endpoint": {
                    "path": "species/lookup",
                    "json": {
                        "species": species,
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
                    },
                    "method": "POST",
                },
            },
        ],
    }

    yield from rest_api_resources(config)
