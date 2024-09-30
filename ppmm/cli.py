import click
from .config import get_mirrors, get_current_mirror, set_current_mirror,add_mirror,remove_mirror, rename_mirror
from .mirror import test_mirrors

@click.group()
def cli():
    """Python Pip Mirror Manager"""
    pass

@cli.command()
def ls():
    """列出所有可用的镜像"""
    mirrors = get_mirrors()
    output_lines = []
    for name, url in mirrors.items():
        stars = "*" if url == get_current_mirror() else " "
        stars = click.style(stars, fg='green')
        output_lines.append(f"{stars.ljust(2)} {name.ljust(10)} {url}")
    click.echo("\n".join(output_lines))

@cli.command()
@click.argument("name")
def use(name):
    """切换到指定的镜像"""
    mirrors = get_mirrors()
    if name in mirrors:
        set_current_mirror(mirrors[name])
        click.echo(f"Switched to {name}")
    else:
        click.echo(f"Mirror {name} not found")

@cli.command()
def test():
    """测试所有可用的镜像"""
    mirrors = get_mirrors()
    current = get_current_mirror()
    key = next((key for key, val in mirrors.items() if val == current), None)
    results = test_mirrors()
    output_lines = []
    for name, time in results.items():
        stars = " "
        if name == key:
            stars = click.style('*', fg='green')
            time = click.style(time, bg='green')
        output_lines.append(f"{stars.ljust(1)} {name.ljust(10)} {time}")
    click.echo("\n".join(output_lines))

@cli.command()
def current():
    """显示当前使用的镜像"""
    current_mirror = get_current_mirror()
    click.echo(f"Current mirror: {current_mirror}")

@cli.command()
@click.argument("name")
@click.argument("url")
def add(name, url):
    """添加一个新的镜像"""
    add_mirror(name, url)

@cli.command()
@click.argument("name")
def rm(name):
    """删除一个已有的镜像"""
    remove_mirror(name)

@cli.command()
@click.argument("old_name")
@click.argument("new_name")
def rename(old_name, new_name):
    """重命名一个已有的镜像"""
    rename_mirror(old_name, new_name)


@cli.command()
def help():
    """显示帮助信息"""
    help_text = """
    ppmm: Python Pip Mirror Manager
    Usage: mm <command>
        Commands:
        ls                              List all mirrors
        use <name>                      Switch to a specific mirror
        test                            Test all mirrors
        current                         Show current mirror
        add <name> <url>                Add a new mirror
        rm <name>                       Delete an existing mirror
        rename <old_name> <new_name>    Rename a mirror
        help                            Show this help message
    """
    click.echo(help_text)


if __name__ == "__main__":
    cli()