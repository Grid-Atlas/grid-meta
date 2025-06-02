from pathlib import Path
import datetime

import click

from gridmeta.opendss import OpenDSSMetdataExtractorV1
from gridmeta.models import Metadata, RegionType


@click.command()
@click.option(
    "-f",
    "--opendss-file",
    type=str,
    help="Path to master opendss file for which data is to be extracted.",
)
@click.option(
    "-pm",
    "--privacy-mode",
    type=click.Choice(["low", "moderate", "high"]),
    default=None,
    help="Region type",
)
@click.option(
    "-o", "--output-json-file", type=str, help="Path to JSON file to store the dehydrated dataset."
)
@click.option("-y", "--model-year", type=int, default=2025, help="Model year for OpenDSS model")
@click.option(
    "-s", "--state", type=str, default="WA", help="US State to which this model belongs to."
)
@click.option(
    "-r",
    "--region-type",
    type=click.Choice([m.value for m in RegionType]),
    default=RegionType.Suburban.value,
    help="Region type",
)
@click.option("-d", "--description", type=str, default="", help="Provide some description.")
@click.option(
    "-o", "--output-json-file", type=str, help="Path to JSON file to store the dehydrated dataset."
)
def extract_opendss_dehydrated_dataset(
    opendss_file: str,
    privacy_mode: str | None,
    output_json_file: str,
    model_year: int,
    state: str,
    region_type: str,
    description: str,
):
    extractor = OpenDSSMetdataExtractorV1(
        Path(opendss_file),
        metadata=Metadata(
            state=state,
            created_at=datetime.datetime.now(),
            model_year=model_year,
            region_type=region_type,
            info=description,
        ),
    )
    extractor.export(output_json_file, privacy_mode)
