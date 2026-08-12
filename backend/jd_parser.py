import re

REQUIRED_MARKERS = ["requirements", "required qualifications", "must have", "minimum qualifications"]
PREFERRED_MARKERS = ["preferred qualifications", "nice to have", "preferred skills", "bonus"]


def _find_block(text: str, markers: list) -> str:
    lower = text.lower()
    for marker in markers:
        idx = lower.find(marker)
        if idx != -1:
            # take ~600 chars after the marker as the relevant block
            return text[idx: idx + 600]
    return ""


def parse_job_description(text: str) -> dict:
    required_block = _find_block(text, REQUIRED_MARKERS) or text
    preferred_block = _find_block(text, PREFERRED_MARKERS)

    return {
        "raw_text": text,
        "required_block": required_block,
        "preferred_block": preferred_block,
    }
