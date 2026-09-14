import os, json, sys

MARKERS = {
    "python": ["requirements.txt","pyproject.toml","setup.py"],
    "node": ["package.json"],
    "kotlin": ["build.gradle.kts","build.gradle"],
    "dotnet": [".csproj"],
}

def _has(root, name):
    if name.startswith("."):
        return any(f.endswith(name) for f in os.listdir(root))
    return os.path.exists(os.path.join(root, name))

def detect_stack(root):
    langs, signals = [], []
    for lang, files in MARKERS.items():
        for f in files:
            if _has(root, f):
                langs.append(lang); signals.append(f); break
    text = ""
    for f in os.listdir(root):
        if f.endswith((".py",".js",".ts",".json",".txt",".toml")):
            try: text += open(os.path.join(root,f)).read().lower()
            except Exception: pass
    kind = "unknown"
    if any(k in text for k in ("fastapi","express","flask","django","aspnet","gin ")):
        kind = "api"
    if any(k in text for k in ("next","react","vue","svelte","<html")):
        kind = "web"
    if "kotlin" in langs or "android" in text:
        kind = "mobile"
    runnable = bool(langs) and kind != "unknown"
    return {"kind": kind, "languages": langs, "runnable": runnable, "signals": signals}

if __name__ == "__main__":
    print(json.dumps(detect_stack(sys.argv[1] if len(sys.argv)>1 else "."), indent=2))
