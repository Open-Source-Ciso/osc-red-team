# OSC Red Team — Attack → Defend as a Service

**Raise the bar:** continuous, AI-orchestrated adversarial assessment paired with AI-generated remediation — not another annual pen-test PDF.

This repo is the product foundation for Open Source CISO’s next-generation red team offering: **Claude plans and prosecutes authorized adversarial hypotheses; Codex closes the loop with patches, detections, and verification.**

| Role | Model | Job |
|------|--------|-----|
| Adversary (Red) | Claude | Threat model, hypothesize, map MITRE, score business risk, propose *authorized* validation checks |
| Defender (Blue) | Codex | Generate remediations, hardening, detections, regression tests; verify the fix |
| Orchestrator | This platform | Scope control, evidence, human gates, reporting, continuous re-test |

> **Scope & ethics:** Engagements are always customer-authorized. The platform does not ship exploit payloads, malware, or unauthorized-access tooling. Validation is detection-, config-, and control-oriented against agreed lab and production scopes.

## Why this, why now

Customers already buy point-in-time red teams. What they struggle to buy — and what will stay in demand — is:

1. **Speed** — findings in days, not quarters, as AI and app surface area change weekly  
2. **Closure** — a fix and a re-test, not a ticket dump  
3. **AI surface** — agents, MCP, RAG, and copilots need adversarial coverage traditional pen tests miss  
4. **Evidence** — board/regulator-ready trails mapped to MITRE, OWASP, NIST AI RMF  

Competitors (Giskard, Adversa, AccuKnox, DeepTeam, etc.) mostly sell **AI-system** red teaming. Our wedge: **full-stack purple team + closed-loop remediation**, with dual-model asymmetry so the attacker does not grade its own fixes.

## Quick start (demo)

```bash
# 1. Run the intentionally misconfigured lab app (authorized demo target)
cd demo/lab-app && python -m http.server 8080 &

# 2. Run one Attack → Defend cycle against the lab (offline stubs; no API keys required)
cd demo/orchestrator
python run_cycle.py --target lab --mode stub
```

Artifacts land in `demo/artifacts/` (findings, remediations, verification report).

See [docs/DEMO_NARRATIVE.md](docs/DEMO_NARRATIVE.md) for the company pitch walkthrough.

## Docs

| Doc | Purpose |
|-----|---------|
| [Product vision](docs/PRODUCT_VISION.md) | Market, positioning, demand thesis |
| [Service catalog](docs/SERVICE_CATALOG.md) | Packages you can sell tomorrow |
| [Architecture](docs/ARCHITECTURE.md) | Claude / Codex dual-agent design |
| [Demo narrative](docs/DEMO_NARRATIVE.md) | 15-minute internal / customer demo script |
| [Roadmap](docs/ROADMAP.md) | Forward-looking capability plan |
| [One-pager](docs/ONE_PAGER.md) | Internal / sales leave-behind |

## Repo layout

```
docs/                 Product + service design
demo/
  lab-app/            Authorized, intentionally weak demo target
  orchestrator/       Attack → Defend cycle runner
  artifacts/          Generated findings & remediations
```

## Principles

- **Human-gated** on anything that touches production or live credentials  
- **Dual-model asymmetry** — Claude attacks; Codex defends; neither self-grades alone  
- **Evidence over theater** — every finding ties to risk, control gap, and a verifiable fix  
- **Continuous by default** — re-run after change; treat red team as a pipeline, not an event  
