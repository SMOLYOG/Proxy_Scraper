import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time

PROXY_TYPES = {
    "1": "http",
    "2": "socks4",
    "3": "socks5"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def display_logo():
    logo = """
    _                 _______  _______  _______    _______  _______  _______  _______  _______  _______  _______ 
    ( (    /||\\     /|(  ____ \\(  ___  )(  ____ \\  (  ____ \\(  ____ \\(  ____ )(  ___  )(  ____ )(  ____ \\(  ____ )
    |  \\  ( |( \\   / )| (    \\/| (   ) || (    \\/  | (    \\/| (    \\/| (    )|| (   ) || (    )|| (    \\/| (    )|
    |   \\ | | \\ (_) / | |      | (___) || (_____   | (_____ | |      | (____)|| (___) || (____)|| (__    | (____)|
    | (\\ \\) |  \\   /  | | ____ |  ___  |(_____  )  (_____  )| |      |     __)|  ___  ||  _____)|  __)   |     __)
    | | \\   |   ) (   | | \\_  )| (   ) |      ) |        ) || |      | (\\ (   | (   ) || (      | (      | (\\ (   
    | )  \\  |   | |   | (___) || )   ( |/\\____) |  /\\____) || (____/\\| ) \\ \\__| )   ( || )      | (____/\\| ) \\ \\__
    |/    )_)   \\_/   (_______)|/     \\|\\_______)  \\_______)(_______/|/   \\__/|/     \\||/       (_______/|/   \\__/
    """
    print(logo)

def fetch_free_proxy_list():
    print("[+] free-proxy-list.net")
    proxies = []
    try:
        response = requests.get("https://free-proxy-list.net/", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"id": "proxylisttable"})
        if table and table.tbody:
            for row in table.tbody.find_all("tr"):
                cols = row.find_all("td")
                ip = cols[0].text
                port = cols[1].text
                https = cols[6].text == "yes"
                ptype = "https" if https else "http"
                proxies.append((ptype, f"{ip}:{port}"))
        else:
            print("[-] Error: Proxy table not found (free-proxy-list.net)")
    except Exception as e:
        print(f"[-] Error: {e}")
    return proxies

def fetch_proxy_list_download(ptype):
    print(f"[+] proxy-list.download ({ptype})")
    proxies = []
    try:
        url = f"https://www.proxy-list.download/api/v1/get?type={ptype}"
        r = requests.get(url, timeout=10)
        for line in r.text.splitlines():
            if ":" in line:
                proxies.append((ptype, line.strip()))
    except Exception as e:
        print(f"[-] Error: {e}")
    return proxies

def fetch_proxyscan():
    print("[+] proxyscan.io")
    proxies = []
    try:
        r = requests.get("https://www.proxyscan.io/api/proxy?last_check=1000&limit=50", timeout=10)
        for item in r.json():
            ip = item["Ip"]
            port = item["Port"]
            ptype = item["Type"][0].lower()
            proxies.append((ptype, f"{ip}:{port}"))
    except Exception as e:
        print(f"[-] Error: {e}")
    return proxies

def fetch_openproxy_space():
    print("[+] openproxy.space")
    urls = [
        "https://openproxy.space/list/http",
        "https://openproxy.space/list/socks4",
        "https://openproxy.space/list/socks5",
    ]
    proxies = []
    for url in urls:
        try:
            ptype = url.split("/")[-1]
            r = requests.get(url, timeout=10)
            for line in r.text.splitlines():
                if ":" in line:
                    proxies.append((ptype, line.strip()))
        except Exception as e:
            print(f"[-] Error: {e}")
    return proxies

def fetch_from_github():
    print("[+] GitHub – TheSpeedX/PROXY-List")
    base = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/main/{}/proxy.txt"
    proxies = []
    for ptype in ["http", "socks4", "socks5"]:
        try:
            r = requests.get(base.format(ptype), timeout=10)
            for line in r.text.splitlines():
                if ":" in line:
                    proxies.append((ptype, line.strip()))
        except Exception as e:
            print(f"[-] Error: {e}")
    return proxies

def fetch_shiftytr():
    print("[+] GitHub – ShiftyTR/Proxy-List")
    proxies = []
    try:
        for ptype in ["http", "socks4", "socks5"]:
            url = f"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/{ptype}.txt"
            r = requests.get(url, timeout=10)
            for line in r.text.splitlines():
                if ":" in line:
                    proxies.append((ptype, line.strip()))
    except Exception as e:
        print(f"[-] Error: {e}")
    return proxies

def fetch_jetkai():
    print("[+] GitHub – jetkai/proxy-list")
    proxies = []
    try:
        for ptype in ["http", "socks4", "socks5"]:
            url = f"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-{ptype}.txt"
            r = requests.get(url, timeout=10)
            for line in r.text.splitlines():
                if ":" in line:
                    proxies.append((ptype, line.strip()))
    except Exception as e:
        print(f"[-] Error: {e}")
    return proxies

def fetch_proxyspace():
    print("[+] proxyspace.pro")
    proxies = []
    try:
        r = requests.get("https://proxyspace.pro/http.txt", timeout=10)
        for line in r.text.splitlines():
            if ":" in line:
                proxies.append(("http", line.strip()))
    except Exception as e:
        print(f"[-] Error: {e}")
    return proxies

def scrape_all(selected_types):
    all_proxies = []
    all_proxies += fetch_free_proxy_list()
    all_proxies += fetch_proxy_list_download("socks4")
    all_proxies += fetch_proxy_list_download("socks5")
    all_proxies += fetch_proxyscan()
    all_proxies += fetch_openproxy_space()
    all_proxies += fetch_from_github()
    all_proxies += fetch_shiftytr()
    all_proxies += fetch_jetkai()
    all_proxies += fetch_proxyspace()

    filtered = [p for p in all_proxies if p[0] in selected_types]
    return list(set(filtered))

def save_to_separate_files(proxies):
    grouped = {}
    for ptype, proxy in proxies:
        grouped.setdefault(ptype, []).append(proxy)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    if not grouped:
        print("[-] No proxies found for the selected type.")
        return
    
    total_proxies = 0
    for ptype, proxy_list in grouped.items():
        filename = f"{ptype}_proxies_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write("\n".join(proxy_list))
        total_proxies += len(proxy_list)
        print(f"[✓] Saved {len(proxy_list)} to file: {filename}")
    
    print(f"\n[✓] Download completed. Total number of proxies: {total_proxies}")

def show_proxy_options():
    print("Select proxy types:")
    for num, name in PROXY_TYPES.items():
        print(f"  {num}. {name.upper()}")
    print("> ", end="")

if __name__ == "__main__":
    display_logo()

    show_proxy_options()
    user_input = input().replace(" ", "").split(",")
    selected_types = [PROXY_TYPES[num] for num in user_input if num in PROXY_TYPES]

    if not selected_types:
        print("[-] No valid proxy types selected.")
    else:
        proxies = scrape_all(selected_types)
        save_to_separate_files(proxies)

    time.sleep(3)
