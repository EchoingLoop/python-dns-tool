import ipaddress
import dns.exception
import dns.resolver
import dns.nameserver
import sys
import socket

def check_ip(ip=str):
    try:
        ip = ipaddress.ip_address(ip)
        return True
    except Exception as e:
        print(f"Not an valid IP address\n Error: {e}")
        return False

"""""
This function set default stud revsolver from stored ip try DoT/DoH if fails fall back 
auto 

""" ""
def default_resolver_config():
    backup_resolver_id = ("9.9.9.9", "1.1.1.1", "8.8.8.8", "1.0.0.1", "208.67.222.222")
    attempt = 3
    for resolver_default_ip in backup_resolver_id:
        try:
            resolver = dns.resolver.make_resolver_at(resolver_default_ip)
            resolver.try_ddr(lifetime=4)
            resolver.resolve("cloudflare.com","A")
            print(f"Default resolver set to '{resolver_default_ip}'\n")
            break
        except (dns.exception.DNSException,socket.error,OSError) as e:
            print(
                f"Failed to set default resolver to '{resolver_default_ip}'\n error: {e}"
            )
            backup_server_initiation = str(
                input("Initiate backup resolver setup [Y/n]:")
            ).lower()
            while True:
                if attempt > 0:
                    if backup_server_initiation not in ("y", "n"):
                        backup_server_initiation = str(
                            input("Please enter valid value [Y/n]:")
                        )
                        attempt -= 1
                    else:
                        break
                else:
                    print("Exceeded allowed attempts. Exiting...")
                    sys.exit(1)
            if backup_server_initiation == "y":
                continue
            else:
                print("DNS config failed and exit")
                sys.exit(1)
    return resolver

def config_DoT_recrusive(resolver_ip:str,name:str):
    resolver = dns.resolver.make_resolver_at(resolver_ip)
    resolver.require_secure_transport = True
    try:
        resolver.dot = dns.nameserver.DoTNameserver(resolver_ip,name)
        resolver.resolve("cloudflare.com","A",lifetime=4)
        print(f"DoT secure connection is established to {resolver_ip}")
    except (dns.exception.DNSException,Exception) as e:
        print(f"DoT setup {resolver_ip} failed \nError: {e}")
        sys.exit(1)
    return resolver

def config_DoH_recrusive(resolver_ip:str,url:str):
    resolver = dns.resolver.make_resolver_at(resolver_ip)
    resolver.require_secure_transport = True
    try:
        resolver.doh = dns.nameserver.DoHNameserver(url,resolver_ip)
        resolver.resolve("cloudflare.com","A",lifetime=4)
        print(f"DoH secure connection is established to {resolver_ip}")
    except (dns.exception.DNSException, Exception)  as e:
        print(f"DoH setup {resolver_ip} failed \nError: {e}")
        sys.exit(1)
    return resolver
