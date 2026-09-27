# Run the Demo — Junior Developer Guide

Follow these steps on your laptop. You do **not** need Claude, Codex, or any API keys for this stub demo.

**Time:** ~10 minutes  
**You need:** `git`, `python3` (3.10+), and a terminal. Optional: `curl` or a browser.

---

## 0. What you are running

| Piece | Role |
|-------|------|
| `demo/lab-app/server.py` | Fake “customer” app with intentional security mistakes |
| `demo/orchestrator/run_cycle.py` | Attack → Defend cycle (stub Claude + stub Codex) |
| `demo/artifacts/` | Output: findings, remediations, verify report |

Flow: **broken lab → find issues → draft fixes → restart lab hardened → verify green.**

---

## 1. Get the code

```bash
git clone https://github.com/Open-Source-Ciso/osc-red-team.git
cd osc-red-team
```

Use the branch that has the demo (if you were pointed at the PR):

```bash
git fetch origin
git checkout cursor/ai-attack-defend-product-a087
```

If that branch is already merged to `main`, `git checkout main` is enough.

Check Python:

```bash
python3 --version
# Expect 3.10 or newer
```

No `pip install` — the demo uses only the Python standard library.

---

## 2. Open two terminals

Work from the **repo root** (`osc-red-team/`) in both.

- **Terminal A** — lab app (keep this one running)  
- **Terminal B** — orchestrator + inspection commands  

---

## 3. Start the insecure lab (Terminal A)

```bash
cd demo/lab-app
python3 server.py
```

You should see:

```text
OSC lab listening on http://127.0.0.1:8080  mode=INSECURE (demo findings expected)
```

Leave this process running. Do not close Terminal A yet.

**Sanity check** (Terminal B or a browser):

```bash
curl -s http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8080/debug/config
curl -s http://127.0.0.1:8080/admin
```

Insecure mode should show debug config (including a fake API key) and an unauthenticated admin response.

---

## 4. Run one Attack → Defend cycle (Terminal B)

From the **repo root**:

```bash
cd demo/orchestrator
python3 run_cycle.py --target lab --mode stub
```

Expected console output (roughly):

```text
=== OSC Attack → Defend cycle complete ===
Confirmed findings: 3
Remediations drafted: 3
Verify passed (current lab): False
Artifacts: .../demo/artifacts
Tip: LAB_SECURE=1 python demo/lab-app/server.py  then  python run_cycle.py --verify-only
```

`Verify passed: False` is **correct** here — the lab is still insecure.

---

## 5. Inspect the artifacts (Terminal B)

From the repo root:

```bash
cd ../..   # back to repo root if you were in demo/orchestrator
ls demo/artifacts/
ls demo/artifacts/remediations/
```

Open these files in your editor (or `cat` / `less`):

| File | What it shows |
|------|----------------|
| `demo/artifacts/findings.json` | “Claude red” findings (risk, MITRE, checks) |
| `demo/artifacts/remediations/F-001.json` (and F-002, F-003) | “Codex blue” fix proposals |
| `demo/artifacts/remediations/*.diff` | Short patch sketches |
| `demo/artifacts/verify.json` | Re-test against the *current* lab (should still fail) |
| `demo/artifacts/summary.json` | One-line counts |

Optional — skim a finding:

```bash
python3 -m json.tool demo/artifacts/findings.json | less
```

---

## 6. “Apply the fix” — restart the lab in secure mode

In **Terminal A**, stop the insecure lab:

- Press `Ctrl+C`

Then start the hardened lab (same terminal):

```bash
# still in demo/lab-app, or: cd path/to/osc-red-team/demo/lab-app
LAB_SECURE=1 python3 server.py
```

You should see:

```text
OSC lab listening on http://127.0.0.1:8080  mode=SECURE
```

Quick check (Terminal B):

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/debug/config   # expect 404
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/admin          # expect 401
```

---

## 7. Re-verify (Terminal B)

From `demo/orchestrator` (or use the path below from repo root):

```bash
python3 demo/orchestrator/run_cycle.py --verify-only
```

Expected: `"passed": true` and all three checks `ok: true`.

That is the full story: **find → remediate → prove closed.**

---

## 8. Shut down

In Terminal A: `Ctrl+C` to stop the lab.

Artifacts under `demo/artifacts/` are local outputs (gitignored). Safe to delete anytime:

```bash
rm -rf demo/artifacts/findings.json demo/artifacts/summary.json demo/artifacts/verify.json demo/artifacts/remediations
```

---

## One-shot helper (optional)

From the repo root, if you prefer a single script:

```bash
chmod +x demo/run_demo.sh
./demo/run_demo.sh
```

This starts the insecure lab, runs the cycle, restarts secure, verifies, then stops the lab. Read the printed paths when it finishes.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Address already in use` on 8080 | Something else is on that port. Stop it, or run `LAB_PORT=8081 python3 server.py` and `python3 run_cycle.py --base-url http://127.0.0.1:8081 --mode stub` |
| `Could not reach lab` | Lab is not running, or wrong URL. Confirm Terminal A shows “listening…” and retry |
| `command not found: python3` | Install Python 3, or try `python` if that is 3.x on your machine |
| Verify still fails after `LAB_SECURE=1` | Old insecure process still bound to 8080. Kill it (`Ctrl+C` / Activity Monitor) and start secure again |
| Wrong branch / missing `demo/` | `git checkout cursor/ai-attack-defend-product-a087` (or updated `main`) and confirm `ls demo/lab-app/server.py` |
| Windows | Use PowerShell/WSL; set env as `$env:LAB_SECURE=1` before `python server.py` (WSL/mac/Linux form above is preferred) |

---

## What you do *not* need for this demo

- Anthropic or OpenAI API keys (`--mode stub` is offline)  
- Docker  
- Node / npm  
- Any cloud account  

Live Claude/Codex modes are placeholders for later pilots — ignore `--mode claude` / `codex` / `hybrid` for now.

---

## After it works — optional reading

1. [DEMO_NARRATIVE.md](DEMO_NARRATIVE.md) — how to talk through it in a meeting  
2. [ARCHITECTURE.md](ARCHITECTURE.md) — how Claude / Codex fit the product  
3. [SERVICE_CATALOG.md](SERVICE_CATALOG.md) — what we sell around this loop  

If anything in this guide fails on your machine, note the OS, Python version, and the exact error text and bring that back.
