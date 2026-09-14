import json, sys

REQUIRED = {"id","dimension","title","surface","repro","evidence","severity","exploitability","status"}
ENUMS = {
    "severity": {"critical","high","medium","low","info"},
    "exploitability": {"trivial","easy","moderate","hard"},
    "status": {"candidate","confirmed","plausible","rejected"},
}

def validate_finding(obj):
    errors = []
    for f in REQUIRED - set(obj):
        errors.append(f"missing field: {f}")
    for f, allowed in ENUMS.items():
        if f in obj and obj[f] not in allowed:
            errors.append(f"field {f} has invalid value {obj[f]!r}")
    if "repro" in obj and not isinstance(obj["repro"], list):
        errors.append("field repro must be a list")
    return errors

def main(path):
    data = json.load(open(path))
    findings = data if isinstance(data, list) else [data]
    bad = 0
    for i, f in enumerate(findings):
        for e in validate_finding(f):
            bad += 1; print(f"[{i}] {e}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
