DNS CLI Tool
A powerful and versatile Python-based Command-Line Interface (CLI) tool designed for performing various DNS record lookups. This tool supports standard DNS queries (A, AAAA, MX, NS, TXT, CNAME) and integrates secure DNS protocols like DNS over TLS (DoT) and DNS over HTTPS (DoH) for enhanced privacy and security.

🌟 Features
Comprehensive DNS Lookups: Query for A, AAAA, MX, NS, TXT, and CNAME records.

Secure DNS Support:

DNS over TLS (DoT): Secure DNS queries over TLS connections.

DNS over HTTPS (DoH): Secure DNS queries over HTTPS connections.

Reverse IP Lookup: Get the hostname associated with an IP address (can be skipped).

Flexible Output: Save query results to files in JSON or plain text (.txt) format.

Robust Error Handling: Gracefully handles network issues, DNS resolution errors, and invalid inputs.

Default Resolver Fallback: Automatically attempts to use well-known public DNS resolvers if the primary configuration fails.

Input Validation: Basic validation for domain names to ensure correct formatting.

🚀 Installation
Clone the repository:

git clone https://github.com/TheForgettenFool/python-dns-tool.git


Install dependencies:
This project requires the dnspython library. You can install it using pip:

pip install dnspython

💡 Usage
The tool is executed via the main.py script.

python main.py <domain_name> [options]

Arguments:
<domain_name>: The domain name you want to query (e.g., google.com, example.org).

Options:
-o, --only <RECORD_TYPE> [<RECORD_TYPE> ...]: Specify one or more specific record types to query (e.g., A, AAAA, MX, NS, TXT, CNAME).

--out <FORMAT>: Save output to a file.

FORMAT: txt or json.

--no-reverse: Skip the reverse IP lookup.

--dot <RESOLVER_IP> <NAME>: Force DoT setup using a specific resolver IP and name.

RESOLVER_IP: IP address of the DoT resolver (e.g., 1.1.1.1).

NAME: Hostname of the DoT resolver (e.g., cloudflare-dns.com).

--doh <RESOLVER_IP> <URL>: Force DoH setup using a specific resolver IP and URL.

RESOLVER_IP: IP address of the DoH resolver (e.g., 1.1.1.1).

URL: URL of the DoH endpoint (e.g., https://cloudflare-dns.com/dns-query).

--normal: Use the system's default DNS resolver setup (this is the default behavior if --dot or --doh are not specified).

Examples:
Get all DNS records for a domain:

python main.py google.com

Get only A and MX records for a domain:

python main.py example.org --only A MX

Get all records and save to a JSON file:

python main.py mywebsite.com --out json

(This will create a file like All_records_DDMMYYYY_HH_MM_SS.json)

Perform a DoT lookup using Cloudflare's resolver:

python main.py cloudflare.com --dot 1.1.1.1 cloudflare-dns.com

Perform a DoH lookup using Google's resolver:

python main.py google.com --doh 8.8.8.8 https://dns.google/dns-query

Get A records without reverse IP lookup and save to a text file:

python main.py github.com --only A --no-reverse --out txt

(This will create a file like A_record_DDMMYYYY_HH_MM_SS.txt)

📂 Project Structure
.
├── main.py        # Main script for parsing arguments and orchestrating DNS lookups
├── resolver.py    # Contains functions for resolving specific DNS record types
└── config.py      # Handles DNS resolver configuration (default, DoT, DoH) and IP validation

🛠️ Error Handling
The tool includes basic error handling for network connectivity issues, DNS resolution failures, and invalid domain names. Errors are printed to the console to inform the user.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

