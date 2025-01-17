# 
# Max Base
# https://github.com/BaseMax/get-my-inbox-imap
# 
import sys
import time
import email
import socks
import socket
import imaplib
import argparse

def set_proxy(proxy_host, proxy_port, proxy_type="HTTP"):
    """Set up a socket proxy for IMAP."""
    proxy_types = {
        "SOCKS4": socks.SOCKS4,
        "SOCKS5": socks.SOCKS5,
        "HTTP": socks.HTTP,
    }
    if proxy_type not in proxy_types:
        raise ValueError("Unsupported proxy type. Use SOCKS4, SOCKS5, or HTTP.")
    
    if proxy_host and proxy_port:
        socks.setdefaultproxy(proxy_types[proxy_type], proxy_host, proxy_port)
        socket.socket = socks.socksocket

def imap_connect(host, port, timeout=20, retries=3):
    """Connect to the IMAP server with retry logic."""
    socket.setdefaulttimeout(timeout)
    for attempt in range(retries):
        try:
            mail = imaplib.IMAP4_SSL(host, port)
            return mail
        except socket.timeout:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise RuntimeError("NETWORK")
        except imaplib.IMAP4.error:
            raise RuntimeError("ERROR")
        except Exception:
            raise RuntimeError("ERROR")

def imap_login(mail, username, password, retries=3):
    """Log in to the IMAP server with retry logic."""
    for attempt in range(retries):
        try:
            response = mail.login(username, password)
            return response
        except socket.timeout:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise RuntimeError("NETWORK")
        except imaplib.IMAP4.error:
            raise RuntimeError("FAIL")
        except Exception:
            raise RuntimeError("ERROR")

def imap_search_mails(mail, criteria, retries=3):
    """Search emails in the mailbox with retry logic."""
    for attempt in range(retries):
        try:
            mail.select("INBOX")
            result, data = mail.search(None, criteria)
            if result == "OK":
                return data[0].split()
            return []
        except socket.timeout:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise RuntimeError("NETWORK")
        except Exception:
            raise RuntimeError("ERROR")
        
def imap_read_mail(mail, message_id):
    result, data = mail.fetch(message_id, "(RFC822)")
    if result == "OK":
        for part in data:
            if isinstance(part, tuple):
                msg = email.message_from_bytes(part[1])
                if msg.is_multipart():
                    return "".join(
                        part.get_payload(decode=True).decode("utf-8", errors="replace")
                        for part in msg.walk()
                        if part.get_content_type() == "text/plain"
                    )
                else:
                    return msg.get_payload(decode=True).decode("utf-8", errors="replace")
    return ""


def main(HOST, PORT, USERNAME, PASSWORD):
    try:
        mail = imap_connect(HOST, PORT)
        login_res = imap_login(mail, USERNAME, PASSWORD)
    except Exception as e:
        print(e, end="")
        return

    if login_res[0] != "OK":
        print("FAIL", end="")
        return
    
    try:
        count = imap_search_mails(mail, '(BODY "github.com" FROM "github.com")')
    except Exception as e:
        print(e, end="")
        return

    if not count:
        print("NOKL", end="")
        return

    count = [int(x.decode('utf-8')) for x in count]
    count = sorted(count, reverse=True)
    
    read_mail = ""
    check = 0
    for mail_id in count:
        mail_id_bin = str(mail_id).encode('utf-8')
        read_mail = imap_read_mail(mail, mail_id_bin)

        print(read_mail)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IMAP Python Client")
    parser.add_argument("username", type=str, help="The IMAP username")
    parser.add_argument("password", type=str, help="The IMAP password")

    parser.add_argument("--host", type=str, default="secureimap.t-online.de", help="The IMAP server host")
    parser.add_argument("--port", type=int, default=993, help="The IMAP server port")

    parser.add_argument("--proxy_host", type=str, help="The proxy server host")
    parser.add_argument("--proxy_port", type=int, help="The proxy server port")
    parser.add_argument("--proxy_type", type=str, default="HTTP", choices=["HTTP", "SOCKS4", "SOCKS5"], help="The proxy type")

    args = parser.parse_args()
    try:
        main(args.host, args.port, args.username, args.password)
    except Exception as e:
        print(f"ERROR", end="")
        sys.exit(1)
