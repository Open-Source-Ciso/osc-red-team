# Product Vision — OSC Attack → Defend

## One-liner

**Continuous purple-team as a service:** Claude finds what matters under authorization; Codex ships the fix and proves it closed — so customers buy outcomes, not PDFs.

## The gap we close

| What customers buy today | What fails |
|--------------------------|------------|
| Annual / quarterly pen test | Stale before the deck is presented |
| Vulnerability scanner + MSSP | Noise; no attacker narrative; weak AI coverage |
| One-off AI red team of a chatbot | Narrow; no infra/app/identity story; no remediation loop |
| Internal red team + ticket queue | Findings rot; no verified closure |

**Demand shift (2025–2026):** continuous adversarial testing, agent/MCP/RAG coverage, and **remediation that lands in the PR**, not the backlog. Boards ask “are we safe against AI-augmented attackers?” — not “when was the last pen test?”

## Positioning

**Category:** Closed-loop adversarial security (purple team + AI remediator)  
**Not:** Another CVE scanner, another LLM jailbreak SaaS, another pen-test firm with a chatbot skin  

**Wedge vs pure AI-red-team vendors:** They stress-test models and agents. We stress-test the **business attack surface** (apps, identity, cloud, AI stack) and **close the loop** with Codex-generated remediations under human review.

**Wedge vs classic red team firms:** Same human craft where it matters (scope, abuse cases, executive narrative) — multiplied by dual agents for hypothesizing, mapping, patching, and re-test cadence.

## Dual-agent thesis (Claude attack / Codex defend)

Independent models outperform single-model “red team itself then fix itself”:

1. **Claude (adversary)** — strong at multi-step reasoning, threat modeling, narrative risk, MITRE mapping, asking uncomfortable “what if” questions within scope  
2. **Codex (defender)** — strong at turning a finding into concrete diffs: code, IaC, detections, tests  
3. **Orchestrator + humans** — enforce scope, authorize probes, approve production changes, own the customer relationship  

This is the product story you demo: *“Watch Claude argue like an attacker. Watch Codex open a fix PR. Watch the re-test go green.”*

## Ideal customer profile

- Mid-market → enterprise with cloud-native apps and growing AI surface  
- Has SOC / AppSec but cannot staff continuous purple team  
- Buying pressure from: board AI risk, cyber insurance, customer security questionnaires, regulated industry  
- Willing to authorize scoped continuous testing (lab + agreed prod read paths)

## Jobs to be done

1. Prove residual risk in language executives understand  
2. Shrink mean-time-to-remediate for high-severity findings  
3. Cover AI features (agents, tools, MCP) without a separate boutique engagement  
4. Produce audit-grade evidence continuously  

## Moats we can build

- **Engagement OS** — scoped orchestrator, evidence store, human gates (hard to copy overnight)  
- **Playbook library** — industry + tech-stack hypotheses that improve with every engagement  
- **Fix quality** — Codex remediations scored by re-test pass rate (outcome data competitors lack)  
- **OSC brand** — open, CISO-fluent, service + product hybrid (not pure SaaS theater)

## Non-goals (near term)

- Selling or shipping weaponized exploit kits  
- Unsupervised production exploitation  
- Replacing human judgment on high-impact findings  
- Competing only on “number of jailbreak probes”

## Success metrics (product & service)

| Metric | Target intent |
|--------|----------------|
| Time to first credible finding | Hours after scope kickoff |
| % findings with proposed remediation | ≥ 90% high/critical |
| Re-test pass rate after Codex fix | Track & publish internally |
| Repeat engagement / continuous subscription | Primary revenue motion |
| Customer NPS / expansion | Service quality + closure speed |
