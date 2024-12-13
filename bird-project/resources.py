from pathlib import Path

from dagster_dbt import DbtCliResource, DbtProject
from dagster_duckdb import DuckDBResource
from dagster_embedded_elt.dlt import DagsterDltResource

dlt_resource = DagsterDltResource()
duckdb_birdweather_resource = DuckDBResource(
    database="birdweather_pipeline.duckdb",
)

dbt_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "dbt_bird_project").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
dbt_project.prepare_if_dev()
dbt_resource = DbtCliResource(project_dir=dbt_project.project_dir)
