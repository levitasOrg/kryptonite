import os
from scripts.detect_stack import detect_stack

def test_detects_python_fastapi(tmp_path):
    (tmp_path/"requirements.txt").write_text("fastapi\nuvicorn\n")
    (tmp_path/"main.py").write_text("from fastapi import FastAPI\napp=FastAPI()\n")
    r = detect_stack(str(tmp_path))
    assert "python" in r["languages"]
    assert r["kind"] in ("api","web")
    assert r["runnable"] is True

def test_unknown_when_empty(tmp_path):
    r = detect_stack(str(tmp_path))
    assert r["kind"] == "unknown"
    assert r["runnable"] is False
