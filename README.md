# Work's Tool v3.1

**Professional Cybersecurity Assessment Framework**

A Python-based command-line penetration testing toolkit with 10 integrated security modules.
text

+==================================================================+
|                                                                  |
|   ##      ## ####### ######  ##   ## #######                    |
|   ##  ##  ## ##   ## ##   ## ## ##  ##                            |
|   ## #### ## ##   ## ######  ####   #######                      |
|   ## #### ## ##   ## ##  ##  ## ##       ##                      |
|    ##  ##   ####### ##   ## ##   ## #######                      |
|                                                                  |
|              ######## ####### ####### ##                          |
|                 ##    ##   ## ##   ## ##                          |
|                 ##    ##   ## ##   ## ##                          |
|                 ##    ##   ## ##   ## ##                          |
|                 ##    ####### ####### #######                     |
|                                                                  |
|  Professional Cybersecurity Assessment Framework       v3.1      |
|  For Authorized Security Testing Only                            |
+==================================================================+
text


---

## About

Work's Tool combines the functionality of Nmap, Hashcat, John the Ripper, Hydra, and ffuf into a single Python script with an interactive menu. No complex commands needed. Just run it, pick a number, enter the target.

| Module | What It Does | Similar To |
|--------|-------------|------------|
| Full Auto Scan | Port scan + service detection + OS fingerprint | Nmap |
| Banner Grabber | Grab service banners from open ports | Nmap -sV |
| Hash Cracker | Crack hashes with dictionary + brute force | Hashcat / John |
| Brute Forcer | Attack SSH, FTP, HTTP, Telnet services | Hydra |
| Web Fuzzer | Discover directories, subdomains, parameters | ffuf / dirb |
| File Cracker | Crack password-protected ZIP files | fcrackzip |
| Network Sweep | Find live hosts on a network | Nmap -sn |
| DNS Lookup | DNS records and reverse lookup | dig / nslookup |
| WHOIS Lookup | Domain registration information | whois |
| Dependency Check | Verify installed libraries | - |

---

## Installation

```bash
# Step 1: Clone
git clone https://github.com/yourusername/workstool.git
cd workstool

# Step 2: Install dependencies
pip install paramiko requests

# Step 3: Run
python workstool.py
One-liner (Linux/macOS):

Bash

git clone https://github.com/yourusername/workstool.git && cd workstool && pip install paramiko requests && python3 workstool.py
One-liner (Windows):

cmd

git clone https://github.com/yourusername/workstool.git && cd workstool && pip install paramiko requests && python workstool.py
Requirements
Python 3.7+
paramiko (for SSH brute force) - pip install paramiko
requests (for HTTP fuzzing/brute force) - pip install requests
colorama (optional, for older Windows) - pip install colorama
How to Run
Bash

python workstool.py        # Windows
python3 workstool.py       # Linux / macOS
You will see:

text

    ==================================================================
    MAIN MENU
    ==================================================================
      [1]  Full Auto Scan
      [2]  Banner Grabber
      [3]  Hash Cracker
      [4]  Brute Forcer (SSH/FTP/HTTP)
      [5]  Web Fuzzer
      [6]  File Password Cracker (ZIP)
      [7]  Network Sweep
      [8]  DNS Lookup
      [9]  WHOIS Lookup
      [10] Check Dependencies
      [0]  Exit
    ==================================================================
    [?] Select option: _
Type a number. Press ENTER. Follow the prompts. Press ENTER after results to go back.

Module 1 - Full Auto Scan
Just enter the target. It scans everything automatically.

text

[?] Select option: 1
[?] Enter target IP or URL: 192.168.1.1
Output when target is UP:

text

    +==================================================================+
    |  FULL AUTO SCAN                                                  |
    +==================================================================+
    [*] Target: 192.168.1.1
    [*] IP: 192.168.1.1
    [*] Started: 2025-01-15 14:30:05
    [*] Phase 0: Checking if host is alive...
    [+] Host is alive: Responding on port 22
    ==================================================================
    [*] Phase 1: Scanning common ports...
    [*] Common Ports: [########################################] 100.00%
    [*] Phase 2: Scanning ports 1-1024...
    [*] Extended   : [########################################] 100.00%
    [*] Phase 3: Scanning high ports...
    [*] High Ports : [########################################] 100.00%
    [*] Phase 4: OS Detection...

    +==================================================================+
    |  SCAN RESULTS                                                    |
    +==================================================================+
    [*] Target: 192.168.1.1 (192.168.1.1)
    [*] OS Guess: Linux/Unix (TTL: 64)
    ==================================================================

    PORT      STATE     SERVICE         VERSION/BANNER
    --------- --------- --------------- ------------------------------------------
    22/tcp    open      ssh             OpenSSH 8.9p1 Ubuntu-3ubuntu0.4
    80/tcp    open      http            nginx/1.18.0
    443/tcp   open      https           nginx/1.18.0
    3306/tcp  open      mysql           5.7.42-0ubuntu0.18.04.1

    ==================================================================
    [*] Detailed Banners:
    ==================================================================
    Port 22 (ssh):
      | SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4

    Port 80 (http):
      | HTTP/1.1 200 OK
      | Server: nginx/1.18.0 (Ubuntu)
      | Content-Type: text/html; charset=UTF-8

    [*] Open: 4  Closed: 1002  Filtered: 40
    [*] Total scanned: 1046 ports
Output when target is DOWN:

text

    [*] Phase 0: Checking if host is alive...
    [-] Target is not reachable: Host is down or all ports filtered
    [-] Host 10.0.0.99 (10.0.0.99) appears to be DOWN
    [*] Possible reasons:
    [*]   - Target does not exist
    [*]   - Firewall blocking all connections
    [*]   - Host is offline
    [*]   - Network routing issue
Output when hostname is fake:

text

    [?] Enter target IP or URL: fakehost.invalid

    [-] Cannot resolve hostname: fakehost.invalid
    [*] Check the target address and try again
Module 2 - Banner Grabber
Grab banners from specific ports.

text

[?] Select option: 2
[?] Enter target IP or URL: 192.168.1.1
[?] Enter ports (comma separated) [21,22,80,443,3306,8080]: 22,80,443
Output:

text

    [*] Target: 192.168.1.1 (192.168.1.1)
    [*] Checking if host is reachable...
    [+] Host is reachable: Responding on port 22
    [*] Checking 3 ports...
    ==================================================================
    Port 22 (ssh):
      | SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.4

    Port 80 (http):
      | HTTP/1.1 200 OK
      | Server: nginx/1.18.0 (Ubuntu)
      | Content-Type: text/html; charset=UTF-8

    Port 443 (https):
      | HTTP/1.1 200 OK
      | Server: nginx/1.18.0 (Ubuntu)

    ==================================================================
    [*] Open ports: 3/3
    [*] Closed/filtered: 0/3
If port is closed:

text

    [!] Port 21: CLOSED or FILTERED
If host is unreachable:

text

    [*] Checking if host is reachable...
    [-] Host is not reachable: Host is down or all ports filtered
Module 3 - Hash Cracker
Auto-detects hash type and cracks it. Built-in wordlist included.

text

[?] Select option: 3
[?] Enter hash to crack: 5d41402abc4b2a76b9719d911017c592
[?] Add custom wordlist [y/N]: n
Supported hash types:

Type	Length	Example
MD5	32	5d41402abc4b2a76b9719d911017c592
SHA-1	40	aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
SHA-224	56	-
SHA-256	64	2cf24dba5fb0a30e26e83b2ac5b9e29e...
SHA-384	96	-
SHA-512	128	-
NTLM	32	066ddfd4ef0e9cd7c256fe77191ef43c
Base64	varies	cGFzc3dvcmQxMjM=
Hex	varies	68656c6c6f
Output (cracked):

text

    +==================================================================+
    |  HASH CRACKER                                                    |
    +==================================================================+
    [*] Hash: 5d41402abc4b2a76b9719d911017c592
    [*] Length: 32
    ==================================================================
    [*] Step 1: Identifying hash type...
    [>] Possible type: MD5
    [>] Possible type: NTLM

    [*] Step 2: Checking for simple encoding...
    [*] Not a simple base64 or hex encoding

    [*] Step 3: Dictionary attack...
    [*] Total candidates: 4,832
    [*] Trying as MD5...

    ==================================================================
    [+] CRACKED!
    [>] Hash:      5d41402abc4b2a76b9719d911017c592
    [>] Plaintext: hello
    [>] Hash Type: MD5

    [*] Attempts: 582
    [*] Speed: 1,940,000 H/s
    [*] Time: 0.00s
Output (base64 detected):

text

    [?] Enter hash to crack: cGFzc3dvcmQxMjM=

    [*] Step 2: Checking for simple encoding...
    [+] Base64 decoded text: password123
Output (with custom wordlist):

text

    [?] Enter hash to crack: 482c811da5d5b4bc6d497ffa98491e38
    [?] Add custom wordlist [y/N]: y
    [?] Wordlist file path: /usr/share/wordlists/rockyou.txt

    [*] Loading: /usr/share/wordlists/rockyou.txt
    [*] Custom words: 14,344,392
    [*] Total candidates: 28,751,216
    [*] Trying as MD5...
    [*] Cracking: [####------------------------------------]  10.00%

    ==================================================================
    [+] CRACKED!
    [>] Plaintext: password123
    [>] Hash Type: MD5
    [*] Speed: 2,635,527 H/s
Output (not cracked):

text

    [!] Hash not cracked with current wordlist
    [*] Tip: Add a custom wordlist (rockyou.txt)
    [*] Recommended: rockyou.txt, SecLists, CrackStation
Output (bcrypt detected):

text

    [?] Enter hash to crack: $2a$12$LJ3m4ys3Lg2VBe5F5OKi9u

    [*] Step 1: Identifying hash type...
    [>] Possible type: bcrypt

    [!] Skipping bcrypt (needs hashcat or john)
    [-] No crackable hash types detected
    [*] Use hashcat or john for specialized hash types
Test hashes you can try right now:

text

MD5 of "hello"       : 5d41402abc4b2a76b9719d911017c592
MD5 of "password123" : 482c811da5d5b4bc6d497ffa98491e38
MD5 of "admin"       : 21232f297a57a5a743894a0e4a801fc3
SHA1 of "hello"      : aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
SHA256 of "hello"    : 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
Base64 of "password" : cGFzc3dvcmQ=
Hex of "hello"       : 68656c6c6f
Module 4 - Brute Forcer
Verifies service is running before attacking. No fake results.

text

[?] Select option: 4
[?] Enter target IP or URL: 192.168.1.50
Then pick a service:

text

    SELECT SERVICE
      [1]  SSH (port 22)
      [2]  FTP (port 21)
      [3]  HTTP Basic Auth (port 80)
      [4]  HTTP Form Login (port 80)
      [5]  Telnet (port 23)
Then pick username mode:

text

    USERNAME
      [1]  Single username
      [2]  Username list file
      [3]  Built-in list (35 common usernames)
Then optional custom password list:

text

    [?] Add custom password list [y/N]: n
Output (service running, found credentials):

text

    [*] Verifying FTP service on 192.168.1.50:21...
    [+] Service confirmed: 220 (vsFTPd 3.0.3)

    [*] Users: 1
    [*] Passwords: 150
    [*] Combinations: 150
    [*] Final connection check...
    [+] Connection verified: 220 (vsFTPd 3.0.3)
    ==================================================================
    [*] Starting attack on FTP...
    ==================================================================
    [*] Attacking: [################------------------------]  35.33%
    [+] FOUND: admin:admin123

    ==================================================================
    [+] Found 1 valid credential(s):
    USERNAME                      PASSWORD
    ------------------------------ ------------------------------
    admin                         admin123
    [*] Attempts: 53
    [*] Speed: 17/s
    [*] Time: 3.12s
Output (service NOT running):

text

    [*] Verifying FTP service on 192.168.1.50:21...
    [-] FTP service is NOT responding:
    [-]   Connection refused
    [*] Target 192.168.1.50:21 is not reachable
    [*] Make sure the service is running on this target
Output (fake target):

text

    [?] Enter target IP or URL: fakehost.invalid
    [-] Cannot resolve: fakehost.invalid
    [*] Check the target address and try again
Output (no credentials found):

text

    [!] No valid credentials found
    [*] Try a larger wordlist or different usernames
    [*] Attempts: 150
HTTP Form Login example:

text

    [?] Select option: 4
    [?] Enter target IP or URL: 192.168.1.100

    [?] Select option: 4    (HTTP Form Login)
    [?] Port [80]: 80
    [?] Select option: 1    (Single username)
    [?] Enter username: admin
    [?] Add custom password list [y/N]: n
    [?] Verbose output [y/N]: n
    [?] Login page path [/login]: /wp-login.php

    Use ^USER^ and ^PASS^ as placeholders
    Example: user=^USER^&pass=^PASS^

    [?] Form data: log=^USER^&pwd=^PASS^&wp-submit=Log+In
    [?] Failure string [Invalid]: Invalid username
Module 5 - Web Fuzzer
Discovers hidden directories, files, subdomains, and parameters. Built-in 160+ wordlist included.

text

[?] Select option: 5
[?] Enter target URL [http://127.0.0.1]: http://192.168.1.100
Pick a mode:

text

    FUZZING MODE
      [1]  Directory / File discovery
      [2]  Subdomain enumeration
      [3]  Parameter fuzzing
Output (directory discovery):

text

    [*] Checking if target is reachable...
    [+] Target responded with status 200

    [*] Target: http://192.168.1.100
    [*] Mode: DIR
    [*] Words: 163
    [*] Extensions: php, html, txt
    ==================================================================

    STATUS    PATH                                    INFO
    --------- ---------------------------------------- --------------------
    [200] index.html                               [Size:11321] [Time:0.045s]
    [200] index.php                                [Size:11321] [Time:0.048s]
    [301] admin                                    [Size:312]   [Time:0.032s]
    [301] images                                   [Size:314]   [Time:0.029s]
    [200] robots.txt                               [Size:154]   [Time:0.027s]
    [200] login.php                                [Size:4521]  [Time:0.041s]
    [403] server-status                            [Size:299]   [Time:0.025s]
    [301] uploads                                  [Size:316]   [Time:0.030s]
    [200] config.bak                               [Size:1842]  [Time:0.035s]
    [200] phpinfo.php                              [Size:74829] [Time:0.067s]

    ==================================================================
    [*] Requests: 489
    [*] Found: 10
    [*] Errors: 2
    [*] Speed: 815 req/s
    [*] Time: 0.60s
Output (target not responding):

text

    [*] Checking if target is reachable...
    [-] Target is not responding
    [*] Check if the web server is running
Parameter fuzzing:

text

    [?] Enter target URL: http://192.168.1.100/page.php?id=FUZZ

    [?] Select option: 3    (Parameter fuzzing)

    STATUS    PATH                                    INFO
    --------- ---------------------------------------- --------------------
    [200] admin                                    [Size:11002] [Time:0.058s]
    [200] test                                     [Size:8442]  [Time:0.052s]
    [500] backup                                   [Size:892]   [Time:0.072s]
Adding custom wordlist:

text

    [?] Add custom wordlist [y/N]: y
    [?] Wordlist file path: /usr/share/dirb/common.txt

    [*] Loading: /usr/share/dirb/common.txt
    [*] Custom words: 4614
    [*] Words: 4777
Module 6 - File Password Cracker
Cracks password-protected ZIP files.

text

[?] Select option: 6
[?] Enter file path (ZIP): secret.zip
[?] Add custom wordlist [y/N]: n
Output (found):

text

    [*] Target: secret.zip
    [*] Type: ZIP
    [*] Candidates: 4,832
    [*] Cracking: [################------------------------]  40.00%

    ==================================================================
    [+] PASSWORD FOUND: sunshine2024
    [*] Attempts: 2,114
    [*] Speed: 352/s
    [*] Time: 6.01s
Output (not found):

text

    [!] Password not found
    [*] Try adding a custom wordlist (rockyou.txt)
Output (file not found):

text

    [?] Enter file path (ZIP): doesnotexist.zip
    [-] File not found: doesnotexist.zip
    [*] Check the file path and try again
Module 7 - Network Sweep
Finds live hosts on a network.

text

[?] Select option: 7
[?] Enter network CIDR [192.168.1.0/24]: 192.168.1.0/24
Output:

text

    [*] Network: 192.168.1.0/24
    [*] Hosts: 254
    ==================================================================
    [+] Host up: 192.168.1.1 (port 80)
    [+] Host up: 192.168.1.5 (port 22)
    [+] Host up: 192.168.1.50 (port 21)
    [+] Host up: 192.168.1.100 (port 80)
    [+] Host up: 192.168.1.254 (port 80)
    ==================================================================
    [*] Live hosts: 5/254
No hosts found:

text

    [!] No live hosts found on this network
Module 8 - DNS Lookup
text

[?] Select option: 8
[?] Enter domain: google.com
Output:

text

    [*] Target: google.com
    ==================================================================
    [>] A Record: 142.250.80.46
    [>] FQDN: google.com
    [>] Hostname: google.com
    [>] Address: 142.250.80.46
    [>] Address: 142.250.80.47
    [>] Reverse DNS: lhr48s29-in-f14.1e100.net
Fake domain:

text

    [?] Enter domain: notreal.invalid
    [-] Cannot resolve A record -- domain does not exist
Module 9 - WHOIS Lookup
text

[?] Select option: 9
[?] Enter domain: google.com
Output:

text

    [*] Target: google.com
    ==================================================================
    [>] refer: whois.verisign-grs.com
    [>] domain: GOOGLE.COM
    [>] organisation: Internet Corporation for Assigned Names and Numbers
    [>] status: ACTIVE
    [>] created: 1997-09-15
    [>] source: IANA
Module 10 - Check Dependencies
text

[?] Select option: 10
All installed:

text

    MODULE              STATUS         USED FOR
    ------------------- -------------- -----------------------------------
    paramiko            Installed      SSH brute force
    requests            Installed      HTTP fuzzing / brute force
    zipfile             Installed      ZIP file cracking
    urllib              Installed      Basic HTTP requests
Something missing:

text

    MODULE              STATUS         USED FOR
    ------------------- -------------- -----------------------------------
    paramiko            MISSING        SSH brute force
    requests            Installed      HTTP fuzzing / brute force

    [!] pip install paramiko
Built-in Wordlists
No external files needed. The tool has built-in lists:

List	Count	Used By
Passwords	150+ common passwords	Hash cracker, Brute forcer, ZIP cracker
Usernames	35+ common usernames	Brute forcer
Directories	160+ common paths	Web fuzzer
Extensions	20+ file extensions	Web fuzzer
Want bigger wordlists? Add your own when prompted:

text

[?] Add custom wordlist [y/N]: y
[?] Wordlist file path: /path/to/rockyou.txt
Recommended:

rockyou.txt
SecLists
CrackStation
Supported Platforms
Platform	Status	Notes
Windows 10/11	Fully supported	Use Windows Terminal for colors
Linux	Fully supported	Best experience
macOS	Fully supported	Default Terminal works
Kali Linux	Fully supported	Ideal for pentesting
Quick Start
Task	Steps
Scan a target	Run tool > Type 1 > Enter IP > Wait
Crack a hash	Run tool > Type 3 > Paste hash > Type n > Wait
Brute force FTP	Run tool > Type 4 > Enter IP > Type 2 > Type 1 > Enter username > Type n > Wait
Find directories	Run tool > Type 5 > Enter URL > Type 1 > Enter extensions > Type n > Wait
Find live hosts	Run tool > Type 7 > Enter CIDR > Wait
DNS lookup	Run tool > Type 8 > Enter domain > Wait
Project Structure
text

workstool/
|-- workstool.py     # Everything is in this single file
|-- README.md        # This file
Disclaimer
text

This tool is for AUTHORIZED SECURITY TESTING and EDUCATIONAL PURPOSES ONLY.
Always get written permission before testing any system you do not own.
Unauthorized access to computer systems is illegal.
The developer is not responsible for any misuse of this tool.
License
MIT License

Author
Your Name - GitHub - LinkedIn