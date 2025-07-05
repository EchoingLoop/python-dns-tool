import socket
import dns.resolver
import argparse
import sys
import json

parser = argparse.ArgumentParser(
    description="Gives you A, AAA, MX, NS, TXT, CNAME for the domain name you enter"
)
parser.add_argument("domain_name", type=str, help="The name of the host")
parser.add_argument(
    "-o",
    "--only",
    type=str,
    nargs="+",
    help="If only a specific record is needed(optional)",
)
parser.add_argument(
    "-s", "--out", action="store_true", help="Save output to file in jason"
)
args = parser.parse_args()


# It gets record by using dns resolver and catch error if it occurs


def records_check(domain, record_type):
    record = {record_type: None, "error": None}
    try:
        record[record_type] = [
            r.to_text() for r in dns.resolver.resolve(domain, record_type)
        ]
    except Exception as e:
        record["error"] = str(e)
    return record


# It call records_check function to A, AAAA, MX, NS, TXT, CNAME dns records


def get_dns_records(domain):
    return [
        records_check(domain, "A"),
        records_check(domain, "AAAA"),
        records_check(domain, "MX"),
        records_check(domain, "NS"),
        records_check(domain, "TXT"),
        records_check(domain, "CNAME"),
    ]


# This function get the ip address of the domain name and reverse it by using th address it got


def get_ip(host):
    ip_handle = {"ip": None, "reverse": None, "error": None}
    try:
        ip_handle["ip"] = socket.gethostbyname(host)
        try:
            ip_handle["reverse"] = socket.gethostbyaddr(ip_handle["ip"])[0]
        except socket.gaierror as e:
            ip_handle["error"] = str(e)
    except socket.gaierror as e:
        ip_handle["error"] = str(e)
    return ip_handle


def simple_print(resolve):
    prev_key = None
    for key, value in resolve.items():
        if key == "error" and value == None:
            continue
        elif key != "error" and value == None:
            prev_key = key
            continue
        elif key == "error":
            print(f"{prev_key} Lookup Error: {json.dumps(value)}")
        else:
            print(f"{key}:{json.dumps(value)}")
        prev_key = key
    print("-----")


# To verify host name


def is_valid_char(c):
    return (
        c.isalnum() or c in "-."
    )  # isalnum check if its string and number and fails when special case so "-." is to include this specific special case


# Function which get ip,reverse and all the record type


def collects_DNS(domain_name):

    dns_resolve = get_dns_records(domain_name)
    dns_lookup = get_ip(domain_name)
    print(f"== DNS LOOKUP FOR: {domain_name}")
    print("== IP LOOKUP ==")
    for key in dns_lookup:
        if key == "error" and dns_lookup[key] == None:
            continue
        elif key == "error":
            print(f"IP Lookup Error: {dns_lookup[key]}")
        else:
            print(f"{key}: {dns_lookup[key]}")
    for resolve in dns_resolve:
        simple_print(resolve)


# Prints record data using JSON string formatting (for readability)
# "Multiple records will overwrite the same file. Later, filename customization is recommended."
def write_record_to_file(rec):
    with open("DNS_lookup_record.json", "w") as f:
        json.dump(rec, f, indent=4)
    print("Saved in file")


# Main function


def main():
    domain_name = args.domain_name.strip().replace(" ", "").lower()
    for char in domain_name:
        if not is_valid_char(char):
            print("DNS Host Name is Invalid")
            sys.exit(1)  ## Exit if domain or record type is invalid
    valid_checks = {"A", "AAAA", "MX", "NS", "TXT", "CNAME"}
    if args.only == None:
        collects_DNS(domain_name)
    else:
        requested_records = [s.upper() for s in args.only]
        for record_type in requested_records:
            if record_type not in valid_checks:
                print(f"Unsupported record type: {record_type}")
                sys.exit(1)
        if len(requested_records) > 1:
            for record_type in requested_records:
                record = records_check(domain_name, record_type)
                if not args.out:
                    simple_print(record)
                else:
                    write_record_to_file(record)
        else:
            record = records_check(domain_name, requested_records[0])
            simple_print(record)


if __name__ == "__main__":
    main()
