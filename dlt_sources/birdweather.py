from typing import Any, Optional

import dlt
import pendulum
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)


@dlt.source(name="birdweather")
def birdweather_source(access_token: Optional[str] = dlt.secrets.value) -> Any:
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
                        "since": "2024-09-17",
                    },
                },
            },
            {
                "name": "detections",
                "endpoint": {
                    "path": "stations/{token}/detections",
                    "params": {
                        "limit": 10,
                        "from": pendulum.today().subtract(days=1).to_iso8601_string(),
                        "to": pendulum.today().to_iso8601_string(),
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


# def load_birdweather() -> None:
#     pipeline = dlt.pipeline(
#         pipeline_name="rest_api_birdweather",
#         destination="duckdb",
#         dataset_name="birdweather_stations",
#     )
#
#     load_info = pipeline.run(birdweather_source())
#     print(load_info)  # noqa: T201
#
#
# if __name__ == "__main__":
#     load_birdweather()
