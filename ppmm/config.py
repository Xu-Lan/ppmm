import subprocess

DEFAULT_MIRRORS = {
    "pip": "https://pypi.org/simple/",
    "thu": "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "ustc": "https://pypi.mirrors.ustc.edu.cn/simple/",
    "ali": "https://mirrors.aliyun.com/pypi/simple/",
    "tencent": "http://mirrors.cloud.tencent.com/pypi/simple/"
}


def get_mirrors():
    return DEFAULT_MIRRORS

def get_current_mirror():
    pip_config_output = subprocess.run(
        ["pip", "config", "get", "global.index-url"], capture_output=True, text=True
    )
    if pip_config_output.stdout.strip():
        return pip_config_output.stdout.strip()
    return DEFAULT_MIRRORS["pip"]


def set_current_mirror(url):
    subprocess.run(["pip", "config", "set", "global.index-url", url])
