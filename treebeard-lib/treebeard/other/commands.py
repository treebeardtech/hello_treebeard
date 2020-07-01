import pprint
import warnings
from pathlib import Path

import click
from halo import Halo  # type: ignore
from humanfriendly import format_size, parse_size  # type: ignore
from timeago import format as timeago_format  # type: ignore

from treebeard.conf import get_treebeard_env
from treebeard.helper import create_example_yaml, set_credentials
from treebeard.util import fatal_exit
from treebeard.version import get_version

pp = pprint.PrettyPrinter(indent=2)


warnings.filterwarnings(
    "ignore", "Your application has authenticated using end user credentials"
)


@click.command()
@click.option("--api_key")
@click.option("--user_name")
def configure(api_key: str, user_name: str):
    """Register with Treebeard services"""
    set_credentials(api_key, user_name)


@click.command()
def setup():
    """Creates examples treebeard.yaml configuration file"""
    if Path("treebeard.yaml").is_file():
        fatal_exit("📁 found existing treebeard.yaml file here")
    create_example_yaml()
    click.echo("📁 created example treebeard.yaml, please update it for your project")


@click.command()
def version():
    """Shows treebeard package version"""
    click.echo(get_version())


@click.group()
def config():
    """Shows Treebeard internal configuration"""


@config.command()  # type: ignore
def list():
    click.echo(pp.pformat(get_treebeard_env(None).dict()))


@config.command()  # type: ignore
@click.argument("key", type=click.STRING)
def get(key: str):
    if key in get_treebeard_env(None).dict():
        click.echo(get_treebeard_env(None).dict()[key])
    else:
        click.echo(f"There is no value for {key}")
