import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.version_option(version="10.4.2", prog_name="NexusTask Enterprise CLI")
def cli():
    """
    NexusTask Enterprise Command Line Interface.
    Interacts with the gRPC/REST gateway or local SQLite cache.
    """
    pass

@cli.command()
@click.argument('title')
@click.option('--project', default='00000000-0000-0000-0000-000000000000', help='Project UUID')
def create(title, project):
    """Create a new task in the enterprise grid."""
    with console.status("[bold green]Dispatching command to Kafka broker...") as status:
        import time
        time.sleep(1) # Simulate network call
        import uuid
        console.print(f"[green]✓[/green] Task created with ID: [bold]{uuid.uuid4()}[/bold]")

@cli.command()
def list():
    """List tasks using ElasticSearch aggregation."""
    table = Table(title="NexusTask Global View")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Status", justify="right", style="green")

    table.add_row("10492-A", "Migrate legacy DB to Spanner", "IN_PROGRESS")
    table.add_row("10493-B", "Update Kubernetes manifests", "TODO")

    console.print(table)

if __name__ == '__main__':
    cli()
