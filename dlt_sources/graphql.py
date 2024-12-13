import requests
import time
from typing import Dict, Optional, List, Union, Generator
from dataclasses import dataclass
from requests.exceptions import RequestException
from datetime import date, datetime


@dataclass
class InputLocation:
    lat: float
    lon: float


@dataclass
class InputDuration:
    count: Optional[int] = None
    unit: Optional[str] = None  # hour/day/week/month/year
    from_date: Optional[str] = None  # YYYY-MM-DD format
    to_date: Optional[str] = None  # YYYY-MM-DD format

    def to_dict(self) -> Dict:
        """
        Convert to dictionary with proper GraphQL field names
        """
        result = {}
        if self.count is not None:
            result["count"] = self.count
        if self.unit is not None:
            result["unit"] = self.unit
        if self.from_date is not None:
            result["from"] = self.from_date  # Already in YYYY-MM-DD format
        if self.to_date is not None:
            result["to"] = self.to_date  # Already in YYYY-MM-DD format
        return result


class BirdWeatherAPI:
    def __init__(self, api_token: str):
        """
        Initialize the API client with authentication.

        Args:
            api_token (str): Your BirdWeather API token
        """
        self.endpoint = "https://app.birdweather.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_token}",
        }
        self.max_retries = 3
        self.retry_delay = 1

    def get_detections(
        self,
        after: Optional[str] = None,
        before: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        period: Optional[InputDuration] = None,
        species_id: Optional[str] = None,
        species_ids: Optional[List[str]] = None,
        station_ids: Optional[List[str]] = [7577],
        station_types: Optional[List[str]] = None,
        continents: Optional[List[str]] = None,
        countries: Optional[List[str]] = None,
        recording_modes: Optional[List[str]] = None,
        score_gt: Optional[float] = None,
        score_lt: Optional[float] = None,
        score_gte: Optional[float] = None,
        score_lte: Optional[float] = None,
        confidence_gt: Optional[float] = None,
        confidence_lt: Optional[float] = None,
        confidence_gte: Optional[float] = None,
        confidence_lte: Optional[float] = None,
        probability_gt: Optional[float] = None,
        probability_lt: Optional[float] = None,
        probability_gte: Optional[float] = None,
        probability_lte: Optional[float] = None,
        time_of_day_gte: Optional[int] = None,
        time_of_day_lte: Optional[int] = None,
        ne: Optional[InputLocation] = None,
        sw: Optional[InputLocation] = None,
        vote: Optional[int] = None,
        sort_by: Optional[str] = None,
        unique_stations: Optional[bool] = None,
        valid_soundscape: Optional[bool] = None,
        eclipse: Optional[bool] = None,
    ) -> Dict:
        """
        Query bird detections with all available filters.
        """
        query = """
        query detections(
            $after: String, $before: String, $first: Int, $last: Int, $period: InputDuration
            $speciesId: ID, $speciesIds: [ID!], $stationIds: [ID!],
            $stationTypes: [String!], $continents: [String!], $countries: [String!],
            $recordingModes: [String!], $scoreGt: Float, $scoreLt: Float,
            $scoreGte: Float, $scoreLte: Float, $confidenceGt: Float,
            $confidenceLt: Float, $confidenceGte: Float, $confidenceLte: Float,
            $probabilityGt: Float, $probabilityLt: Float, $probabilityGte: Float,
            $probabilityLte: Float, $timeOfDayGte: Int, $timeOfDayLte: Int,
            $ne: InputLocation, $sw: InputLocation, $vote: Int, $sortBy: String,
            $uniqueStations: Boolean, $validSoundscape: Boolean, $eclipse: Boolean
        ) {
            detections(
                after: $after, before: $before, first: $first, last: $last, period: $period
                speciesId: $speciesId, speciesIds: $speciesIds, stationIds: $stationIds,
                stationTypes: $stationTypes, continents: $continents, countries: $countries,
                recordingModes: $recordingModes, scoreGt: $scoreGt, scoreLt: $scoreLt,
                scoreGte: $scoreGte, scoreLte: $scoreLte, confidenceGt: $confidenceGt,
                confidenceLt: $confidenceLt, confidenceGte: $confidenceGte,
                confidenceLte: $confidenceLte, probabilityGt: $probabilityGt,
                probabilityLt: $probabilityLt, probabilityGte: $probabilityGte,
                probabilityLte: $probabilityLte, timeOfDayGte: $timeOfDayGte,
                timeOfDayLte: $timeOfDayLte, ne: $ne, sw: $sw, vote: $vote,
                sortBy: $sortBy, uniqueStations: $uniqueStations,
                validSoundscape: $validSoundscape, eclipse: $eclipse
            ) {
                edges {
                    node {
                        id
                        score
                        confidence
                        certainty
                        probability
                        species {
                            id
                            scientificName
                            imageUrl
                            thumbnailUrl
                        }
                        soundscape {
                               id
                               url
                        }
                    }
                    cursor
                }
                pageInfo {
                    hasNextPage
                    hasPreviousPage
                    startCursor
                    endCursor
                }
                speciesCount
                totalCount
            }
        }
        """

        variables = {
            "after": after,
            "before": before,
            "first": first,
            "last": last,
            "period": period.to_dict() if period else None,
            "speciesId": species_id,
            "speciesIds": species_ids,
            "stationIds": station_ids,
            "stationTypes": station_types,
            "continents": continents,
            "countries": countries,
            "recordingModes": recording_modes,
            "scoreGt": score_gt,
            "scoreLt": score_lt,
            "scoreGte": score_gte,
            "scoreLte": score_lte,
            "confidenceGt": confidence_gt,
            "confidenceLt": confidence_lt,
            "confidenceGte": confidence_gte,
            "confidenceLte": confidence_lte,
            "probabilityGt": probability_gt,
            "probabilityLt": probability_lt,
            "probabilityGte": probability_gte,
            "probabilityLte": probability_lte,
            "timeOfDayGte": time_of_day_gte,
            "timeOfDayLte": time_of_day_lte,
            "ne": ne.__dict__ if ne else None,
            "sw": sw.__dict__ if sw else None,
            "vote": vote,
            "sortBy": sort_by,
            "uniqueStations": unique_stations,
            "validSoundscape": valid_soundscape,
            "eclipse": eclipse,
        }

        return self._execute_query(
            query, {k: v for k, v in variables.items() if v is not None}
        )

    def get_all_detections(
        self, page_size: int = 100, **kwargs
    ) -> Generator[Dict, None, None]:
        """
        Fetch all detections using pagination.
        Yields each page of results.

        Args:
            page_size: Number of results per page
            **kwargs: Any valid parameters for get_detections()
        """
        kwargs["first"] = page_size
        after_cursor = None

        while True:
            kwargs["after"] = after_cursor
            result = self.get_detections(**kwargs)

            yield result["data"]["detections"]

            page_info = result["data"]["detections"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break

            after_cursor = page_info["endCursor"]

    def _execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """
        Execute a GraphQL query with retry logic and error handling.
        """
        payload = {"query": query, "variables": variables or {}}

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.endpoint, headers=self.headers, json=payload, timeout=10
                )

                try:
                    response_data = response.json()
                except ValueError:
                    raise Exception(f"Invalid JSON response: {response.text}")

                if response.status_code == 200:
                    if "errors" in response_data:
                        raise Exception(f"GraphQL errors: {response_data['errors']}")
                    return response_data
                elif response.status_code == 401:
                    raise Exception(
                        "Authentication failed. Please check your API token."
                    )
                elif response.status_code == 403:
                    raise Exception(
                        "Access forbidden. Please check your API token permissions."
                    )
                elif response.status_code == 500:
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                    raise Exception(f"Server error (500). Response: {response.text}")
                else:
                    raise Exception(f"Unexpected status code: {response.status_code}")

            except RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise Exception(f"Network error: {str(e)}")

        raise Exception("Max retries exceeded")


# Example usage
def main():
    API_TOKEN = ""
    api = BirdWeatherAPI(API_TOKEN)

    # Example 1: Get a single page of results
    result = api.get_detections(
        first=10,
        score_gte=0.8,
    )

    # print(result)
    print(
        f"Single page query results: {result['data']['detections']['totalCount']} total detections"
    )
    # Example 1: Using count and unit
    period1 = InputDuration(
        count=24,
        unit="hour",  # Can be hour/day/week/month/year
    )

    # Example 2: Using date range
    period2 = InputDuration(from_date="2024-09-14", to_date="2024-09-15")

    # Query with time period
    result = api.get_detections(
        first=10,
        period=period2,  # or period2
        score_gte=0.8,
    )
    print(result["data"]["detections"]["edges"])

    # Example 2: Get all results using pagination
    # total_detections = 0
    # for page in api.get_all_detections(
    #     page_size=100,
    #     score_gte=0.8,
    #     period=period1,  # or period2
    # ):
    #     total_detections += len(page["edges"])
    #     print(f"Processed page: {len(page['edges'])} detections")
    #     print(page)
    #
    # print(f"Total detections processed: {total_detections}")


if __name__ == "__main__":
    main()
