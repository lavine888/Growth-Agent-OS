# Growth Agent OS

> An open-source operating system for AI-native growth teams: **goal → experiment → acquire → activate → convert → retain → learn**.

Growth Agent OS is not another marketing chatbot. It is a control plane for running measurable growth loops with multiple agents, shared business context, first-party product events, experiments, adapters, and human approval gates.

This repository is a V2 rebuild around four ideas:

1. **Organization layer** — inspired by OpenSoul's multi-agent operating model.
2. **Context + measurement layer** — inspired by Growth OS's persistent marketing context and adapters.
3. **Acquisition execution layer** — inspired by AI-SDR style prospecting, qualification, outreach, and follow-up pipelines.
4. **Product event layer** — first-party activation, conversion, and retention events so the system optimizes for customers, not vanity traffic.

No source code is copied from those projects; the architecture is an independent implementation.

## Why this exists

Most “growth agents” stop at content generation or outbound automation. That creates activity, not a growth system.

Growth Agent OS treats growth as a closed-loop control problem:

```text
                         Human owner
                    strategy / approvals
                           │
                   ┌───────▼────────┐
                   │ Growth Director │
                   └───────┬────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    Acquisition       Activation        Retention
       Agents            Agents            Agents
          │                │                │
          └────────────────┼────────────────┘
                           │
                  Shared Growth Context
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       Channel          Product           CRM / Sales
        data             events              data
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                      Analyst Agent
                           │
                    next experiment
                           └──────────────↺
```

## V0.3: execution substrate

The system now has a deterministic execution substrate before LLM autonomy is introduced:

- explicit agent roles and ownership;
- shared product / ICP / positioning / metric context;
- canonical first-party product event contract;
- ordered funnel conversion and bottleneck analysis;
- event adapter interface for external systems;
- append-only JSONL ingestion;
- experiment lifecycle (`draft → running → paused/completed`);
- approval queue for external mutations;
- deterministic owner / next-action planner;
- CI unit and CLI smoke tests.

The point is to make LLMs replaceable execution engines rather than the system of record.

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/lavine888/Growth-Agent-OS.git
cd Growth-Agent-OS
python -m pip install -e .

growth-os agents
growth-os report examples/events.jsonl
growth-os plan examples/events.jsonl
```

Ingest a new product event:

```bash
cat > /tmp/event.json <<'JSON'
{
  "actor_id": "family_101",
  "event": "trial_booked",
  "source": "landing_page",
  "properties": {"campaign": "minecraft_demo"}
}
JSON

growth-os ingest /tmp/event.json --out data/events.jsonl
```

## Repository layout

```text
Growth-Agent-OS/
├── config/
│   ├── agents.json          # roles, ownership, approval rules
│   └── funnel.json          # ordered growth funnel
├── context/
│   ├── product.md           # what the product is
│   ├── icp.md               # buyer / user / qualification model
│   ├── positioning.md       # value proposition and messaging boundaries
│   └── metrics.md           # north-star + guardrail metrics
├── examples/
│   └── events.jsonl         # first-party event example
├── src/growth_agent_os/
│   ├── adapters.py          # external system → canonical Event boundary
│   ├── approvals.py         # human approval queue
│   ├── cli.py               # local control plane
│   ├── experiments.py       # experiment lifecycle
│   ├── ingestion.py         # append-only event ingestion
│   ├── metrics.py           # funnel analytics
│   ├── models.py            # canonical data models
│   └── orchestrator.py      # planning / ownership logic
├── tests/
├── ARCHITECTURE.md
└── ROADMAP.md
```

## Default agent organization

| Agent | Owns | Typical outputs |
|---|---|---|
| Growth Director | goals, prioritization, handoffs | weekly growth plan, experiment queue |
| Strategist | ICP, positioning, hypotheses | testable growth hypotheses |
| Content | organic creative and campaign assets | briefs, drafts, variants |
| Acquisition | distribution, partnerships, outbound | qualified leads, channel actions |
| Activation | onboarding and first-value experience | activation fixes, trial ops |
| Revenue | trial-to-paid conversion | offer / follow-up experiments |
| Retention | repeat use and referral | retention / referral experiments |
| Analyst | event data and experiment evaluation | funnel report, next-step recommendation |

## Event contract

One line per canonical event:

```json
{"actor_id":"family_001","event":"trial_attended","timestamp":"2026-09-02T09:30:00Z","source":"offline_demo","properties":{"lesson":"lesson_01"}}
```

The default product-centric funnel is configurable:

```text
lead_created
→ trial_booked
→ trial_attended
→ first_valid_speech
→ lesson_completed
→ parent_report_viewed
→ purchase_completed
→ lesson_2_booked
```

For another product, replace the funnel configuration and adapters without changing the analytics engine.

## Adapter contract

External sources should not leak vendor-specific schemas into the core. Each integration normalizes upstream data into the canonical `Event` model:

```text
Minecraft Runtime ─┐
CRM / Sales ───────┼─> EventAdapter ─> Event Store ─> Funnel / Experiment Engine
Website / GA4 ─────┘
```

The included `MappingAdapter` is intentionally small. Concrete adapters for Minecraft Runtime, CRM and analytics systems should live behind the same interface.

## Human approval boundary

Read, analyze, plan and draft operations can be automated. External mutations should enter the approval queue first, including:

- publishing content;
- outbound messages;
- ad spend;
- pricing changes;
- CRM destructive writes;
- any action with material reputational or financial impact.

## Design principles

1. **Shared context before autonomous action.**
2. **Every action maps to a measurable hypothesis.**
3. **Product events outrank vanity metrics.**
4. **Read/analyze by default; external writes require approval.**
5. **Agents have explicit owners, inputs, outputs, and boundaries.**
6. **Structured artifacts beat opaque chat history.**
7. **Persist learning so the next cycle starts smarter.**
8. **LLMs are replaceable execution engines, not the system of record.**

## Next

The next milestone is **V0.4: real adapters + experiment persistence**:

1. Minecraft Runtime webhook adapter;
2. website / analytics adapter;
3. CRM lead adapter;
4. persistent experiment store;
5. approval persistence and audit log;
6. LLM provider interface after the deterministic control plane is stable.

## Status

Experimental / pre-alpha. Interfaces will change quickly while the first end-to-end growth loop is validated.

## License

A project license has not yet been selected. Do not assume permission beyond GitHub's default repository rights.
