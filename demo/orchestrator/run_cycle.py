"""Attack → Defend cycle orchestrator.

Modes:
  stub   — offline deterministic demo (default)
  claude — placeholder for live Anthropic red provider
  codex  — placeholder for live OpenAI blue provider
  hybrid — both live (when adapters implemented)

Safety: only allowlisted check types against in-scope hosts. No exploit generation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
SCOPE_DEFAULT = Path(__file__).resolve().parent / "scope.lab.json"

SECRET_RE = re.compile(r"(sk_live_[A-Za-z0-9_]+|api[_-]?key[\"']?\s*[:=]\s*[\"'][^\"']+)", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_scope(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def redact(text: str) -> str:
    return SECRET_RE.sub("[REDACTED]", text)


def http_get(url: str, timeout: float = 3.0) -> tuple[int, dict[str, str], str]:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, headers, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        headers = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
        return e.code, headers, body


def assert_in_scope(url: str, scope: dict[str, Any]) -> None:
    allowed = scope["in_scope"]["hosts"]
    # url like http://127.0.0.1:8080/path
    hostport = url.split("//", 1)[-1].split("/", 1)[0]
    if hostport not in allowed:
        raise PermissionError(f"Host {hostport} out of scope; allowed={allowed}")


# --- Red (Claude) providers -------------------------------------------------

def red_stub(scope: dict[str, Any], base: str) -> list[dict[str, Any]]:
    """Deterministic adversarial hypotheses for the lab app."""
    return [
        {
            "id": "F-001",
            "title": "Debug config endpoint publicly reachable",
            "severity": "high",
            "mitre": ["T1082", "T1552.001"],
            "hypothesis": (
                "A staging payments app exposes /debug/config without auth, leaking "
                "environment details and credential-shaped secrets to anyone who can reach the host."
            ),
            "business_risk": "Secret material and internal topology accelerate account takeover and fraud against payment flows.",
            "authorized_check": {
                "type": "http_get",
                "url": f"{base}/debug/config",
                "expect_not_status": 200,
            },
            "detection_gap": "No alert on access to sensitive debug paths from non-operator networks.",
            "provider": "stub-claude-red",
        },
        {
            "id": "F-002",
            "title": "Admin panel reachable without authentication",
            "severity": "high",
            "mitre": ["T1190", "T1078"],
            "hypothesis": " /admin returns privileged data with no auth challenge in insecure mode.",
            "business_risk": "Unauthorized user enumeration and admin function abuse on a payments-adjacent app.",
            "authorized_check": {
                "type": "http_get",
                "url": f"{base}/admin",
                "expect_status_in": [401, 403],
            },
            "detection_gap": "Missing 401/403 anomaly detection on admin routes.",
            "provider": "stub-claude-red",
        },
        {
            "id": "F-003",
            "title": "Overly permissive CORS reflects wildcard origin",
            "severity": "medium",
            "mitre": ["T1185"],
            "hypothesis": "Access-Control-Allow-Origin: * on API responses enables hostile browser origins to read responses.",
            "business_risk": "Cross-origin data theft from authenticated browser sessions if cookies/tokens are present.",
            "authorized_check": {
                "type": "http_header",
                "url": f"{base}/health",
                "header": "access-control-allow-origin",
                "expect_not_equals": "*",
            },
            "detection_gap": "No CSP/CORS misconfiguration monitors in CI.",
            "provider": "stub-claude-red",
        },
    ]


def red_claude_live(_scope: dict[str, Any], _base: str) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Live Claude adapter not wired yet. Use --mode stub for demos, "
        "or implement providers/claude_red.py with structured JSON output."
    )


# --- Validation -------------------------------------------------------------

def run_check(check: dict[str, Any], scope: dict[str, Any]) -> dict[str, Any]:
    ctype = check["type"]
    if ctype not in scope["in_scope"]["check_types"]:
        return {"ok": False, "error": f"check type {ctype} not allowlisted"}

    url = check["url"]
    assert_in_scope(url, scope)
    status, headers, body = http_get(url)
    body = redact(body)

    if ctype == "http_get":
        if "expect_not_status" in check:
            ok = status != check["expect_not_status"]
            return {
                "ok": ok,
                "observed_status": status,
                "detail": "endpoint should not be publicly readable" if not ok else "endpoint restricted",
                "body_excerpt": body[:200],
            }
        if "expect_status_in" in check:
            ok = status in check["expect_status_in"]
            return {
                "ok": ok,
                "observed_status": status,
                "detail": "expected auth challenge" if not ok else "auth challenge present",
                "body_excerpt": body[:200],
            }

    if ctype == "http_header":
        header = check["header"].lower()
        observed = headers.get(header)
        ok = observed != check.get("expect_not_equals")
        return {
            "ok": ok,
            "observed_header": observed,
            "detail": "CORS wildcard present" if not ok else "CORS not wildcard",
        }

    return {"ok": False, "error": f"unsupported check {ctype}"}


def validate_findings(findings: list[dict[str, Any]], scope: dict[str, Any]) -> list[dict[str, Any]]:
    validated = []
    for f in findings:
        result = run_check(f["authorized_check"], scope)
        # Confirmed if the secure expectation FAILED (i.e. vulnerability present)
        confirmed = not result.get("ok", False) and "error" not in result
        entry = {**f, "validation": result, "confirmed": confirmed}
        validated.append(entry)
    return validated


# --- Blue (Codex) providers -------------------------------------------------

REMEDIATIONS = {
    "F-001": {
        "summary": "Disable debug config exposure; serve 404 unless operator auth.",
        "files": {
            "lab-app/HARDENING.md": (
                "# Hardening notes for F-001\n\n"
                "- Set `LAB_SECURE=1` (or equivalent feature flag) so `/debug/config` returns 404.\n"
                "- Never embed live API keys in process config; inject via secret manager.\n"
                "- Alert on any hit to `/debug/*` from non-VPN CIDRs.\n"
            )
        },
        "diff": """\
--- a/demo/lab-app/server.py
+++ b/demo/lab-app/server.py
@@ config @@
- "debug": True  # insecure demo default
+ "debug": False  # remediated: debug endpoints off
""",
        "detection": {
            "name": "sensitive_debug_path_access",
            "sketch": "ALERT when http.path LIKE '/debug/%' AND src.network NOT IN operator_cidrs",
        },
        "verify_hint": "LAB_SECURE=1 → GET /debug/config returns 404",
    },
    "F-002": {
        "summary": "Require authentication on /admin; return 401 when anonymous.",
        "files": {
            "lab-app/HARDENING.md": (
                "# Hardening notes for F-002\n\n"
                "- Gate `/admin` behind SSO / mTLS.\n"
                "- Default deny; no public admin in staging replicas that share prod-like data.\n"
            )
        },
        "diff": """\
--- a/demo/lab-app/server.py
+++ b/demo/lab-app/server.py
@@ admin @@
- admin_panel_public = True
+ admin_panel_public = False
""",
        "detection": {
            "name": "admin_unauth_success",
            "sketch": "ALERT when path=/admin AND status=200 AND user.authenticated=false",
        },
        "verify_hint": "LAB_SECURE=1 → GET /admin returns 401",
    },
    "F-003": {
        "summary": "Replace CORS wildcard with explicit application origin.",
        "files": {
            "lab-app/HARDENING.md": (
                "# Hardening notes for F-003\n\n"
                "- Set `Access-Control-Allow-Origin` to the known app origin only.\n"
                "- Add CI check that fails on `*` for credentialed APIs.\n"
            )
        },
        "diff": """\
--- a/demo/lab-app/server.py
+++ b/demo/lab-app/server.py
@@ cors @@
- cors_allow_origin = "*"
+ cors_allow_origin = "https://app.example.com"
""",
        "detection": {
            "name": "cors_wildcard_deployed",
            "sketch": "CI policy: fail if ACAO header equals * on authenticated services",
        },
        "verify_hint": "LAB_SECURE=1 → ACAO header is not *",
    },
}


def blue_stub(confirmed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for f in confirmed:
        rem = REMEDIATIONS.get(f["id"])
        if not rem:
            continue
        out.append(
            {
                "finding_id": f["id"],
                "provider": "stub-codex-blue",
                "summary": rem["summary"],
                "diff": rem["diff"],
                "files": rem["files"],
                "detection": rem["detection"],
                "verify_hint": rem["verify_hint"],
            }
        )
    return out


def blue_codex_live(_confirmed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "Live Codex adapter not wired yet. Use --mode stub for demos, "
        "or implement providers/codex_blue.py that returns diffs + verify tests."
    )


# --- Verify after remediation narrative ------------------------------------

def verify_expectations(scope: dict[str, Any], base: str, secure_assumed: bool) -> dict[str, Any]:
    """
    In stub demos we verify the *running* lab.
    If still insecure, report failing verify (pre-remediation).
    Operator can restart lab with LAB_SECURE=1 and re-run --verify-only.
    """
    checks = [
        {"id": "F-001", "type": "http_get", "url": f"{base}/debug/config", "expect_not_status": 200},
        {"id": "F-002", "type": "http_get", "url": f"{base}/admin", "expect_status_in": [401, 403]},
        {
            "id": "F-003",
            "type": "http_header",
            "url": f"{base}/health",
            "header": "access-control-allow-origin",
            "expect_not_equals": "*",
        },
    ]
    results = []
    for c in checks:
        r = run_check(c, scope)
        results.append({"finding_id": c["id"], **r})
    passed = all(r.get("ok") for r in results)
    return {
        "generated_at": utc_now(),
        "secure_lab_expected": secure_assumed,
        "passed": passed,
        "results": results,
        "next_step": (
            "All checks green — remediation verified."
            if passed
            else "Restart lab with LAB_SECURE=1 and re-run: python run_cycle.py --verify-only"
        ),
    }


def write_artifacts(
    findings: list[dict[str, Any]],
    remediations: list[dict[str, Any]],
    verify: dict[str, Any],
) -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    rem_dir = ARTIFACTS / "remediations"
    rem_dir.mkdir(exist_ok=True)

    findings_doc = {
        "generated_at": utc_now(),
        "role": "adversary",
        "model_story": "Claude (stub)",
        "findings": findings,
    }
    (ARTIFACTS / "findings.json").write_text(json.dumps(findings_doc, indent=2))

    for rem in remediations:
        fid = rem["finding_id"]
        (rem_dir / f"{fid}.diff").write_text(rem["diff"])
        (rem_dir / f"{fid}.json").write_text(json.dumps(rem, indent=2))
        for rel, content in rem.get("files", {}).items():
            path = rem_dir / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            # append-safe single hardening file
            existing = path.read_text() if path.exists() else ""
            if content not in existing:
                path.write_text(existing + ("\n" if existing else "") + content)

    (ARTIFACTS / "verify.json").write_text(json.dumps(verify, indent=2))

    summary = {
        "generated_at": utc_now(),
        "confirmed_findings": sum(1 for f in findings if f.get("confirmed")),
        "remediations": len(remediations),
        "verify_passed": verify.get("passed"),
    }
    (ARTIFACTS / "summary.json").write_text(json.dumps(summary, indent=2))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OSC Attack → Defend cycle")
    p.add_argument("--target", default="lab", choices=["lab"])
    p.add_argument("--mode", default="stub", choices=["stub", "claude", "codex", "hybrid"])
    p.add_argument("--base-url", default="http://127.0.0.1:8080")
    p.add_argument("--scope", type=Path, default=SCOPE_DEFAULT)
    p.add_argument("--verify-only", action="store_true", help="Only run post-remediation checks")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    scope = load_scope(args.scope)
    base = args.base_url.rstrip("/")

    if args.verify_only:
        verify = verify_expectations(scope, base, secure_assumed=True)
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        (ARTIFACTS / "verify.json").write_text(json.dumps(verify, indent=2))
        print(json.dumps(verify, indent=2))
        return 0 if verify["passed"] else 1

    # Red
    if args.mode in ("stub", "codex"):
        findings = red_stub(scope, base)
    elif args.mode in ("claude", "hybrid"):
        findings = red_claude_live(scope, base)
    else:
        findings = red_stub(scope, base)

    try:
        findings = validate_findings(findings, scope)
    except PermissionError as e:
        print(f"Scope violation: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(
            f"Could not reach lab at {base}. Start it with: "
            f"python demo/lab-app/server.py\nError: {e}",
            file=sys.stderr,
        )
        return 2

    confirmed = [f for f in findings if f.get("confirmed")]

    # Blue
    if args.mode in ("stub", "claude"):
        remediations = blue_stub(confirmed)
    elif args.mode in ("codex", "hybrid"):
        remediations = blue_codex_live(confirmed)
    else:
        remediations = blue_stub(confirmed)

    verify = verify_expectations(scope, base, secure_assumed=False)
    write_artifacts(findings, remediations, verify)

    print("=== OSC Attack → Defend cycle complete ===")
    print(f"Confirmed findings: {len(confirmed)}")
    print(f"Remediations drafted: {len(remediations)}")
    print(f"Verify passed (current lab): {verify['passed']}")
    print(f"Artifacts: {ARTIFACTS}")
    if not verify["passed"]:
        print("Tip: LAB_SECURE=1 python demo/lab-app/server.py  then  python run_cycle.py --verify-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
