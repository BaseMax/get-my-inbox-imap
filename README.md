# get-my-inbox-imap

This is a Python script that connects to an IMAP server, logs in using provided credentials, and fetches emails based on specific criteria. The script supports connecting through a proxy server, retries on failure, and reads emails containing certain keywords.

## Features
- Connects to an IMAP server using SSL.
- Supports logging in to the server with username and password.
- Allows searching for emails containing specific keywords from a specific sender (e.g., GitHub).
- Proxy support (HTTP, SOCKS4, SOCKS5).
- Retries for network-related errors.
- Fetches and prints email content.

## Requirements

- Python 3.x
- `socks` library (`pip install PySocks`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BaseMax/get-my-inbox-imap.git
   ```

2. Install the required dependencies:
   ```bash
   pip install PySocks
   ```

## Usage

To run the script, use the following command:

```bash
python imap.py <username> <password> [--host <host>] [--port <port>] [--proxy_host <proxy_host>] [--proxy_port <proxy_port>] [--proxy_type <proxy_type>]
```

### Parameters:

- `<username>`: The IMAP username (usually your email address).
- `<password>`: The IMAP password (you may need to generate an app-specific password for some providers).
- `--host`: The IMAP server host (default: `secureimap.t-online.de`).
- `--port`: The IMAP server port (default: `993`).
- `--proxy_host`: The proxy server host (optional).
- `--proxy_port`: The proxy server port (optional).
- `--proxy_type`: The proxy type (`HTTP`, `SOCKS4`, or `SOCKS5`; default: `HTTP`).

### Example:

```bash
python imap.py example@gmail.com mypassword --host imap.gmail.com --port 993 --proxy_host 127.0.0.1 --proxy_port 1080 --proxy_type SOCKS5
```

This command will connect to the IMAP server(s), authenticate using the provided username and password, and fetch emails containing the keyword "github.com" from "github.com".

## Disclaimer

Use the script responsibly. Ensure that you have permission to access the email account and that the use of proxies is allowed by your network or service provider.

## Contact

For any issues or feature requests, feel free to open an issue on the [GitHub repository](https://github.com/BaseMax/get-my-inbox-imap).

## License

MIT License

Copyright 2025 Max Base
