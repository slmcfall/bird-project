from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from ..resources import dbt_project


@dbt_assets(manifest=dbt_project.manifest_path)
def my_dbt_assets(
    context: AssetExecutionContext,
    dbt: DbtCliResource,
):
    yield from dbt.cli(["build", *dbt.get_defer_args()], context=context).stream()
