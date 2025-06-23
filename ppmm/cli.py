import argparse

from .core import (
    add,
    current,
    edit,
    enable_ansi_colors,
    help,
    ls,
    rename,
    rm,
    test,
    use,
)


def main():
    enable_ansi_colors()
    parser = argparse.ArgumentParser(prog="mm", description="Python Pip 镜像源管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # ls 命令
    subparsers.add_parser("ls", help="列出所有镜像源")

    # use 命令
    use_parser = subparsers.add_parser("use", help="切换到指定镜像源")
    use_parser.add_argument("name", help="镜像源名称")

    # current 命令
    subparsers.add_parser("current", help="显示当前使用的镜像源")

    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新的镜像源")
    add_parser.add_argument("name", help="新镜像源名称")
    add_parser.add_argument("url", help="新镜像源URL")

    # rm 命令
    rm_parser = subparsers.add_parser("rm", help="删除指定的镜像源")
    rm_parser.add_argument("name", help="要删除的镜像源名称")

    # rename 命令
    rename_parser = subparsers.add_parser("rename", help="重命名镜像源")
    rename_parser.add_argument("old_name", help="当前镜像源名称")
    rename_parser.add_argument("new_name", help="新的镜像源名称")

    # edit 命令
    edit_parser = subparsers.add_parser("edit", help="修改指定镜像源的URL")
    edit_parser.add_argument("name", help="要修改的镜像源名称")
    edit_parser.add_argument("url", help="新的镜像源URL")

    # test 命令
    subparsers.add_parser("test", help="测试所有镜像源的响应速度")

    # help 命令
    subparsers.add_parser("help", help="显示帮助信息")

    # 解析命令行参数
    args = parser.parse_args()

    command_handlers = {
        "ls": lambda: ls(),
        "use": lambda: use(args.name),
        "current": lambda: current(),
        "add": lambda: add(args.name, args.url),
        "rm": lambda: rm(args.name),
        "rename": lambda: rename(args.old_name, args.new_name),
        "edit": lambda: edit(args.name, args.url),
        "test": lambda: test(),
        "help": lambda: help(),
    }

    handler = command_handlers.get(args.command)
    if handler:
        handler()
    else:
        help()


if __name__ == "__main__":
    main()
