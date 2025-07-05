# 🧠 Python DNS Lookup CLI Tool

This is a Python-based command-line utility to perform DNS lookups (A, AAAA, MX, NS, TXT, CNAME), reverse IP lookups, and save the output in JSON format using flags.

---

## ⚙️ Features

- ✅ A, AAAA, MX, NS, TXT, CNAME record queries
- ✅ Reverse DNS lookup
- ✅ Argument flags using argparse
- ✅ Save output to JSON file
- ✅ Error handling for each record type
- ✅ Clean CLI formatting

---

## 🚀 How to Use

### Basic usage:
```bash
python dns_lookup.py example.com

Query specific records:
python dns_lookup.py example.com --only MX TXT

Save result to file:
python dns_lookup.py example.com --only MX --out

## 📁 File Structure

dns-lookup-tool/
├── dns_lookup.py       # Main script
├── README.md           # You're reading it now!

## 🙌 Author
Abinesh K
Python Enthusiast | DNS Tinkerer
