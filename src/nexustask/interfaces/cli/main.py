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
    import httpx
    with console.status("[bold green]Dispatching command to API gateway...") as status:
        try:
            response = httpx.post(
                "http://localhost:8000/api/v1/tasks",
                json={"title": title, "project_id": project}
            )
            response.raise_for_status()
            task_id = response.json()["task_id"]
            console.print(f"[green]✓[/green] Task created with ID: [bold]{task_id}[/bold]")
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to create task: {e}")

@cli.command()
def list():
    """List tasks using the API gateway."""
    import httpx
    with console.status("[bold green]Fetching tasks from API gateway...") as status:
        try:
            response = httpx.get("http://localhost:8000/api/v1/tasks")
            response.raise_for_status()
            tasks = response.json()
            
            table = Table(title="NexusTask Global View")
            table.add_column("ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Title", style="magenta")
            table.add_column("Status", justify="right", style="green")

            for task in tasks:
                table.add_row(task["id"][:8], task["title"], task["status"])

            console.print(table)
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to fetch tasks: {e}")

if __name__ == '__main__':
    cli()
