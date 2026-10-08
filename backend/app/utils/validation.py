VALID_RECORD_TYPES = {"A", "AAAA", "CNAME", "TXT", "MX", "NS", "PTR", "SRV", "CAA"}
VALID_ZONE_TYPES = {"Public", "Private"}


def normalize_domain(value: str) -> str:
    return value.strip().lower().rstrip(".")


def validate_domain_name(name: str) -> str:
    normalized = normalize_domain(name)
    parts = normalized.split(".")
    if (
        not normalized
        or "." not in normalized
        or any(not part or len(part) > 63 for part in parts)
        or len(normalized) > 253
    ):
        raise ValueError("Enter a valid domain name")
    return normalized


def normalize_record_name(name: str) -> str:
    normalized = name.strip().lower().rstrip(".")
    if not normalized:
        raise ValueError("Record name is required")
    return normalized


def validate_record_type(record_type: str) -> str:
    normalized = record_type.strip().upper()
    if normalized not in VALID_RECORD_TYPES:
        raise ValueError("Unsupported record type")
    return normalized


def normalize_record_value(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("Record value is required")
    return normalized
