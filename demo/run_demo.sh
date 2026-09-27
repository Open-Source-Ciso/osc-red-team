#!/usr/bin/env bash
# One-shot Attack → Defend demo for junior developers.
# Usage (from repo root): ./demo/run_demo.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAB="$ROOT/demo/lab-app/server.py"
ORCH="$ROOT/demo/orchestrator/run_cycle.py"
PORT="${LAB_PORT:-8080}"
BASE="http://127.0.0.1:${PORT}"
LAB_PID=""

cleanup() {
  if [[ -n "${LAB_PID}" ]] && kill -0 "${LAB_PID}" 2>/dev/null; then
    kill "${LAB_PID}" 2>/dev/null || true
    wait "${LAB_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need python3

if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
  echo "Python 3.10+ required. Found: $(python3 --version)" >&2
  exit 1
fi

echo "==> [1/4] Starting INSECURE lab on ${BASE}"
LAB_SECURE=0 LAB_PORT="${PORT}" python3 "${LAB}" >/tmp/osc-lab-insecure.log 2>&1 &
LAB_PID=$!
sleep 1

if ! curl -sf "${BASE}/health" >/dev/null; then
  echo "Lab failed to start. See /tmp/osc-lab-insecure.log" >&2
  cat /tmp/osc-lab-insecure.log >&2 || true
  exit 1
fi

echo "==> [2/4] Running Attack → Defend cycle (stub)"
python3 "${ORCH}" --target lab --mode stub --base-url "${BASE}"

echo "==> [3/4] Restarting lab in SECURE mode"
kill "${LAB_PID}"
wait "${LAB_PID}" 2>/dev/null || true
LAB_PID=""
sleep 1

LAB_SECURE=1 LAB_PORT="${PORT}" python3 "${LAB}" >/tmp/osc-lab-secure.log 2>&1 &
LAB_PID=$!
sleep 1

echo "==> [4/4] Verifying remediations"
python3 "${ORCH}" --verify-only --base-url "${BASE}"

echo
echo "Done. Inspect:"
echo "  ${ROOT}/demo/artifacts/findings.json"
echo "  ${ROOT}/demo/artifacts/remediations/"
echo "  ${ROOT}/demo/artifacts/verify.json"
echo
echo "Talk track: docs/DEMO_NARRATIVE.md"
echo "Full guide: docs/RUN_THE_DEMO.md"
