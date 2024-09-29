import subprocess, json
import pkg_resources

config_path = pkg_resources.resource_filename('ppmm', 'data.json')
with open(config_path, "r", encoding="utf-8") as f:
    mirrors = json.load(f)["mirrors"]


def get_mirrors():
    return mirrors


def get_current_mirror():
    pip_config_output = subprocess.run(
        ["pip", "config", "get", "global.index-url"], capture_output=True, text=True
    )
    if pip_config_output.stdout.strip():
        return pip_config_output.stdout.strip()
    return mirrors["pip"]


def set_current_mirror(url):
    subprocess.run(["pip", "config", "set", "global.index-url", url])


def add_mirror(name, url):
    if name in mirrors:
        print(f"Mirror with name '{name}' already exists.")
        return
    mirrors[name] = url
    save_config()
    print(f"Added mirror '{name}' successfully.")


def remove_mirror(name):
    if name not in mirrors:
        print(f"Mirror with name '{name}' does not exist.")
        return
    del mirrors[name]
    save_config()
    print(f"Mirror '{name}' has been deleted successfully.")


def rename_mirror(old_name, new_name):
    if old_name not in mirrors:
        print(f"Mirror with name '{old_name}' does not exist.")
        return
    if new_name in mirrors:
        print(f"Mirror with name '{new_name}' already exists.")
        return
    mirrors[new_name] = mirrors.pop(old_name)
    save_config()
    print(f"Renamed mirror from '{old_name}' to '{new_name}' successfully.")


def save_config():
    with open(config_path, "w", encoding="utf-8") as f:
        data = {"mirrors": mirrors}
        json.dump(data, f, indent=4, ensure_ascii=False)
