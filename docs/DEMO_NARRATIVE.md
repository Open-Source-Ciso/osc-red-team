# Demo Narrative — 15 Minutes to Raise the Bar

Use this script for internal leadership and customer pre-sales. Run in **stub mode** so nothing depends on API keys.

## Setup (2 min before)

```bash
cd demo/lab-app && python3 server.py &
cd demo/orchestrator && python3 run_cycle.py --target lab --mode stub
```

Have three screens ready:

1. Lab “broken” app behavior (browser or curl)  
2. Terminal / artifacts (`findings.json` → `remediations/` → `verify.json`)  
3. Slides or this narrative  

---

## Talk track

### 1. The problem (2 min)

> “Our industry still sells point-in-time red teams. Attackers — and now AI-assisted attackers — do not work on an annual calendar. Customers are buying continuous assurance and **verified closure**. AI-only red-team SaaS vendors mostly poke chatbots. We close the full loop: adversarial reasoning **and** remediation.”

### 2. The product idea (2 min)

> “Claude plays red: threat model, hypothesize, map MITRE, propose authorized checks. Codex plays blue: patch, harden, detect, verify. Different models on purpose — the attacker does not grade its own homework. Humans own scope and production.”

Show [ARCHITECTURE.md](ARCHITECTURE.md) diagram verbally.

### 3. Live lab (6 min)

**Before:** Show lab issues (debug endpoint, permissive CORS, secret in config).

**Run cycle:** Point at `demo/artifacts/`:

- `findings.json` — Claude-style adversarial findings with business risk  
- `remediations/*.diff` — Codex-style fixes  
- `verify.json` — re-test results  

**After:** Apply remediations (or show already-applied `lab-app` secure variant) and re-verify green.

> “This is what a sprint or retainer cycle looks like — compressed. Finding → fix → proof.”

### 4. Commercial ask (3 min)

> “We productize this as: Demo → 2-week Purple Sprint → Continuous Attack→Defend retainer, with an AI-stack add-on. We raise the bar on what OSC offers: not more PDFs — **outcomes with evidence**.”

Close with Tier 2 as the north-star SKU ([SERVICE_CATALOG.md](SERVICE_CATALOG.md)).

### 5. Objections (handle live)

| Objection | Response |
|-----------|----------|
| “AI will hallucinate vulns” | Dual-model + authorized checks + human gate; we score on re-test pass rate |
| “Legal won’t allow AI attackers” | Scoped, allowlisted validators; no exploit kits; customer authorization packet |
| “We already have a pen-test firm” | Keep them for deep immersive ops; we own continuous closure + AI surface |
| “Why Claude and Codex?” | Best-in-class asymmetric pair for reason-then-remediate; providers swappable |

---

## Demo success criteria

Audience can repeat back:

1. Continuous Attack → Defend, not annual PDF  
2. Claude red / Codex blue / human gates  
3. We sell pilots that convert to retainers  
4. Safe, authorized, evidence-first  

## Optional stretch (if time)

Show how a new playbook entry would catch an AI-agent tool-overprivilege theme from the roadmap — forward-looking demand without leaving the narrative.
