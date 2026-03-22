"""
Helper module: apply manual timestampCorrections on top of a timestampMap.

Import and call apply_corrections() after building a timestampMap.
Corrections always win over auto-generated values.
"""


def apply_corrections(service, timestamp_map_entries):
    """
    Given a service object and its timestampMap entries (list of dicts),
    apply any timestampCorrections on top, returning the modified entries.
    Corrections always win over auto-generated values.
    """
    corrections = service.get("timestampCorrections", {})
    if not corrections:
        return timestamp_map_entries

    for entry in timestamp_map_entries:
        chant_id = entry.get("chantId")
        chant_corrections = corrections.get(chant_id)
        if not chant_corrections:
            continue
        line_map = {line["lineIndex"]: line for line in entry.get("lines", [])}
        for correction in chant_corrections:
            idx = correction["lineIndex"]
            if idx in line_map:
                line_map[idx]["cueIn"] = correction["cueIn"]

    return timestamp_map_entries
