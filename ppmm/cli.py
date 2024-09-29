import click
from .config import get_mirrors, get_current_mirror, set_current_mirror
from .mirror import test_mirrors

@click.group()
def cli():
    pass

@cli.command()
def ls():
    mirrors = get_mirrors()
    output_lines = []
    for name, url in mirrors.items():
        current = "*" if url == get_current_mirror() else " "
        output_lines.append(f"{current.ljust(2)} {name.ljust(10)} {url}")
    print("\n".join(output_lines))

@cli.command()
@click.argument("name")
def use(name):
    mirrors = get_mirrors()
    if name in mirrors:
        set_current_mirror(mirrors[name])
        print(f"Switched to {name}")
    else:
        print(f"Mirror {name} not found")

@cli.command()
def test():
    mirrors = get_mirrors()
    current = get_current_mirror()
    key = next((key for key, val in mirrors.items() if val == current), None)
    results = test_mirrors()
    output_lines = []
    for name, time in results.items():
        current_mark = "*" if name == key else " "
        output_lines.append(f"{current_mark.ljust(2)} {name.ljust(10)} {time}")
    print("\n".join(output_lines))

@cli.command()
def current():
    current_mirror = get_current_mirror()
    print(f"Current mirror: {current_mirror}")

@cli.command()
def help():
    help_text = """
    ppmm: Python Pip Mirror Manager
    Usage: mm <command>
    Commands:
      ls          List all mirrors
      use <name>  Switch to a specific mirror
      test        Test all mirrors
      current     Show current mirror
      help        Show this help message
    """
    print(help_text)

if __name__ == "__main__":
    cli()