# Architecture — Claude Attack / Codex Defend

## Design goals

1. **Asymmetry** — adversary and defender are different models/providers  
2. **Authorization** — every probe is scoped; production actions are human-gated  
3. **Evidence** — artifacts are first-class (findings, diffs, verify reports)  
4. **Swappable providers** — stub mode for demos; live Claude/Codex when keys exist  
5. **Safe by default** — no exploit payload generation in the platform path  

## Logical flow

```
┌─────────────┐     scope + assets      ┌──────────────────┐
│  Customer   │ ───────────────────────▶│   Orchestrator   │
│  Scope Gate │◀── approve / reject ────│  (this platform) │
└─────────────┘                         └────────┬─────────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    ▼                            ▼                            ▼
           ┌────────────────┐          ┌────────────────┐          ┌────────────────┐
           │  Claude Red    │          │  Evidence Store│          │  Codex Blue    │
           │  • threat model│─────────▶│  findings.json │─────────▶│  • patches     │
           │  • hypotheses  │          │  remediations/ │          │  • detections  │
           │  • risk score  │          │  verify.json   │◀─────────│  • verify tests│
           │  • MITRE map   │          └────────────────┘          └────────────────┘
           └────────────────┘
                    │
                    ▼
           Authorized validators
           (config/control checks
            against agreed targets)
```

## Components

### Orchestrator (`demo/orchestrator`)

- Loads scope (in-bounds assets, forbidden actions)  
- Invokes **Red provider** → structured findings  
- Invokes **Blue provider** → remediations per finding  
- Runs **verification** (static checks / tests against lab)  
- Writes artifacts under `demo/artifacts/`  

### Red provider (Claude)

**Inputs:** scope, asset inventory, prior findings, playbook library  
**Outputs (structured JSON):**

```json
{
  "id": "F-001",
  "title": "Public debug endpoint exposes internal config",
  "severity": "high",
  "mitre": ["T1082"],
  "hypothesis": "...",
  "business_risk": "...",
  "authorized_check": {
    "type": "http_get",
    "path": "/debug/config",
    "expect_not_status": 200
  },
  "detection_gap": "No alert on sensitive path access"
}
```

Red proposes **checks**, not payloads. Checks are allowlisted types: HTTP status/header assertions, config key presence, IAM policy shape, dependency CVE *lookup* via advisory DBs, etc.

### Blue provider (Codex)

**Inputs:** finding + relevant source/config snippets  
**Outputs:**

- Unified diff or file replacements  
- Optional detection rule (Sigma / cloud query sketch)  
- Verification test the orchestrator can run  

### Human gates

| Action | Gate |
|--------|------|
| Expand scope | Customer + OSC lead |
| Touch production | Explicit ticket + approval |
| Apply remediations | Customer AppSec / platform owner |
| Publish external report | OSC engagement lead |

## Provider modes

| Mode | Behavior |
|------|----------|
| `stub` | Deterministic offline demo (no API keys) |
| `claude` | Live Anthropic API for red (when configured) |
| `codex` | Live OpenAI Codex / code model for blue (when configured) |
| `hybrid` | Live red + live blue |

Stub mode is what you run in the company demo so the story never depends on credentials.

## Security & compliance controls (platform)

- Scope file is mandatory; out-of-scope hosts rejected  
- Allowlisted check types only  
- Secrets never logged into artifacts (redaction filter)  
- Full audit log of model prompts/responses retained per engagement policy  
- Customer data residency options on retainer tier  

## Extension points (roadmap-ready)

- CI plugin: fail PR if high finding lacks remediation plan  
- SIEM export of detection suggestions  
- Playbook packs per vertical (fintech, health, SaaS)  
- Multi-agent debate: second red model challenges first (quality bar)  
