import click
from gridmeta.cli.converter import extract_opendss_dehydrated_dataset


@click.group()
def cli():
    pass


cli.add_command(extract_opendss_dehydrated_dataset)
