import urllib.request, time, http.client
from .config import get_mirrors

def test_mirrors():
    mirrors = get_mirrors()
    results = {}
    TIMEOUT = 3
    for name, url in mirrors.items():
        try:
            start_time = time.time()
            with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
                end_time = time.time()
                latency = str(int((end_time - start_time) * 1000)) + ' ms'
                results[name] = latency
        except urllib.error.URLError as e:
            results[name] = f"timeout (Fetch timeout over {TIMEOUT * 1000} ms)"
        except http.client.RemoteDisconnected as e:
            results[name] = f"disconnected (Server closed the connection without response)"
        except Exception as e:
            results[name] = f"error ({str(e)})"
    return results