#!/usr/bin/env python3
"""
================================================================================
  Work's Tool v3.1 - Professional Cybersecurity Assessment Framework
  FIXED: Proper connection validation and real results only
  For Authorized Security Testing Only
================================================================================
"""

import sys
import os
import platform
import socket
import threading
import hashlib
import itertools
import string
import time
import struct
import ssl
import ftplib
import json
import re
import signal
import binascii
import base64
import ipaddress
import concurrent.futures
from datetime import datetime

# ===========================================================================
#  WINDOWS COMPATIBILITY
# ===========================================================================

def enable_windows_ansi():
    if platform.system() != "Windows":
        return True
    try:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.GetStdHandle(-11)
        m = ctypes.c_ulong()
        k.GetConsoleMode(h, ctypes.byref(m))
        k.SetConsoleMode(h, m.value | 0x0004 | 0x0001)
        return True
    except Exception:
        pass
    try:
        os.system("")
        return True
    except Exception:
        pass
    try:
        import colorama
        colorama.init()
        return True
    except ImportError:
        pass
    return False

enable_windows_ansi()

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import zipfile as zf
    HAS_ZIPFILE = True
except ImportError:
    HAS_ZIPFILE = False

try:
    import urllib.request
    import urllib.parse
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


# ===========================================================================
#  COLORS
# ===========================================================================

class C:
    P  = "\033[38;5;129m"
    LP = "\033[38;5;141m"
    DP = "\033[38;5;93m"
    M  = "\033[38;5;165m"
    W  = "\033[38;5;255m"
    G  = "\033[38;5;245m"
    R  = "\033[38;5;196m"
    GR = "\033[38;5;82m"
    Y  = "\033[38;5;220m"
    CY = "\033[38;5;87m"
    B  = "\033[1m"
    RS = "\033[0m"


# ===========================================================================
#  BUILT-IN WORDLISTS
# ===========================================================================

BUILTIN_PASSWORDS = [
    "", "password", "123456", "12345678", "qwerty", "abc123", "monkey",
    "master", "dragon", "111111", "baseball", "iloveyou", "trustno1",
    "sunshine", "football", "shadow", "123123", "654321", "superman",
    "qazwsx", "michael", "Password1", "password1", "password123",
    "admin", "admin123", "admin1234", "administrator", "root", "toor",
    "letmein", "welcome", "login", "passw0rd", "hello", "charlie",
    "qwerty123", "pass123", "pass1234", "1234", "12345", "123456789",
    "0987654321", "abcdef", "test", "test123", "guest", "guest123",
    "mysql", "user", "user123", "demo", "oracle", "postgres",
    "changeme", "changeit", "secret", "default", "access", "server",
    "computer", "internet", "service", "canada", "killer", "george",
    "andrew", "jessica", "pepper", "joshua", "hunter", "ranger",
    "harley", "thomas", "hockey", "robert", "daniel", "starwars",
    "jordan", "dallas", "summer", "albert", "maxwell", "arsenal",
    "batman", "soccer", "tigger", "buster", "ginger", "hammer",
    "silver", "cookie", "1111", "2222", "3333", "4444", "5555",
    "6666", "7777", "8888", "9999", "0000", "p@ssw0rd", "P@ssw0rd",
    "P@ssword1", "Welcome1", "Welcome123", "Qwerty123", "Letmein1",
    "abc@123", "test@123", "admin@123", "Winter2024", "Summer2024",
    "Winter2025", "Summer2025", "Company1", "Company123", "Temp1234",
    "Password!", "Password1!", "!@#$%^&*", "administrator1",
]

BUILTIN_USERNAMES = [
    "admin", "root", "user", "test", "guest", "info", "mysql",
    "oracle", "postgres", "administrator", "webmaster", "sysadmin",
    "operator", "support", "backup", "ftp", "www", "web", "mail",
    "postmaster", "service", "daemon", "nobody", "www-data",
    "apache", "nginx", "tomcat", "manager", "deploy", "jenkins",
    "git", "developer", "dev", "sa", "demo", "anonymous",
]

BUILTIN_DIRS = [
    "admin", "administrator", "login", "wp-admin", "wp-login",
    "dashboard", "panel", "cpanel", "webmail", "phpmyadmin",
    "api", "v1", "v2", "docs", "test", "dev", "staging",
    "backup", "backups", "uploads", "upload", "download",
    "media", "static", "assets", "css", "js", "img", "images",
    "lib", "vendor", "dist", "build", "bin", "src", "config",
    "database", "db", "data", "log", "logs", "private", "public",
    "env", ".env", ".git", ".svn", ".htaccess", ".htpasswd",
    "wp-content", "wp-includes", "wp-config", "robots", "robots.txt",
    "server-status", "info", "phpinfo", "cgi-bin", "status",
    "health", "metrics", "user", "users", "register", "signup",
    "signin", "logout", "auth", "oauth", "search", "blog",
    "forum", "shop", "store", "cart", "checkout", "portal",
    "app", "feed", "rss", "readme", "changelog", "license",
]

BUILTIN_EXTENSIONS = [
    "", ".php", ".html", ".htm", ".asp", ".aspx", ".jsp", ".txt",
    ".xml", ".json", ".bak", ".old", ".log", ".sql", ".conf",
    ".config", ".ini", ".env", ".zip", ".tar", ".gz",
]


# ===========================================================================
#  SERVICE DATABASE
# ===========================================================================

SERVICE_PROBES = {
    21: b"\r\n", 22: b"\r\n", 23: b"\r\n",
    25: b"EHLO workstool\r\n",
    80: b"GET / HTTP/1.1\r\nHost: target\r\nUser-Agent: WorksTool/3.1\r\nConnection: close\r\n\r\n",
    110: b"\r\n", 143: b"\r\n",
    443: b"GET / HTTP/1.1\r\nHost: target\r\nUser-Agent: WorksTool/3.1\r\nConnection: close\r\n\r\n",
    993: b"\r\n", 995: b"\r\n", 3306: b"\r\n",
    5432: b"\x00\x00\x00\x08\x04\xd2\x16\x2f",
    6379: b"PING\r\n",
    8080: b"GET / HTTP/1.1\r\nHost: target\r\nUser-Agent: WorksTool/3.1\r\nConnection: close\r\n\r\n",
    8443: b"GET / HTTP/1.1\r\nHost: target\r\nUser-Agent: WorksTool/3.1\r\nConnection: close\r\n\r\n",
}

SERVICE_NAMES = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    80: "http", 110: "pop3", 143: "imap", 389: "ldap",
    443: "https", 445: "microsoft-ds", 465: "smtps",
    587: "submission", 993: "imaps", 995: "pop3s",
    1433: "ms-sql", 1521: "oracle", 3306: "mysql",
    3389: "rdp", 5432: "postgresql", 5900: "vnc",
    6379: "redis", 8080: "http-proxy", 8443: "https-alt",
    8888: "http-alt", 9200: "elasticsearch",
    11211: "memcached", 27017: "mongodb",
}

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 161,
    389, 443, 445, 465, 587, 631, 636, 993, 995, 1433, 1521,
    1723, 2049, 3306, 3389, 5432, 5900, 5984, 6379, 6667,
    8000, 8080, 8443, 8888, 9200, 9418, 11211, 27017,
]


# ===========================================================================
#  DISPLAY ENGINE
# ===========================================================================

class D:
    @staticmethod
    def clear():
        os.system("cls" if platform.system() == "Windows" else "clear")

    @staticmethod
    def banner():
        print(rf"""
{C.DP}    +==================================================================+
    |                                                                  |
{C.P}    |   ##      ## ####### ######  ##   ## #######                    |
    |   ##  ##  ## ##   ## ##   ## ## ##  ##                            |
    |   ## #### ## ##   ## ######  ####   #######                      |
    |   ## #### ## ##   ## ##  ##  ## ##       ##                      |
    |    ##  ##   ####### ##   ## ##   ## #######                      |
{C.LP}    |                                                                  |
    |              ######## ####### ####### ##                          |
    |                 ##    ##   ## ##   ## ##                          |
    |                 ##    ##   ## ##   ## ##                          |
    |                 ##    ##   ## ##   ## ##                          |
    |                 ##    ####### ####### #######                     |
{C.DP}    |                                                                  |
    |  {C.G}Professional Cybersecurity Assessment Framework       v3.1{C.DP}   |
    |  {C.G}For Authorized Security Testing Only{C.DP}                        |
    +==================================================================+{C.RS}
""")

    @staticmethod
    def section(t):
        w = 66
        print(f"\n{C.DP}    +{'=' * w}+")
        print(f"    |{C.P}{C.B}  {t.upper()}{' ' * (w - len(t) - 2)}{C.RS}{C.DP}|")
        print(f"    +{'=' * w}+{C.RS}")

    @staticmethod
    def info(m):
        print(f"    {C.P}[*]{C.W} {m}{C.RS}")

    @staticmethod
    def ok(m):
        print(f"    {C.GR}[+]{C.W} {m}{C.RS}")

    @staticmethod
    def warn(m):
        print(f"    {C.Y}[!]{C.W} {m}{C.RS}")

    @staticmethod
    def err(m):
        print(f"    {C.R}[-]{C.W} {m}{C.RS}")

    @staticmethod
    def res(m):
        print(f"    {C.M}[>]{C.CY} {m}{C.RS}")

    @staticmethod
    def line():
        print(f"    {C.DP}{'=' * 66}{C.RS}")

    @staticmethod
    def progress(cur, tot, pre="Progress"):
        bl = 40
        f = int(bl * cur / tot) if tot > 0 else 0
        bar = f"{'#' * f}{'-' * (bl - f)}"
        pct = (cur / tot * 100) if tot > 0 else 0
        sys.stdout.write(f"\r    {C.P}[*]{C.W} {pre}: {C.DP}[{bar}]{C.W} {pct:6.2f}%{C.RS}")
        sys.stdout.flush()
        if cur >= tot:
            print()

    @staticmethod
    def th(cols, ws):
        h = "    "
        s = "    "
        for c, w in zip(cols, ws):
            h += f"{C.B}{C.P}{c:<{w}}{C.RS}"
            s += f"{C.G}{'-' * w}{C.RS}"
        print(h)
        print(s)

    @staticmethod
    def tr(vals, ws):
        cs = [C.W, C.LP, C.CY, C.GR, C.Y, C.M]
        r = "    "
        for i, (v, w) in enumerate(zip(vals, ws)):
            r += f"{cs[i % len(cs)]}{str(v):<{w}}{C.RS}"
        print(r)

    @staticmethod
    def ask(m, d=None):
        dd = f" [{C.LP}{d}{C.RS}]" if d else ""
        try:
            v = input(f"    {C.P}[?]{C.W} {m}{dd}: {C.CY}").strip()
            print(C.RS, end="")
            return v if v else (d or "")
        except (EOFError, KeyboardInterrupt):
            print(C.RS)
            return d or ""

    @staticmethod
    def yn(m, d=True):
        dd = "Y/n" if d else "y/N"
        v = D.ask(m, dd)
        if v.lower() in ("y", "yes", "y/n"):
            return True
        if v.lower() in ("n", "no"):
            return False
        return d

    @staticmethod
    def menu(t, opts):
        print()
        D.line()
        print(f"    {C.B}{C.P}{t}{C.RS}")
        D.line()
        for n, desc in opts:
            print(f"    {C.LP}  [{C.CY}{n}{C.LP}]{C.W}  {desc}{C.RS}")
        D.line()
        return D.ask("Select option")


def pause():
    print()
    D.ask("Press ENTER to continue")


# ===========================================================================
#  CONNECTION CHECKER
# ===========================================================================

class ConnectionChecker:
    """Verify target is alive and service is reachable before any operation."""

    @staticmethod
    def resolve_target(target):
        """Clean target string and resolve to IP."""
        t = target.strip()
        t = t.replace("http://", "").replace("https://", "")
        t = t.replace("ftp://", "").replace("ssh://", "")
        t = t.split("/")[0].split(":")[0]
        try:
            ip = socket.gethostbyname(t)
            return t, ip, True
        except socket.gaierror:
            return t, None, False

    @staticmethod
    def check_port(host, port, timeout=5):
        """Check if a specific port is actually open and reachable."""
        try:
            ip = socket.gethostbyname(host)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    @staticmethod
    def check_host_alive(host, timeout=3):
        """Check if host is reachable by trying multiple ports."""
        try:
            ip = socket.gethostbyname(host)
        except Exception:
            return False, "Cannot resolve hostname"

        check_ports = [80, 443, 22, 21, 445, 3389, 8080, 3306]
        for port in check_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    return True, f"Responding on port {port}"
            except Exception:
                continue
        return False, "Host is down or all ports filtered"

    @staticmethod
    def check_ftp(host, port, timeout=5):
        """Verify FTP service is actually running."""
        try:
            f = ftplib.FTP()
            f.connect(host, port, timeout=timeout)
            banner = f.getwelcome()
            f.quit()
            return True, banner
        except ftplib.error_reply as e:
            return False, f"Invalid FTP response: {e}"
        except socket.timeout:
            return False, "Connection timed out"
        except ConnectionRefusedError:
            return False, "Connection refused"
        except ConnectionResetError:
            return False, "Connection reset"
        except OSError as e:
            return False, f"Network error: {e}"
        except Exception as e:
            return False, f"Error: {e}"

    @staticmethod
    def check_ssh(host, port, timeout=5):
        """Verify SSH service is actually running."""
        if not HAS_PARAMIKO:
            return False, "paramiko not installed"
        try:
            transport = paramiko.Transport((host, port))
            transport.connect(timeout=timeout)
            banner = transport.remote_version
            transport.close()
            return True, banner
        except paramiko.ssh_exception.SSHException as e:
            return False, f"SSH error: {e}"
        except socket.timeout:
            return False, "Connection timed out"
        except ConnectionRefusedError:
            return False, "Connection refused"
        except Exception as e:
            return False, f"Error: {e}"

    @staticmethod
    def check_http(host, port, timeout=5):
        """Verify HTTP service is actually running."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            ip = socket.gethostbyname(host)
            sock.connect((ip, port))

            req = (f"GET / HTTP/1.1\r\nHost: {host}\r\n"
                   f"User-Agent: WorksTool/3.1\r\nConnection: close\r\n\r\n")
            sock.send(req.encode())
            response = sock.recv(4096).decode("utf-8", errors="replace")
            sock.close()

            if response.startswith("HTTP/"):
                status_line = response.split("\n")[0].strip()
                return True, status_line
            return False, "Not HTTP"
        except socket.timeout:
            return False, "Connection timed out"
        except ConnectionRefusedError:
            return False, "Connection refused"
        except Exception as e:
            return False, f"Error: {e}"

    @staticmethod
    def check_ssl(host, port, timeout=5):
        """Verify HTTPS/SSL service is actually running."""
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            ip = socket.gethostbyname(host)
            ssock = ctx.wrap_socket(sock, server_hostname=host)
            ssock.connect((ip, port))
            req = (f"GET / HTTP/1.1\r\nHost: {host}\r\n"
                   f"User-Agent: WorksTool/3.1\r\nConnection: close\r\n\r\n")
            ssock.send(req.encode())
            response = ssock.recv(4096).decode("utf-8", errors="replace")
            ssock.close()
            if response.startswith("HTTP/"):
                return True, response.split("\n")[0].strip()
            return False, "Not HTTP over SSL"
        except socket.timeout:
            return False, "Connection timed out"
        except ConnectionRefusedError:
            return False, "Connection refused"
        except Exception as e:
            return False, f"Error: {e}"


# ===========================================================================
#  MODULE 1: PORT SCANNER (FIXED)
# ===========================================================================

class AutoScanner:

    def __init__(self, target):
        self.target = target.strip()
        self.target_ip = None
        self.open_ports = {}
        self.closed = 0
        self.filtered = 0
        self.lock = threading.Lock()
        self.host_alive = False
        self.alive_reason = ""

    def _resolve(self):
        t, ip, ok = ConnectionChecker.resolve_target(self.target)
        self.target = t
        self.target_ip = ip
        return ok

    def _scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            r = s.connect_ex((self.target_ip, port))
            if r == 0:
                banner = ""
                service = SERVICE_NAMES.get(port, "unknown")
                try:
                    if port in (443, 8443, 993, 995, 465):
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        ss = ctx.wrap_socket(s, server_hostname=self.target)
                        ss.send(SERVICE_PROBES.get(port, b"\r\n"))
                        banner = ss.recv(1024).decode("utf-8", errors="replace").strip()
                    else:
                        s.send(SERVICE_PROBES.get(port, b"\r\n"))
                        banner = s.recv(1024).decode("utf-8", errors="replace").strip()
                except Exception:
                    pass
                detected = self._id_service(banner, port)
                if detected:
                    service = detected
                version = self._extract_version(banner)
                with self.lock:
                    self.open_ports[port] = {
                        "service": service,
                        "version": version,
                        "banner": banner[:200] if banner else "",
                    }
            else:
                with self.lock:
                    self.closed += 1
            s.close()
        except socket.timeout:
            with self.lock:
                self.filtered += 1
        except OSError:
            with self.lock:
                self.closed += 1

    def _id_service(self, b, port):
        if not b:
            return None
        bl = b.lower()
        sigs = {
            "openssh": "ssh", "ssh-": "ssh", "dropbear": "ssh",
            "apache": "http", "nginx": "http", "iis": "http",
            "http/1": "http", "http/2": "http", "lighttpd": "http",
            "mysql": "mysql", "mariadb": "mysql",
            "postgresql": "postgresql", "+pong": "redis",
            "redis": "redis", "mongodb": "mongodb",
            "vnc": "vnc", "rfb": "vnc",
            "smtp": "smtp", "220-": "ftp" if port == 21 else "smtp",
            "imap": "imap", "pop3": "pop3", "+ok": "pop3",
            "ftp": "ftp", "vsftp": "ftp", "proftp": "ftp",
            "tomcat": "http", "jetty": "http", "gunicorn": "http",
            "elastic": "elasticsearch",
        }
        for sig, svc in sigs.items():
            if sig in bl:
                return svc
        return None

    def _extract_version(self, banner):
        if not banner:
            return ""
        patterns = [
            r"(OpenSSH[_\s][\d\.]+\w*)",
            r"(Apache/[\d\.]+)",
            r"(nginx/[\d\.]+)",
            r"(vsFTPd\s+[\d\.]+)",
            r"(ProFTPD\s+[\d\.]+)",
            r"([\d\.]+[-\w]*ubuntu[\w.-]*)",
            r"([\d\.]+[-\w]*deb[\w.-]*)",
            r"(MySQL\s+[\d\.]+)",
            r"(MariaDB[\s-]+[\d\.]+)",
            r"(PostgreSQL\s+[\d\.]+)",
            r"(Redis[\s:v]+[\d\.]+)",
            r"(Tomcat/[\d\.]+)",
            r"(IIS/[\d\.]+)",
            r"(SSH-2\.0-[\w\d\._-]+)",
            r"(Microsoft[\s-]+[\w\d\.]+)",
        ]
        for p in patterns:
            m = re.search(p, banner, re.IGNORECASE)
            if m:
                return m.group(1)
        return banner[:60].split("\n")[0].strip()

    def _detect_os(self):
        if not self.open_ports:
            return "Unknown"
        try:
            port = list(self.open_ports.keys())[0]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((self.target_ip, port))
            ttl = s.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
            s.close()

            os_hints = []
            for p, info in self.open_ports.items():
                bl = (info.get("banner", "") + info.get("version", "")).lower()
                if "ubuntu" in bl or "debian" in bl:
                    os_hints.append("Ubuntu/Debian Linux")
                elif "centos" in bl or "rhel" in bl:
                    os_hints.append("CentOS/RHEL Linux")
                elif "windows" in bl or "microsoft" in bl or "iis" in bl:
                    os_hints.append("Windows Server")
                elif "freebsd" in bl:
                    os_hints.append("FreeBSD")

            if os_hints:
                return f"{os_hints[0]} (TTL: {ttl})"
            if ttl <= 64:
                return f"Linux/Unix (TTL: {ttl})"
            elif ttl <= 128:
                return f"Windows (TTL: {ttl})"
            return f"Network Device (TTL: {ttl})"
        except Exception:
            return "Unknown"

    def scan(self):
        D.section("FULL AUTO SCAN")

        # Step 1: Resolve
        if not self._resolve():
            D.err(f"Cannot resolve hostname: {self.target}")
            D.info("Check the target address and try again")
            D.line()
            return

        D.info(f"Target: {self.target}")
        D.info(f"IP: {self.target_ip}")
        D.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Step 2: Check if host is alive
        D.info("Phase 0: Checking if host is alive...")
        self.host_alive, self.alive_reason = ConnectionChecker.check_host_alive(
            self.target, timeout=5)

        if not self.host_alive:
            D.err(f"Target is not reachable: {self.alive_reason}")
            D.err(f"Host {self.target} ({self.target_ip}) appears to be DOWN")
            D.info("Possible reasons:")
            D.info("  - Target does not exist")
            D.info("  - Firewall blocking all connections")
            D.info("  - Host is offline")
            D.info("  - Network routing issue")
            D.line()
            return

        D.ok(f"Host is alive: {self.alive_reason}")
        D.line()

        # Step 3: Scan common ports
        D.info("Phase 1: Scanning common ports...")
        total = len(COMMON_PORTS)
        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as ex:
            futs = {ex.submit(self._scan_port, p): p for p in COMMON_PORTS}
            done = 0
            for f in concurrent.futures.as_completed(futs):
                done += 1
                if done % max(1, total // 10) == 0 or done == total:
                    D.progress(done, total, "Common Ports")

        # Step 4: Extended scan 1-1024
        D.info("Phase 2: Scanning ports 1-1024...")
        extended = [p for p in range(1, 1025) if p not in COMMON_PORTS]
        total2 = len(extended)
        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as ex:
            futs = {ex.submit(self._scan_port, p): p for p in extended}
            done = 0
            for f in concurrent.futures.as_completed(futs):
                done += 1
                if done % max(1, total2 // 10) == 0 or done == total2:
                    D.progress(done, total2, "Extended   ")

        # Step 5: High ports
        D.info("Phase 3: Scanning high ports...")
        high_ports = [
            1080, 1433, 1434, 1521, 2049, 2082, 2083, 2181,
            3000, 3128, 3306, 3389, 4443, 5000, 5432, 5555,
            5672, 5900, 5984, 6379, 6667, 7070, 8000, 8008,
            8009, 8080, 8081, 8443, 8888, 9000, 9090, 9200,
            9418, 9999, 10000, 11211, 27017, 27018, 28017, 50000,
        ]
        high_ports = [p for p in high_ports if p > 1024 and p not in COMMON_PORTS]
        total3 = len(high_ports)
        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as ex:
            futs = {ex.submit(self._scan_port, p): p for p in high_ports}
            done = 0
            for f in concurrent.futures.as_completed(futs):
                done += 1
                if done % max(1, total3 // 5) == 0 or done == total3:
                    D.progress(done, total3, "High Ports ")

        # Step 6: OS Detection
        D.info("Phase 4: OS Detection...")
        os_guess = self._detect_os()

        # ---- RESULTS ----
        print()
        D.section("SCAN RESULTS")
        D.info(f"Target: {self.target} ({self.target_ip})")
        D.info(f"OS Guess: {os_guess}")
        D.line()
        print()

        if self.open_ports:
            cols = ["PORT", "STATE", "SERVICE", "VERSION/BANNER"]
            ws = [10, 10, 16, 42]
            D.th(cols, ws)
            for port in sorted(self.open_ports):
                i = self.open_ports[port]
                v = i["version"] if i["version"] else i["banner"][:40]
                D.tr([f"{port}/tcp", "open", i["service"], v], ws)

            print()
            D.line()
            D.info("Detailed Banners:")
            D.line()
            for port in sorted(self.open_ports):
                i = self.open_ports[port]
                if i["banner"]:
                    print(f"    {C.GR}Port {port} ({i['service']}):{C.RS}")
                    for line in i["banner"].split("\n")[:6]:
                        line = line.strip()
                        if line:
                            print(f"    {C.G}  | {C.LP}{line}{C.RS}")
                    print()
        else:
            D.warn("No open ports found on this target")

        print()
        D.info(f"Open: {len(self.open_ports)}  "
               f"Closed: {self.closed}  Filtered: {self.filtered}")
        D.info(f"Total scanned: {len(self.open_ports) + self.closed + self.filtered} ports")
        D.line()
        return self.open_ports


# ===========================================================================
#  MODULE 2: BANNER GRABBER (FIXED)
# ===========================================================================

class BannerGrabber:

    @staticmethod
    def grab():
        D.section("BANNER GRABBER")

        target = D.ask("Enter target IP or URL")
        ports = D.ask("Enter ports (comma separated)", "21,22,80,443,3306,8080")

        if not target:
            D.err("No target provided")
            return

        t, ip, ok = ConnectionChecker.resolve_target(target)
        if not ok:
            D.err(f"Cannot resolve: {t}")
            D.info("Check the target address and try again")
            D.line()
            return

        # Check if host is alive
        D.info(f"Target: {t} ({ip})")
        D.info("Checking if host is reachable...")
        alive, reason = ConnectionChecker.check_host_alive(t, timeout=5)

        if not alive:
            D.err(f"Host is not reachable: {reason}")
            D.line()
            return

        D.ok(f"Host is reachable: {reason}")

        port_list = []
        for part in ports.split(","):
            part = part.strip()
            if "-" in part:
                s, e = part.split("-", 1)
                port_list.extend(range(int(s), int(e) + 1))
            else:
                port_list.append(int(part))

        D.info(f"Checking {len(port_list)} ports...")
        D.line()

        open_ports = []
        for port in port_list:
            # First verify port is open
            if not ConnectionChecker.check_port(t, port, timeout=3):
                D.warn(f"Port {port}: CLOSED or FILTERED")
                continue

            # Then grab banner
            banner = ""
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((ip, port))

                if port in (443, 8443, 993, 995, 465):
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    sock = ctx.wrap_socket(sock, server_hostname=t)

                sock.send(SERVICE_PROBES.get(port, b"\r\n"))
                banner = sock.recv(2048).decode("utf-8", errors="replace").strip()
                sock.close()
            except Exception as e:
                banner = f"[Could not grab banner: {e}]"

            svc = SERVICE_NAMES.get(port, "unknown")
            open_ports.append(port)

            print(f"    {C.GR}Port {port} ({svc}):{C.RS}")
            if banner:
                for line in banner.split("\n")[:8]:
                    line = line.strip()
                    if line:
                        print(f"    {C.G}  | {C.LP}{line}{C.RS}")
            else:
                print(f"    {C.G}  | {C.LP}(no banner){C.RS}")
            print()

        D.line()
        D.info(f"Open ports: {len(open_ports)}/{len(port_list)}")
        D.info(f"Closed/filtered: {len(port_list) - len(open_ports)}/{len(port_list)}")
        D.line()


# ===========================================================================
#  MODULE 3: HASH CRACKER (FIXED)
# ===========================================================================

class HashEngine:

    PATTERNS = [
        (r"^[a-f0-9]{32}$", ["md5", "ntlm"]),
        (r"^[a-f0-9]{40}$", ["sha1"]),
        (r"^[a-f0-9]{56}$", ["sha224"]),
        (r"^[a-f0-9]{64}$", ["sha256"]),
        (r"^[a-f0-9]{96}$", ["sha384"]),
        (r"^[a-f0-9]{128}$", ["sha512"]),
        (r"^[a-f0-9]{16}$", ["mysql323", "half-md5"]),
        (r"^\$1\$", ["md5crypt"]),
        (r"^\$2[aby]?\$", ["bcrypt"]),
        (r"^\$5\$", ["sha256crypt"]),
        (r"^\$6\$", ["sha512crypt"]),
        (r"^\$apr1\$", ["apr1"]),
        (r"^\$P\$", ["phpass"]),
        (r"^\$H\$", ["phpass"]),
    ]

    DISPLAY_NAMES = {
        "md5": "MD5", "ntlm": "NTLM", "sha1": "SHA-1",
        "sha224": "SHA-224", "sha256": "SHA-256",
        "sha384": "SHA-384", "sha512": "SHA-512",
        "mysql323": "MySQL 3.2.3", "half-md5": "Half MD5",
        "md5crypt": "MD5crypt", "bcrypt": "bcrypt",
        "sha256crypt": "SHA-256crypt", "sha512crypt": "SHA-512crypt",
        "apr1": "Apache APR1", "phpass": "PHPass",
    }

    def __init__(self, hash_val, custom_wordlist=None):
        self.hash_val = hash_val.strip()
        self.hash_lower = hash_val.strip().lower()
        self.custom_wordlist = custom_wordlist
        self.found = False
        self.result = None
        self.attempts = 0
        self.lock = threading.Lock()

    def _detect_types(self):
        types = []
        for pat, t_list in self.PATTERNS:
            if re.match(pat, self.hash_lower):
                types.extend(t_list)
        return types if types else ["unknown"]

    def _compute(self, pw, htype):
        try:
            if htype == "md5":
                return hashlib.md5(pw.encode()).hexdigest()
            elif htype == "sha1":
                return hashlib.sha1(pw.encode()).hexdigest()
            elif htype == "sha224":
                return hashlib.sha224(pw.encode()).hexdigest()
            elif htype == "sha256":
                return hashlib.sha256(pw.encode()).hexdigest()
            elif htype == "sha384":
                return hashlib.sha384(pw.encode()).hexdigest()
            elif htype == "sha512":
                return hashlib.sha512(pw.encode()).hexdigest()
            elif htype == "ntlm":
                return binascii.hexlify(
                    hashlib.new("md4", pw.encode("utf-16le")).digest()
                ).decode()
            elif htype == "mysql323":
                nr = 1345345333
                add = 7
                nr2 = 0x12345671
                for c in pw:
                    if c in (' ', '\t'):
                        continue
                    tmp = ord(c)
                    nr ^= (((nr & 63) + add) * tmp) + (nr << 8)
                    nr &= 0x7FFFFFFF
                    nr2 += (nr2 << 8) ^ nr
                    nr2 &= 0x7FFFFFFF
                    add += tmp
                return f"{nr:08x}{nr2:08x}"
        except Exception:
            pass
        return ""

    def _generate_mutations(self, word):
        v = {word}
        v.add(word.capitalize())
        v.add(word.upper())
        v.add(word.lower())
        v.add(word[::-1])
        for i in range(10):
            v.add(word + str(i))
        for s in ["!", "@", "#", "123", "1234", "2024", "2025",
                   "1!", "@123", "01"]:
            v.add(word + s)
            v.add(word.capitalize() + s)
        leet = word.replace("a", "@").replace("e", "3").replace(
            "i", "1").replace("o", "0").replace("s", "$")
        v.add(leet)
        v.add(leet.capitalize())
        return list(v)

    def _try_word(self, pw, htype):
        if self.found:
            return
        computed = self._compute(pw, htype)
        with self.lock:
            self.attempts += 1
        if computed == self.hash_lower:
            with self.lock:
                self.found = True
                self.result = pw

    def _check_base64(self):
        try:
            decoded = base64.b64decode(self.hash_val).decode("utf-8")
            if decoded.isprintable() and len(decoded) > 1:
                return decoded
        except Exception:
            pass
        return None

    def _check_hex(self):
        try:
            decoded = bytes.fromhex(self.hash_val).decode("utf-8")
            if decoded.isprintable() and len(decoded) > 1:
                return decoded
        except Exception:
            pass
        return None

    def crack(self):
        D.section("HASH CRACKER")
        D.info(f"Hash: {self.hash_val}")
        D.info(f"Length: {len(self.hash_val)}")
        D.line()

        # Step 1: Detect
        D.info("Step 1: Identifying hash type...")
        hash_types = self._detect_types()
        for ht in hash_types:
            name = self.DISPLAY_NAMES.get(ht, ht.upper())
            D.res(f"Possible type: {name}")
        print()

        # Step 2: Check encodings
        D.info("Step 2: Checking for simple encoding...")
        b64 = self._check_base64()
        if b64:
            D.ok(f"Base64 decoded text: {b64}")
        hx = self._check_hex()
        if hx:
            D.ok(f"Hex decoded text: {hx}")
        if not b64 and not hx:
            D.info("Not a simple base64 or hex encoding")
        print()

        # Step 3: Check unsupported
        unsupported = ["bcrypt", "md5crypt", "sha256crypt",
                       "sha512crypt", "apr1", "phpass", "unknown"]
        active = [t for t in hash_types if t not in unsupported]
        skipped = [t for t in hash_types if t in unsupported]

        if skipped:
            for st in skipped:
                name = self.DISPLAY_NAMES.get(st, st)
                D.warn(f"Skipping {name} (needs hashcat or john)")

        if not active:
            D.err("No crackable hash types detected")
            D.info("Use hashcat or john for specialized hash types")
            D.line()
            return

        # Step 4: Dictionary attack
        D.info("Step 3: Dictionary attack...")
        start = time.time()

        words = list(BUILTIN_PASSWORDS)
        if self.custom_wordlist and os.path.isfile(self.custom_wordlist):
            D.info(f"Loading: {self.custom_wordlist}")
            with open(self.custom_wordlist, "r", errors="replace") as f:
                custom = [l.strip() for l in f if l.strip()]
            D.info(f"Custom words: {len(custom):,}")
            words.extend(custom)

        all_candidates = []
        for w in words:
            all_candidates.extend(self._generate_mutations(w))
        all_candidates = list(set(all_candidates))
        D.info(f"Total candidates: {len(all_candidates):,}")

        for htype in active:
            if self.found:
                break
            name = self.DISPLAY_NAMES.get(htype, htype)
            D.info(f"Trying as {name}...")

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
                for i, pw in enumerate(all_candidates):
                    if self.found:
                        break
                    ex.submit(self._try_word, pw, htype)

            time.sleep(0.1)

        elapsed = time.time() - start

        # Step 5: Quick brute force if not found
        if not self.found and not self.custom_wordlist:
            print()
            D.info("Step 4: Quick brute force (1-4 chars)...")
            chars = string.ascii_lowercase + string.digits
            for htype in active:
                if self.found:
                    break
                for length in range(1, 5):
                    if self.found:
                        break
                    with concurrent.futures.ThreadPoolExecutor(
                            max_workers=8) as ex:
                        for combo in itertools.product(chars, repeat=length):
                            if self.found:
                                break
                            ex.submit(self._try_word,
                                      "".join(combo), htype)
            elapsed = time.time() - start

        print()
        D.line()

        if self.found:
            D.ok("CRACKED!")
            D.res(f"Hash:     {self.hash_val}")
            D.res(f"Plaintext: {self.result}")
            for ht in active:
                if self._compute(self.result, ht) == self.hash_lower:
                    D.res(f"Hash Type: {self.DISPLAY_NAMES.get(ht, ht)}")
                    break
        else:
            D.warn("Hash not cracked with current wordlist")
            if not self.custom_wordlist:
                D.info("Tip: Add a custom wordlist (rockyou.txt)")
            D.info("Recommended: rockyou.txt, SecLists, CrackStation")
        print()
        D.info(f"Attempts: {self.attempts:,}")
        D.info(f"Speed: {self.attempts / max(elapsed, 0.001):,.0f} H/s")
        D.info(f"Time: {elapsed:.2f}s")
        D.line()
        return self.result


# ===========================================================================
#  MODULE 4: BRUTE FORCER (COMPLETELY FIXED)
# ===========================================================================

class BruteForcer:

    def __init__(self):
        self.target = ""
        self.target_ip = ""
        self.service = ""
        self.port = 0
        self.creds = []
        self.attempts = 0
        self.lock = threading.Lock()
        self.stopped = False
        self.connection_verified = False
        self.connection_info = ""

    def _try_ssh(self, u, p):
        if self.stopped:
            return False
        if not HAS_PARAMIKO:
            return False
        try:
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(self.target_ip, port=self.port, username=u,
                      password=p, timeout=8, allow_agent=False,
                      look_for_keys=False)
            c.close()
            return True
        except paramiko.AuthenticationException:
            return False
        except paramiko.ssh_exception.NoValidConnectionsError:
            self.stopped = True
            return False
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.timeout:
            return False
        except ConnectionRefusedError:
            self.stopped = True
            return False
        except Exception:
            return False

    def _try_ftp(self, u, p):
        if self.stopped:
            return False
        try:
            f = ftplib.FTP()
            f.connect(self.target_ip, self.port, timeout=8)
            f.login(u, p)
            f.quit()
            return True
        except ftplib.error_perm:
            return False
        except (socket.timeout, ConnectionRefusedError,
                ConnectionResetError, OSError):
            self.stopped = True
            return False
        except Exception:
            return False

    def _try_http(self, u, p):
        if self.stopped:
            return False
        try:
            cr = base64.b64encode(f"{u}:{p}".encode()).decode()
            if HAS_REQUESTS:
                r = requests.get(
                    f"http://{self.target_ip}:{self.port}{self.http_path}",
                    headers={"Authorization": f"Basic {cr}"},
                    timeout=10, allow_redirects=False)
                if r.status_code == 0:
                    self.stopped = True
                    return False
                return r.status_code != 401
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(8)
                s.connect((self.target_ip, self.port))
                req = (f"GET {self.http_path} HTTP/1.1\r\n"
                       f"Host: {self.target}\r\n"
                       f"Authorization: Basic {cr}\r\n"
                       f"Connection: close\r\n\r\n")
                s.send(req.encode())
                resp = s.recv(4096).decode("utf-8", errors="replace")
                s.close()
                return "401" not in resp.split("\n")[0]
        except (socket.timeout, ConnectionRefusedError, OSError):
            self.stopped = True
            return False
        except Exception:
            return False

    def _try_http_form(self, u, p):
        if self.stopped:
            return False
        if not HAS_REQUESTS:
            return False
        try:
            fd = {}
            if self.http_form:
                for pair in self.http_form.split("&"):
                    k, v = pair.split("=", 1)
                    fd[k] = v.replace("^USER^", u).replace("^PASS^", p)
            else:
                fd = {"username": u, "password": p}
            url = f"http://{self.target_ip}:{self.port}{self.http_path}"
            r = requests.post(url, data=fd, timeout=10,
                              allow_redirects=True)
            if r.status_code == 0:
                self.stopped = True
                return False
            return self.http_fail.lower() not in r.text.lower()
        except (ConnectionRefusedError, OSError):
            self.stopped = True
            return False
        except Exception:
            return False

    def _try_telnet(self, u, p):
        if self.stopped:
            return False
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(8)
            s.connect((self.target_ip, self.port))
            time.sleep(0.5)
            s.recv(4096)
            s.send(f"{u}\r\n".encode())
            time.sleep(0.5)
            s.recv(4096)
            s.send(f"{p}\r\n".encode())
            time.sleep(1)
            resp = s.recv(4096).decode("utf-8", errors="replace")
            s.close()
            fails = ["incorrect", "invalid", "failed", "denied",
                     "login:", "bad"]
            return not any(f in resp.lower() for f in fails)
        except (socket.timeout, ConnectionRefusedError, OSError):
            self.stopped = True
            return False
        except Exception:
            return False

    def _attempt(self, u, p):
        if self.stopped:
            return
        with self.lock:
            self.attempts += 1
        fn = {"ssh": self._try_ssh, "ftp": self._try_ftp,
              "http": self._try_http, "http-form": self._try_http_form,
              "telnet": self._try_telnet}.get(self.service)
        if fn and fn(u, p):
            with self.lock:
                self.creds.append((u, p))
                D.ok(f"FOUND: {u}:{p}")
                self.stopped = True

    def run(self):
        D.section("BRUTE FORCER")

        # Step 1: Get target
        target = D.ask("Enter target IP or URL")
        if not target:
            D.err("No target provided")
            return

        t, ip, ok = ConnectionChecker.resolve_target(target)
        if not ok:
            D.err(f"Cannot resolve: {t}")
            D.info("Check the target address and try again")
            D.line()
            return

        self.target = t
        self.target_ip = ip

        D.info(f"Target: {t} ({ip})")
        print()

        # Step 2: Select service
        ch = D.menu("SELECT SERVICE", [
            ("1", "SSH (port 22)"),
            ("2", "FTP (port 21)"),
            ("3", "HTTP Basic Auth (port 80)"),
            ("4", "HTTP Form Login (port 80)"),
            ("5", "Telnet (port 23)"),
        ])
        svc_map = {"1": "ssh", "2": "ftp", "3": "http",
                   "4": "http-form", "5": "telnet"}
        self.service = svc_map.get(ch, "ssh")
        def_ports = {"ssh": 22, "ftp": 21, "http": 80,
                     "http-form": 80, "telnet": 23}
        self.port = int(D.ask("Port", str(def_ports.get(self.service, 80))))

        # Step 3: VERIFY SERVICE IS RUNNING
        D.info(f"Verifying {self.service.upper()} service on "
               f"{self.target}:{self.port}...")
        check_fn = {
            "ssh": ConnectionChecker.check_ssh,
            "ftp": ConnectionChecker.check_ftp,
            "http": ConnectionChecker.check_http,
            "http-form": ConnectionChecker.check_http,
            "telnet": lambda h, p, t=5: ConnectionChecker.check_port(h, p, t),
        }.get(self.service)

        if check_fn:
            if self.service == "telnet":
                ok = check_fn(self.target, self.port)
                if not ok:
                    D.err(f"Port {self.port} is CLOSED on {self.target}")
                    D.info("The service is not running on this port")
                    D.line()
                    return
                self.connection_verified = True
                self.connection_info = "Port open"
            else:
                verified, info = check_fn(self.target, self.port, timeout=5)
                if not verified:
                    D.err(f"{self.service.upper()} service is NOT responding:")
                    D.err(f"  {info}")
                    D.info(f"Target {self.target}:{self.port} is not reachable")
                    D.info("Make sure the service is running on this target")
                    D.line()
                    return
                self.connection_verified = True
                self.connection_info = info

        D.ok(f"Service confirmed: {self.connection_info}")
        print()

        # Step 4: Get credentials list
        ch2 = D.menu("USERNAME", [
            ("1", "Single username"),
            ("2", "Username list file"),
            ("3", "Built-in list (35 common usernames)"),
        ])
        users = []
        if ch2 == "1":
            u = D.ask("Enter username")
            if u:
                users = [u]
        elif ch2 == "2":
            uf = D.ask("Username list file path")
            if uf and os.path.isfile(uf):
                with open(uf, "r", errors="replace") as f:
                    users = [l.strip() for l in f if l.strip()]
                D.info(f"Loaded {len(users)} usernames")
            else:
                D.err("File not found, using built-in list")
                users = list(BUILTIN_USERNAMES)
        else:
            users = list(BUILTIN_USERNAMES)

        if not users:
            D.err("No usernames provided")
            return

        add_pw = D.yn("Add custom password list", False)
        passwords = list(BUILTIN_PASSWORDS)
        if add_pw:
            pf = D.ask("Password list file path")
            if pf and os.path.isfile(pf):
                with open(pf, "r", errors="replace") as f:
                    custom_pw = [l.strip() for l in f if l.strip()]
                D.info(f"Loaded {len(custom_pw)} passwords")
                passwords = custom_pw
            else:
                D.err("File not found, using built-in list")

        total = len(users) * len(passwords)
        D.info(f"Users: {len(users)}")
        D.info(f"Passwords: {len(passwords)}")
        D.info(f"Combinations: {total:,}")

        # Double check: verify connection one more time right before attack
        D.info("Final connection check...")
        if self.service == "ssh":
            ok, info = ConnectionChecker.check_ssh(
                self.target, self.port, timeout=5)
        elif self.service == "ftp":
            ok, info = ConnectionChecker.check_ftp(
                self.target, self.port, timeout=5)
        elif self.service in ("http", "http-form"):
            ok, info = ConnectionChecker.check_http(
                self.target, self.port, timeout=5)
        else:
            ok = ConnectionChecker.check_port(
                self.target, self.port, timeout=5)
            info = "port open" if ok else "port closed"

        if not ok:
            D.err(f"Connection failed: {info}")
            D.err("Service may have gone down between checks")
            D.line()
            return

        D.ok(f"Connection verified: {info}")
        D.line()

        self.http_path = "/"
        self.http_form = None
        self.http_fail = "Invalid"
        if self.service == "http-form":
            self.http_path = D.ask("Login page path", "/login")
            print(f"    {C.G}Use ^USER^ and ^PASS^ as placeholders{C.RS}")
            print(f"    {C.G}Example: user=^USER^&pass=^PASS^{C.RS}")
            self.http_form = D.ask("Form data")
            self.http_fail = D.ask("Failure string", "Invalid")
            print()

        # Step 5: Run attack
        D.info(f"Starting attack on {self.service.upper()}...")
        D.line()

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            futs = []
            for u in users:
                for p in passwords:
                    if self.stopped:
                        break
                    futs.append(ex.submit(self._attempt, u, p))
                if self.stopped:
                    break
            done = 0
            for f in concurrent.futures.as_completed(futs):
                done += 1
                if not self.stopped and done % max(1, total // 20) == 0:
                    D.progress(done, total, "Attacking")
                if self.stopped and done >= len(futs):
                    break

        elapsed = time.time() - start
        print()
        D.line()

        if self.creds:
            D.ok(f"Found {len(self.creds)} valid credential(s):")
            D.th(["USERNAME", "PASSWORD"], [30, 30])
            for u, p in self.creds:
                D.tr([u, p], [30, 30])
        else:
            D.warn("No valid credentials found")
            D.info("Try a larger wordlist or different usernames")

        D.info(f"Attempts: {self.attempts:,}")
        D.info(f"Speed: {self.attempts / max(elapsed, 0.001):.0f}/s")
        D.info(f"Time: {elapsed:.2f}s")
        D.line()


# ===========================================================================
#  MODULE 5: WEB FUZZER (FIXED)
# ===========================================================================

class WebFuzzer:

    def __init__(self):
        self.results = []
        self.reqs = 0
        self.errors = 0
        self.lock = threading.Lock()

    def _request(self, url):
        try:
            start = time.time()
            if HAS_REQUESTS:
                h = {"User-Agent": "WorksTool/3.1"}
                r = requests.get(url, headers=h, timeout=10,
                                 allow_redirects=False)
                return r.status_code, len(r.content), time.time() - start
            elif HAS_URLLIB:
                req = urllib.request.Request(url)
                req.add_header("User-Agent", "WorksTool/3.1")
                resp = urllib.request.urlopen(req, timeout=10)
                body = resp.read()
                return resp.status, len(body), time.time() - start
        except Exception:
            with self.lock:
                self.errors += 1
        return None, 0, 0

    def _fuzz_word(self, word, url, extensions, mode):
        targets = []
        if mode == "dir":
            for ext in extensions:
                if ext and not ext.startswith("."):
                    ext = "." + ext
                targets.append((f"{url}/{word}{ext}", f"{word}{ext}"))
        elif mode == "subdomain":
            base = url.replace("http://", "").replace("https://", "")
            targets.append((f"http://{word}.{base}", f"{word}.{base}"))
        elif mode == "param":
            if "FUZZ" in url:
                targets.append((url.replace("FUZZ", word), word))
            else:
                sep = "&" if "?" in url else "?"
                targets.append((f"{url}{sep}id={word}", word))

        for turl, dw in targets:
            code, size, rt = self._request(turl)
            with self.lock:
                self.reqs += 1
            if code is None or code == 404:
                continue
            col = C.GR if code < 300 else C.Y if code < 400 else \
                C.CY if code < 500 else C.R
            with self.lock:
                self.results.append({
                    "url": turl, "word": dw, "code": code,
                    "size": size, "time": rt})
                print(f"    {col}[{code}]{C.W} {dw:<40} "
                      f"{C.G}[Size:{size}] [Time:{rt:.3f}s]{C.RS}")

    def run(self):
        D.section("WEB FUZZER")

        if not HAS_REQUESTS and not HAS_URLLIB:
            D.err("Needs: pip install requests")
            return

        url = D.ask("Enter target URL", "http://127.0.0.1")
        if not url:
            D.err("No URL provided")
            return

        # Verify URL is reachable
        D.info("Checking if target is reachable...")
        try:
            code, _, _ = self._request(url)
            if code is None:
                D.err("Target is not responding")
                D.info("Check if the web server is running")
                D.line()
                return
            D.ok(f"Target responded with status {code}")
        except Exception:
            D.err("Cannot connect to target")
            D.line()
            return

        ch = D.menu("FUZZING MODE", [
            ("1", "Directory / File discovery"),
            ("2", "Subdomain enumeration"),
            ("3", "Parameter fuzzing"),
        ])
        mode = {"1": "dir", "2": "subdomain", "3": "param"}.get(ch, "dir")

        extensions = [""]
        if mode == "dir":
            ext_str = D.ask("Extensions (comma separated)",
                            "php,html,txt,bak")
            extensions = [e.strip() for e in ext_str.split(",")]

        if mode == "param" and "FUZZ" not in url:
            D.warn("URL should contain FUZZ placeholder")
            D.info("Example: http://target.com/page?id=FUZZ")
            url = D.ask("Update URL", url)

        add_wl = D.yn("Add custom wordlist", False)
        custom = None
        if add_wl:
            custom = D.ask("Wordlist file path")

        words = list(BUILTIN_DIRS)
        if custom and os.path.isfile(custom):
            D.info(f"Loading: {custom}")
            with open(custom, "r", errors="replace") as f:
                cw = [l.strip() for l in f if l.strip()
                      and not l.startswith("#")]
            words.extend(cw)
            D.info(f"Custom words: {len(cw)}")
        words = list(set(words))

        D.info(f"Target: {url}")
        D.info(f"Mode: {mode.upper()}")
        D.info(f"Words: {len(words)}")
        if extensions != [""]:
            D.info(f"Extensions: {', '.join(extensions)}")
        D.line()
        print()
        D.th(["STATUS", "PATH", "INFO"], [10, 40, 30])

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as ex:
            list(ex.map(lambda w: self._fuzz_word(w, url, extensions, mode),
                        words))

        elapsed = time.time() - start
        print()
        D.line()
        D.info(f"Requests: {self.reqs:,}")
        D.info(f"Found: {len(self.results)}")
        D.info(f"Errors: {self.errors}")
        D.info(f"Speed: {self.reqs / max(elapsed, 0.001):.0f} req/s")
        D.info(f"Time: {elapsed:.2f}s")
        D.line()


# ===========================================================================
#  MODULE 6: FILE CRACKER (FIXED)
# ===========================================================================

class FileCracker:

    def __init__(self):
        self.found = False
        self.result = None
        self.attempts = 0
        self.lock = threading.Lock()

    def _try_zip(self, filepath, pw):
        if not HAS_ZIPFILE:
            return False
        try:
            with zf.ZipFile(filepath) as z:
                z.extractall(pwd=pw.encode())
            return True
        except RuntimeError as e:
            if "password" in str(e).lower() or "encrypted" in str(e).lower():
                return False
            return False
        except Exception:
            return False

    def _generate_mutations(self, word):
        v = {word, word.capitalize(), word.upper(), word.lower(),
             word[::-1]}
        for i in range(10):
            v.add(word + str(i))
        for s in ["!", "123", "@", "2024", "2025"]:
            v.add(word + s)
            v.add(word.capitalize() + s)
        return list(v)

    def _attempt(self, filepath, pw):
        if self.found:
            return
        with self.lock:
            self.attempts += 1
        if self._try_zip(filepath, pw):
            with self.lock:
                self.found = True
                self.result = pw

    def crack(self):
        D.section("FILE PASSWORD CRACKER")

        filepath = D.ask("Enter file path (ZIP)")
        if not filepath:
            D.err("No file provided")
            return

        if not os.path.isfile(filepath):
            D.err(f"File not found: {filepath}")
            D.info("Check the file path and try again")
            D.line()
            return

        D.info(f"Target: {filepath}")
        D.info(f"Type: ZIP")
        D.line()

        add_wl = D.yn("Add custom wordlist", False)
        words = list(BUILTIN_PASSWORDS)
        if add_wl:
            custom = D.ask("Wordlist file path")
            if custom and os.path.isfile(custom):
                D.info(f"Loading: {custom}")
                with open(custom, "r", errors="replace") as f:
                    cw = [l.strip() for l in f if l.strip()]
                words.extend(cw)
                D.info(f"Custom words: {len(cw)}")

        all_candidates = []
        for w in words:
            all_candidates.extend(self._generate_mutations(w))
        all_candidates = list(set(all_candidates))
        D.info(f"Candidates: {len(all_candidates):,}")

        start = time.time()
        total = len(all_candidates)

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            for i, pw in enumerate(all_candidates):
                if self.found:
                    break
                ex.submit(self._attempt, filepath, pw)
                if (i + 1) % max(1, total // 20) == 0:
                    D.progress(i + 1, total, "Cracking")

        elapsed = time.time() - start
        print()
        D.line()
        if self.found:
            D.ok(f"PASSWORD FOUND: {self.result}")
        else:
            D.warn("Password not found")
            D.info("Try adding a custom wordlist (rockyou.txt)")
        D.info(f"Attempts: {self.attempts:,}")
        D.info(f"Speed: {self.attempts / max(elapsed, 0.001):,.0f}/s")
        D.info(f"Time: {elapsed:.2f}s")
        D.line()


# ===========================================================================
#  MODULE 7: NETWORK UTILITIES
# ===========================================================================

class NetUtils:

    @staticmethod
    def sweep():
        D.section("NETWORK SWEEP")
        network = D.ask("Enter network CIDR", "192.168.1.0/24")
        if not network:
            D.err("No network provided")
            return
        try:
            net = ipaddress.ip_network(network, strict=False)
        except ValueError:
            D.err(f"Invalid CIDR: {network}")
            return
        hosts = list(net.hosts())
        if len(hosts) > 1024:
            D.warn(f"Large network ({len(hosts)} hosts) -- may take long")
        D.info(f"Network: {network}")
        D.info(f"Hosts: {len(hosts)}")
        D.line()
        live = []
        lock = threading.Lock()

        def check(ip):
            ip_s = str(ip)
            for p in (80, 443, 22, 21, 8080, 3389, 445):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    if s.connect_ex((ip_s, p)) == 0:
                        with lock:
                            live.append(ip_s)
                            D.ok(f"Host up: {ip_s} (port {p})")
                        s.close()
                        return
                    s.close()
                except Exception:
                    pass

        with concurrent.futures.ThreadPoolExecutor(max_workers=150) as ex:
            ex.map(check, hosts)
        D.line()
        D.info(f"Live hosts: {len(live)}/{len(hosts)}")
        if len(live) == 0:
            D.warn("No live hosts found on this network")
        D.line()

    @staticmethod
    def dns():
        D.section("DNS LOOKUP")
        target = D.ask("Enter domain")
        if not target:
            D.err("No domain provided")
            return
        D.info(f"Target: {target}")
        D.line()
        found_any = False
        try:
            ip = socket.gethostbyname(target)
            D.res(f"A Record: {ip}")
            found_any = True
        except socket.gaierror:
            D.err("Cannot resolve A record -- domain does not exist")
            D.line()
            return
        try:
            fqdn = socket.getfqdn(target)
            if fqdn and fqdn != target:
                D.res(f"FQDN: {fqdn}")
        except Exception:
            pass
        try:
            hn, al, ad = socket.gethostbyname_ex(target)
            D.res(f"Hostname: {hn}")
            for a in al:
                D.res(f"Alias: {a}")
            for a in ad:
                D.res(f"Address: {a}")
        except Exception:
            pass
        try:
            rev = socket.gethostbyaddr(ip)
            D.res(f"Reverse DNS: {rev[0]}")
        except Exception:
            pass
        D.line()

    @staticmethod
    def whois():
        D.section("WHOIS LOOKUP")
        target = D.ask("Enter domain")
        if not target:
            D.err("No domain provided")
            return
        D.info(f"Target: {target}")
        D.line()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect(("whois.iana.org", 43))
            s.send(f"{target}\r\n".encode())
            resp = b""
            while True:
                d = s.recv(4096)
                if not d:
                    break
                resp += d
            s.close()
            found = False
            for line in resp.decode("utf-8", errors="replace").split("\n"):
                line = line.strip()
                if line and not line.startswith("%"):
                    D.res(line)
                    found = True
            if not found:
                D.warn("No WHOIS data returned")
        except socket.timeout:
            D.err("WHOIS connection timed out")
        except ConnectionRefusedError:
            D.err("WHOIS server refused connection")
        except Exception as e:
            D.err(f"WHOIS failed: {e}")
        D.line()


# ===========================================================================
#  INTERACTIVE MENU
# ===========================================================================

def opt_scan():
    print()
    target = D.ask("Enter target IP or URL")
    if not target:
        D.err("No target provided")
        pause()
        return
    scanner = AutoScanner(target)
    scanner.scan()
    pause()


def opt_banner():
    BannerGrabber.grab()
    pause()


def opt_hash():
    print()
    hash_val = D.ask("Enter hash to crack")
    if not hash_val:
        D.err("No hash provided")
        pause()
        return
    add_wl = D.yn("Add custom wordlist", False)
    custom = None
    if add_wl:
        custom = D.ask("Wordlist file path")
    engine = HashEngine(hash_val, custom)
    engine.crack()
    pause()


def opt_brute():
    bf = BruteForcer()
    bf.run()
    pause()


def opt_fuzz():
    fuzzer = WebFuzzer()
    fuzzer.run()
    pause()


def opt_crack():
    fc = FileCracker()
    fc.crack()
    pause()


def opt_sweep():
    NetUtils.sweep()
    pause()


def opt_dns():
    NetUtils.dns()
    pause()


def opt_whois():
    NetUtils.whois()
    pause()


def opt_deps():
    D.section("DEPENDENCY CHECK")
    print()
    deps = [
        ("paramiko", HAS_PARAMIKO, "SSH brute force"),
        ("requests", HAS_REQUESTS, "HTTP fuzzing / brute force"),
        ("zipfile", HAS_ZIPFILE, "ZIP file cracking"),
        ("urllib", HAS_URLLIB, "Basic HTTP requests"),
    ]
    D.th(["MODULE", "STATUS", "USED FOR"], [20, 15, 35])
    for name, ok, use in deps:
        st = "Installed" if ok else "MISSING"
        D.tr([name, st, use], [20, 15, 35])
    print()
    if not HAS_PARAMIKO:
        D.warn("pip install paramiko")
    if not HAS_REQUESTS:
        D.warn("pip install requests")
    D.line()
    pause()


# ===========================================================================
#  MAIN LOOP
# ===========================================================================

def main():
    signal.signal(signal.SIGINT, lambda s, f: (
        print(f"\n\n    {C.R}[!] Interrupted.{C.RS}\n"),
        os._exit(0)))

    while True:
        D.clear()
        D.banner()
        print(f"    {C.G}Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"    Platform: {platform.system()} "
              f"{platform.release()}{C.RS}")

        ch = D.menu("MAIN MENU", [
            ("1",  "Full Auto Scan"),
            ("2",  "Banner Grabber"),
            ("3",  "Hash Cracker"),
            ("4",  "Brute Forcer (SSH/FTP/HTTP)"),
            ("5",  "Web Fuzzer"),
            ("6",  "File Password Cracker (ZIP)"),
            ("7",  "Network Sweep"),
            ("8",  "DNS Lookup"),
            ("9",  "WHOIS Lookup"),
            ("10", "Check Dependencies"),
            ("0",  "Exit"),
        ])

        actions = {
            "1": opt_scan, "2": opt_banner, "3": opt_hash,
            "4": opt_brute, "5": opt_fuzz, "6": opt_crack,
            "7": opt_sweep, "8": opt_dns, "9": opt_whois,
            "10": opt_deps,
        }

        if ch == "0":
            D.clear()
            D.banner()
            D.info("Thank you for using Work's Tool")
            D.info("For authorized security testing only")
            D.line()
            print()
            sys.exit(0)
        elif ch in actions:
            actions[ch]()
        else:
            D.err("Invalid option")
            time.sleep(1)


if __name__ == "__main__":
    main()