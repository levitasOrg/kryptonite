from scripts.validate_findings import validate_finding

VALID = {"id":"F1","dimension":"security-pentest","title":"IDOR on /orders","surface":"GET /orders/{id}","repro":["auth as user A","GET /orders/<B_id>"],"evidence":"200 with B's data","severity":"high","exploitability":"easy","status":"confirmed"}

def test_valid_finding_has_no_errors():
    assert validate_finding(VALID) == []

def test_missing_field_reported():
    bad = {k:v for k,v in VALID.items() if k != "severity"}
    assert any("severity" in e for e in validate_finding(bad))

def test_bad_enum_reported():
    bad = dict(VALID, severity="spicy")
    assert any("severity" in e for e in validate_finding(bad))
