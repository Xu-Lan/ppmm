import subprocess, json, pkg_resources, urllib.request, time, http.client
from click import echo, style

Status = {"success": "✅", "fail": "❌", "warning": "⚠️", "info": "ℹ️"}
config_path = pkg_resources.resource_filename("ppmm", "data.json")
with open(config_path, "r", encoding="utf-8") as f:
    mirrors = json.load(f)["mirrors"]


def get_mirrors():
    return mirrors


def use_mirror(name):
    mirrors = get_mirrors()
    if name in mirrors:
        result = subprocess.run(
            ["pip", "config", "set", "global.index-url", mirrors[name]],
            capture_output=True,  # 捕获输出
            text=True,  # 以文本形式返回输出
        )
        if result.stdout:
            echo(f"{Status['success']} The mirror has been changed to '{name}'.")
        if result.stderr:
            echo(style(f"{Status['fail']} {result.stderr}", fg="red"))
    else:
        echo(style(f"{Status['fail']} The mirror '{name}' is not found.", fg="red"))


def get_current_mirror():
    result = subprocess.run(
        ["pip", "config", "get", "global.index-url"], capture_output=True, text=True
    )
    return result

def print_current_mirror():
    result = get_current_mirror()
    if result.stdout:
        current_mirror = result.stdout.strip()
        for key in mirrors:
            if mirrors[key] == current_mirror:
                echo(f"{Status['info']} You are using {style(key,fg='green')} mirror.")
                return key
        echo(f"{Status['info']} Your current mirror({current_mirror}) is not included in the ppmm mirrors.")
        echo(f"{Status['info']} Use the mm add {style('<mirror> <url>', fg='green')} command to add your mirrors.")
    if result.stderr:
        echo(style(f"{Status['fail']} {result.stderr}", fg="red"))


def add_mirror(name, url):
    if name in mirrors or url in mirrors.values():
        echo(
            style(
                f"{Status['fail']} The mirror name or url is already included in the ppmm mirrors. Please make sure that the name and url are unique.",
                fg="red",
            )
        )
        return
    mirrors[name] = url
    save_config()
    echo(
        f"{Status['success']}  Add mirror '{name}' success, run {style(f'mm use {name}', fg='green')} command to use '{name}' mirror."
    )


def remove_mirror(name):
    if name not in mirrors:
        echo(style(f"{Status['fail']} The mirror '{name}' is not found.", fg="red"))
        return
    del mirrors[name]
    save_config()
    echo(f"{Status['success']} The mirror '{name}' has been deleted successfully.")


def rename_mirror(old_name, new_name):
    if old_name not in mirrors:
        echo(style(f"{Status['fail']} The mirror '{old_name}' is not found.", fg="red"))
        return
    if new_name in mirrors:
        echo(
            style(
                f"{Status['fail']}  ERROR  The new mirror name '{new_name}' is already exist",
                fg="red",
            )
        )
        return
    mirrors[new_name] = mirrors.pop(old_name)
    save_config()
    echo(
        f"{Status['success']}  The mirror '{old_name}' has been renamed to '{new_name}'."
    )


def test_mirrors():
    mirrors = get_mirrors()
    results = {}
    TIMEOUT = 3
    for name, url in mirrors.items():
        try:
            start_time = time.time()
            with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
                end_time = time.time()
                latency = str(int((end_time - start_time) * 1000)) + " ms"
                results[name] = latency
        except urllib.error.URLError as e:
            results[name] = f"timeout (Fetch timeout over {TIMEOUT * 1000} ms)"
        except http.client.RemoteDisconnected as e:
            results[name] = (
                f"disconnected (Server closed the connection without response)"
            )
        except Exception as e:
            results[name] = f"ERROR ({str(e)})"
    return results


def save_config():
    with open(config_path, "w", encoding="utf-8") as f:
        data = {"mirrors": mirrors}
        json.dump(data, f, indent=4, ensure_ascii=False)
