# 🕸️ Multi-Source Proxy Scraper

A Python tool to scrape free proxies from multiple sources simultaneously. Supports **HTTP**, **SOCKS4**, and **SOCKS5**. Results are saved in separate timestamped files.

---

## Features
- Scrapes proxies from:
  - free-proxy-list.net
  - proxy-list.download
  - proxyscan.io
  - openproxy.space
  - proxyspace.pro
  - GitHub repositories: TheSpeedX, ShiftyTR, jetkai
- Filters by type (HTTP/SOCKS4/SOCKS5)
- Saves proxies to separate `.txt` files with timestamp
- Simple CLI interface

---

## Installation
```bash
git clone https://github.com/yourusername/multi-proxy-scraper.git
cd multi-proxy-scraper
pip install -r requirements.txt
```

---

## Usage
```bash
python NYGAS_SCRAPER.py
```

Select proxy types by entering numbers (e.g., `1,3`):

```
  1. HTTP
  2. SOCKS4
  3. SOCKS5
> 1,3
```

Example output files:
```
http_proxies_2025-08-14_12-00-00.txt
socks5_proxies_2025-08-14_12-00-00.txt
```

---

## License
MIT License – free to use and modify.
