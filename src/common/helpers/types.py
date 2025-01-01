_UNIT_MAP = {
    "k": 1_000,
    "m": 1_000_000,
    "b": 1_000_000_000,
}


def dehumanize(number_str: str) -> str:
    """
    Converts a human-readable number string to an integer.

    Handles the following humanized number formats:
    - Thousands: "1k", "1.2k"
    - Millions: "2m", "2.5m"
    - Billions: "3b", "3.5b"

    Also handles commas in the number string: "1,000", "1,000,000"

    :param number_str: The human-readable number string
    :return: The integer representation of the number string
    """
    if not number_str:
        return number_str

    number_str = number_str.replace(",", "")

    if not number_str[-1].isdigit():
        unit = number_str[-1].lower()
        if unit not in _UNIT_MAP:
            raise ValueError(f"Unknown human-readable number type: '{unit}'")
        return str(int(float(number_str[:-1]) * _UNIT_MAP[unit]))

    return number_str
