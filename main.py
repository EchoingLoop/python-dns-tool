import socket
import argparse
import sys
import json
import os
import datetime
import config
from resolver import set_mode

parser = argparse.ArgumentParser(
    prog="DNS CLI Tool",
    description="Gives you A, AAA, MX, NS, TXT, CNAME for the domain name you enter",
)
parser.add_argument("domain_name", type=str, help="The name of the domain")
parser.add_argument(
    "-o",
    "--only",
    choices=["A", "AAAA", "MX", "NS", "TXT", "CNAME"],
    type=str,
    nargs="+",
    help="If only a specific record is needed(optional)",
)
parser.add_argument(
    "--out",
    choices=["txt", "json"],
    type=str,
    help="Save output to file in json and txt format",
)
parser.add_argument(
    "--no-reverse", action="store_true", help="This skips the reverse ip lookup"
)

group = parser.add_mutually_exclusive_group()
group.add_argument("--dot", type=str, nargs="+", help="Force DoT setup")
group.add_argument("--doh", type=str, nargs="+", help="Foce DoH setup")
group.add_argument("--normal", action="store_true", help="Use system default setup")
args = parser.parse_args()

# It gets record by using dns resolver and catch error if it occurs


def records_check(domain: str, record_type, setup):
    record = {record_type: None, "error": None}
    try:
        resolve = setup
        record[record_type] = [
            r.to_text() for r in resolve.resolve(domain, record_type)
        ]
    except Exception as e:
        record["error"] = str(e)
    return record


# It call records_check function to A, AAAA, MX, NS, TXT, CNAME dns records


def get_dns_records(domain, setup):
    return [
        records_check(domain, "A", setup),
        records_check(domain, "AAAA", setup),
        records_check(domain, "MX", setup),
        records_check(domain, "NS", setup),
        records_check(domain, "TXT", setup),
        records_check(domain, "CNAME", setup),
    ]


# This function get the ip address of the domain name and reverse it by using th address it got


def get_ip(host):
    ip_handle = {"ip": [], "reverse_ip": None, "error": None}
    try:
        for add in socket.getaddrinfo(host, None):
            if add[4][0] in ip_handle["ip"]:
                continue
            else:
                ip_handle["ip"].append(add[4][0])
        try:
            ip_handle["reverse_ip"] = [
                socket.gethostbyaddr(ip)[0] for ip in ip_handle["ip"]
            ]
        except Exception as e:
            ip_handle["error"] = str(e)
    except Exception as e:
        ip_handle["error"] = str(e)
    return ip_handle


# Prints record data using JSON string formatting (for readability)
def simple_print(resolve):
    prev_key = None
    for key, value in resolve.items():
        if key == "error" and value == None:
            continue
        elif key != "error" and value == None:
            prev_key = key
            continue
        elif key == "error":
            print(f"{prev_key} Lookup Error: {json.dumps(value, indent=4)}")
        else:
            print(f"{key}:{json.dumps(value, indent=4)}")
        prev_key = key
    print("-----")


# To verify host name


def is_valid_char(c):
    return (
        c.isalnum() or c in "-."
    )  # isalnum check if its string and number and fails when special case so "-." is to include this specific special case


# Function which get ip,reverse and all the record type


def collects_DNS(domain_name, setup):
    dns_resolve = set_mode(domain_name, setup)
    if not args.no_reverse:
        dns_lookup = get_ip(domain_name)
        del dns_lookup["ip"]
        dns_resolve.append(dns_lookup)
    if not args.out:
        for resolve in dns_resolve:
            simple_print(resolve)
    else:
        write_record_to_file(f"All_records.{args.out}", dns_resolve)


# Write the record in jason or txt format
def write_record_to_file(file_name, rec):
    bash_name, exe = os.path.splitext(file_name)
    timestamp = datetime.datetime.now().strftime("%d%m%Y_%H_%M_%S")
    new_filename = f"{bash_name}_{timestamp}{exe}"
    try:
        with open(new_filename, "w") as f:
            if exe == ".json":
                json.dump(rec, f, indent=4)
            else:
                if isinstance(rec, list):
                    for records_val in rec:
                        f.write(f"{str(records_val)}\n")
                else:
                    f.write("{\n")
                    for key, value in rec.items():
                        f.write(f"\t{key}: {value}" + "\n")
                    f.write("}\n")
            print(f"File has been saved as {new_filename}")
    except IOError as e:
        print(f"Error saving file {e}")


# Main function


def main():
    domain_name = args.domain_name.strip().replace(" ", "").lower()
    for char in domain_name:
        if not is_valid_char(char):
            print("DNS Host Name is Invalid")
            sys.exit(1)  ## Exit if domain or record type is invalid
    if args.dot:
        setup = config.config_DoT_recrusive(args.dot[0], args.dot[1])
    elif args.doh:
        setup = config.config_DoH_recrusive(args.doh[0], args.doh[1])
    else:
        setup = config.default_resolver_config()
    if args.only == None:
        collects_DNS(domain_name, setup)
    else:
        if len(args.only) > 1:
            for record_type in args.only:
                record = set_mode(domain_name, setup, record_type)
                if not args.out:
                    simple_print(record)
                else:
                    write_record_to_file(f"{record_type}_record.{args.out}", record)
        else:
            record = set_mode(domain_name, setup, args.only[0])
            if not args.out:
                simple_print(record)
            else:
                write_record_to_file(f"{args.only[0]}_record.{args.out}", record)


if __name__ == "__main__":
    main()
