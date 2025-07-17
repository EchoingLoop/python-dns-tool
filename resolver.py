def resolve_type(domain, record_type, setup):
    record = {record_type: None, "error": None}
    try:
        resolve = setup
        record[record_type] = [
            r.to_text() for r in resolve.resolve(domain, record_type)
        ]
    except Exception as e:
        record["error"] = str(e)
    return record


def set_mode(domain: str, setup=None, record_type: str = None):
    rtype = ("A", "AAAA", "MX", "NS", "TXT", "CNAME")
    if record_type:
        record = resolve_type(domain, record_type, setup)
    else:
        record = []
        for type in rtype:
            record.append(resolve_type(domain, type, setup))
    return record
