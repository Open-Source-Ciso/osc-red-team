# Service Catalog — What We Sell

Packages are designed for **demo → pilot → retainer**. Lead with outcomes (risk reduced, fixes verified), not hours burned.

## Tier 0 — Executive Demo (internal / pre-sales)

**Duration:** 1–2 hours  
**Deliverable:** Live Attack → Defend cycle on the OSC lab (this repo)  
**Purpose:** Win internal buy-in; seed customer conversations  

Includes: Claude-style adversarial brief, Codex-style remediation PR, verification report, positioning talk track ([DEMO_NARRATIVE.md](DEMO_NARRATIVE.md)).

---

## Tier 1 — AI Purple Team Sprint

**Duration:** 2-week engagement  
**Best for:** First paid pilot  

| Phase | What happens |
|-------|----------------|
| Scope & threat model | Assets, abuse cases, AI surfaces, out-of-bounds |
| Adversarial campaign | Claude-assisted hypotheses + authorized validation |
| Remediation pack | Codex-assisted patches, detections, hardening |
| Re-test & readout | Verified closure + residual risk for execs |

**Outputs:** Findings board, MITRE map, remediation PRs/patches, detection suggestions, residual risk memo.

**Pricing posture:** Fixed fee pilot; conversion credit toward retainer.

---

## Tier 2 — Continuous Attack → Defend (Retainer)

**Cadence:** Monthly adversarial cycles + always-on CI hooks where agreed  

| Included | Detail |
|----------|--------|
| Continuous hypothesizing | New features, cloud changes, AI agent updates |
| Closed-loop remediations | Codex drafts; customer AppSec approves |
| Re-test automation | Orchestrator re-runs scoped checks |
| Quarterly exec brief | Risk trend, top open paths, AI surface growth |
| On-call purple consult | Bounded hours for incident / launch support |

**This is the productized service customers will renew** — annual pen tests become a subset, not the product.

---

## Tier 3 — AI Stack Adversarial Add-on

Bolt onto Tier 1 or 2 when the customer ships LLMs / agents / MCP / RAG.

Coverage themes (authorized, policy-aligned):

- Prompt injection & tool-abuse *resilience testing* (against customer-owned endpoints)  
- Over-privileged tool / MCP permission review  
- Data exfil paths via retrieval & connectors  
- Guardrail bypass *detection gaps* (not payload catalogs)  
- Mapping to OWASP LLM / Agentic Top 10 & NIST AI RMF evidence packs  

---

## Tier 4 — Board & Assurance Pack

For CISOs who need evidence, not just fixes:

- Continuous control evidence export  
- Insurance / customer questionnaire support pack  
- Tabletop: “AI-augmented attacker vs our SOC”  
- Comparison baseline: last classic pen test vs current Attack → Defend posture  

---

## Packaging tips for the company pitch

1. **Sell Tier 2** as the north star; use Tier 1 as the on-ramp.  
2. Demo Tier 0 every sales call — *see a fix land*.  
3. Price on **closure and coverage**, not raw finding count (finding inflation destroys trust).  
4. Keep a clear **human gate** story for legal / risk committees.  
5. Offer a **lab-first** path for cautious buyers; expand scope after first re-test wins.

## What we explicitly do not sell

- Exploit kits, zero-days, or unattended production exploitation  
- “Guaranteed breach” theater without authorized scope  
- Dark-web access or illegal data acquisition as a service  
