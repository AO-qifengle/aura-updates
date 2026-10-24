"""Anonymous native HTTP acceptance, runnable locally and on a fresh GitHub runner."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

LATEST = "https://ao-qifengle.github.io/aura-updates/updates/latest.json"
DIGEST = "7fb642c8579d31ca8c0d95bee211cb94d74c0998c0f1e8132eee362699dcf9f1"
EXPECTED_DMG = "https://github.com/AO-qifengle/aura-updates/releases/download/V0.5.5.0-build67/Aura-Demo-V0.5.5.0-build67-arm64.dmg"
EXPECTED_NOTES = "https://ao-qifengle.github.io/aura-updates/updates/V0.5.5.0.html"


def fetch(url, label, output, mime, include_headers=False):
    command = [
        "curl", "--fail", "--silent", "--show-error", "--location",
        "--connect-timeout", "15", "--max-time", "90",
        "-H", "User-Agent: Aura/1.0",
        "-D", str(output.with_suffix(".headers")), "-o", str(output),
        "-w", "%{http_code}\t%{content_type}\t%{url_effective}",
    ]
    if include_headers:
        command.append("-i")
    result = subprocess.run(command + [url], check=True, capture_output=True, text=True)
    status, content_type, final_url = result.stdout.strip().split("\t", 2)
    print(f"{label}: HTTP {status}; content-type: {content_type}", flush=True)
    assert status == "200", f"{label}: unexpected status {status}"
    assert content_type.split(";", 1)[0].strip().lower() == mime, f"{label}: unexpected MIME {content_type}"
    data = output.read_bytes()
    if include_headers:
        data = data.rsplit(b"\r\n\r\n", 1)[-1]
    return data


with tempfile.TemporaryDirectory(prefix="aura-anonymous-check-") as directory:
    root = Path(directory)
    manifest = json.loads(fetch(LATEST, "latest.json", root / "latest.response", "application/json", True))
    assert manifest == {
        "schema": 1, "version": "V0.5.5.0", "build": 67,
        "minimumMacOS": "15.0", "architecture": "arm64",
        "downloadURL": EXPECTED_DMG, "sha256": DIGEST,
        "releaseNotesURL": EXPECTED_NOTES, "publishedAt": "2026-10-19T03:32:57Z",
    }
    dmg = fetch(manifest["downloadURL"], "DMG", root / "Aura.dmg", "application/octet-stream")
    assert len(dmg) == 3060605
    assert dmg[-512:-508] == b"koly", "Not a UDIF disk image"
    assert hashlib.sha256(dmg).hexdigest() == DIGEST
    print(f"SHA-256: {DIGEST}", flush=True)
    notes = fetch(manifest["releaseNotesURL"], "release notes", root / "notes.html", "text/html")
    assert b"V0.5.5.0" in notes and b"Aura" in notes
    print("PASS: no cookies, Authorization, login or browser challenge execution", flush=True)
