import ctypes
import http.client
import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# 状态符号
Status = {"success": "✅", "fail": "❌", "warning": "⚠️", "info": "ℹ️"}


# ANSI 转义码定义颜色
class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def enable_ansi_colors():
    """启用ANSI转义码"""
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            if not kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7):
                print(
                    f"{Status['warning']} 警告: ANSI转义码启用失败, 可能导致命令行输出显示不正常"
                )
        except Exception as e:
            print(
                f"{Status['warning']} 警告: ANSI转义码启用时出错({str(e)}), 可能导致命令行输出显示不正常"
            )

current_dir = Path(__file__).parent
config_path = current_dir / "data.json"

with open(config_path, "r", encoding="utf-8") as f:
    mirrors = json.load(f)["mirrors"]


def echo(message, color=Colors.RESET):
    """带颜色的打印函数"""
    print(f"{color}{message}{Colors.RESET}")


def get_current_mirror():
    """获取当前pip镜像源，直接返回URL字符串"""
    result = subprocess.run(
        ["pip", "config", "get", "global.index-url"], capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


def save_config():
    """保存配置到文件"""
    with open(config_path, "w", encoding="utf-8") as f:
        data = {"mirrors": mirrors}
        json.dump(data, f, indent=4, ensure_ascii=False)


def ls():
    """列出所有镜像源"""
    current_mirror = get_current_mirror()

    echo("\n可用镜像源列表:", Colors.BOLD)
    for name, url in mirrors.items():
        star = f"{Colors.GREEN}*{Colors.RESET}" if url == current_mirror else " "
        echo(f"  {star} {name.ljust(14, '-')} {url}")
    print()


def use(name):
    """切换镜像源"""
    if name in mirrors:
        result = subprocess.run(
            ["pip", "config", "set", "global.index-url", mirrors[name]],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            echo(f"{Status['success']} 已成功切换镜像源到 '{name}'", Colors.GREEN)
        else:
            error_msg = result.stderr.strip() if result.stderr else "未知错误"
            echo(f"{Status['fail']} 切换镜像源失败: {error_msg}", Colors.RED)
    else:
        available = ", ".join(mirrors.keys())
        echo(
            f"{Status['fail']} 未找到镜像源 '{name}'，可用镜像源有: {available}",
            Colors.RED,
        )


def current():
    """显示当前使用的镜像源"""
    current_mirror = get_current_mirror()
    if current_mirror:
        for name, url in mirrors.items():
            if url == current_mirror:
                echo(
                    f"{Status['info']} 当前正在使用 {Colors.GREEN}{name}{Colors.RESET} 镜像源"
                )
                return
        echo(f"{Status['info']} 当前镜像源({current_mirror})不在ppmm管理的镜像列表中")
        echo(
            f"{Status['info']} 使用 {Colors.GREEN}mm add <名称> <URL>{Colors.RESET} 命令添加镜像源"
        )
    else:
        echo(f"{Status['fail']} 获取当前镜像源失败", Colors.RED)


def add(name, url):
    """添加新镜像源"""
    if name in mirrors:
        echo(f"{Status['fail']} 镜像名称 '{name}' 已存在", Colors.RED)
        return
    if url in mirrors.values():
        echo(f"{Status['fail']} 镜像URL '{url}' 已存在", Colors.RED)
        return

    mirrors[name] = url
    save_config()
    echo(f"{Status['success']} 已成功添加镜像源 '{name}'", Colors.GREEN)
    echo(
        f"\n{Colors.BLUE}提示:{Colors.RESET} 使用 {Colors.GREEN}mm use {name}{Colors.RESET} 命令切换到此镜像源"
    )


def rm(name):
    """删除镜像源"""
    if name not in mirrors:
        echo(f"{Status['fail']} 未找到镜像源 '{name}'", Colors.RED)
        return

    del mirrors[name]
    save_config()
    echo(f"{Status['success']} 已成功删除镜像源 '{name}'", Colors.GREEN)


def rename(old_name, new_name):
    """重命名镜像源"""
    if old_name not in mirrors:
        echo(f"{Status['fail']} 未找到镜像源 '{old_name}'", Colors.RED)
        return
    if new_name in mirrors:
        echo(f"{Status['fail']} 新名称 '{new_name}' 已存在", Colors.RED)
        return

    mirrors[new_name] = mirrors.pop(old_name)
    save_config()
    echo(
        f"{Status['success']} 已成功将镜像源 '{old_name}' 重命名为 '{new_name}'",
        Colors.GREEN,
    )


def edit(name, url):
    """编辑镜像源URL"""
    if name not in mirrors:
        echo(f"{Status['fail']} 未找到镜像源 '{name}'", Colors.RED)
        return

    mirrors[name] = url
    save_config()
    echo(f"{Status['success']} 已成功更新镜像源 '{name}' 的URL", Colors.GREEN)


def test_mirror(url, timeout):
    """测试单个镜像源的响应时间"""
    try:
        # 确保URL以/结尾，避免重定向
        if not url.endswith("/"):
            url += "/"

        # 创建请求对象，使用HEAD方法
        req = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": "ppmm-mirror-tester/1.0"}
        )

        start_time = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # 确保得到的是HEAD响应而不是重定向后的GET
            if response.status == 200 and response.getheader("Content-Length"):
                end_time = time.time()
                latency = int((end_time - start_time) * 1000)
                return f"{latency} ms"
            else:
                return "无效响应 (非200状态)"

    except urllib.error.HTTPError as e:
        # 如果不支持HEAD方法，回退到GET
        if e.code == 405:
            return test_with_get(url, timeout)
        return f"HTTP错误 ({e.code})"
    except urllib.error.URLError as e:
        # 捕获 URLError 并根据原因进行更详细的判断
        if isinstance(e.reason, TimeoutError):
            return "请求超时"
        elif isinstance(e.reason, ConnectionRefusedError):
            return "连接被拒绝"
        elif isinstance(e.reason, socket.gaierror):
            return "DNS解析失败"
        return f"URL错误 ({str(e.reason)})"
    except ValueError as e:
        return f"URL格式错误 ({str(e)})"
    except http.client.RemoteDisconnected:
        return "连接断开 (服务器无响应)"
    except Exception as e:
        return f"未知错误 ({str(e)})"


def test_with_get(url, timeout):
    """当HEAD方法不被支持时的GET方法回退"""
    try:
        start_time = time.time()
        with urllib.request.urlopen(url, timeout=timeout) as response:
            # 只读取前1字节确认连接有效
            response.read(1)
            end_time = time.time()
            latency = int((end_time - start_time) * 1000)
            return f"{latency} ms (GET)"
    except Exception as e:
        return f"错误 ({str(e)})"


def test():
    """测试所有镜像源的响应速度"""
    timeout = 5
    results = {}
    current_mirror = get_current_mirror()

    echo(f"{Status['info']} 正在测试镜像源响应速度(超时: {timeout}秒)...", Colors.GREEN)

    with ThreadPoolExecutor(max_workers=len(mirrors)) as executor:
        futures = {
            name: executor.submit(test_mirror, url, timeout)
            for name, url in mirrors.items()
        }

        for name, future in futures.items():
            results[name] = future.result()

    # 显示测试结果
    echo(f"\n{Colors.BOLD}镜像源响应速度测试结果:{Colors.RESET}")
    for name, url in mirrors.items():
        # 标记当前使用的镜像源
        star = f"{Colors.GREEN}*{Colors.RESET}" if url == current_mirror else " "
        latency = results[name]
        # 包含ms则为正常响应，否则为错误信息
        if "ms" in latency:
            latency_value = latency.split()[0]
            latency_text = f"{Colors.CYAN}{latency_value}{Colors.RESET} ms"
        else:
            latency_text = f"{Colors.RED}{latency}{Colors.RESET}"

        echo(f"  {star} {name.ljust(14, '-')} {latency_text}")
    print()


def help():
    """显示美观的帮助信息"""
    help_text = f"""
{Colors.BOLD}{Colors.MAGENTA}╔════════════════════════════════════════════╗
║{Colors.GREEN}  ppmm: Python Pip 镜像源管理工具  {Colors.MAGENTA}         ║
╚════════════════════════════════════════════╝{Colors.RESET}

{Colors.BOLD}使用方法:{Colors.RESET} mm {Colors.CYAN}<命令>{Colors.RESET} [参数]

{Colors.BOLD}命令列表:{Colors.RESET}

  {Colors.BOLD}ls{Colors.RESET}
    {Colors.CYAN}↳ 列出所有可用镜像源{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}use {Colors.YELLOW}<名称>{Colors.RESET}
    {Colors.CYAN}↳ 切换到指定镜像源{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}test{Colors.RESET}
    {Colors.CYAN}↳ 测试所有镜像源的响应速度{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}current{Colors.RESET}
    {Colors.CYAN}↳ 显示当前使用的镜像源{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}add {Colors.YELLOW}<名称> <URL>{Colors.RESET}
    {Colors.CYAN}↳ 添加新的镜像源{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}edit {Colors.YELLOW}<名称> <URL>{Colors.RESET}
    {Colors.CYAN}↳ 修改指定镜像源的URL{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}rm {Colors.YELLOW}<名称>{Colors.RESET}
    {Colors.CYAN}↳ 删除指定的镜像源{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}rename {Colors.YELLOW}<旧名称> <新名称>{Colors.RESET}
    {Colors.CYAN}↳ 重命名镜像源{Colors.RESET}
    {"─" * 60}

  {Colors.BOLD}help{Colors.RESET}
    {Colors.CYAN}↳ 显示本帮助信息{Colors.RESET}
    {"─" * 60}
"""
    print(help_text)
