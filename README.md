# Growth Agent OS

> An open-source operating system for AI-native growth teams: **goal → experiment → acquire → activate → convert → retain → learn**.

Growth Agent OS is not another marketing chatbot. It is a control plane for running measurable growth loops with multiple agents, shared business context, first-party product events, and human approval gates.

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

## V0.2: runnable foundation

The current milestone intentionally starts deterministic before adding LLM autonomy. It provides:

- explicit agent roles and ownership;
- shared product / ICP / positioning / metric context;
- an ordered product-growth funnel;
- JSONL event ingestion;
- funnel conversion analysis;
- bottleneck detection;
- a deterministic next-action planner;
- CI tests;
- approval boundaries for external actions.

This gives future LLM agents a stable operating substrate instead of letting prompts become the architecture.

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

Example output will identify the largest funnel bottleneck and assign an owner rather than simply generating more content.

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
│   ├── cli.py
│   ├── metrics.py
│   ├── models.py
│   └── orchestrator.py
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

External publishing, outreach, spend, and destructive CRM actions require human approval by default.

## Event contract

One line per event:

```json
{"actor_id":"family_001","event":"trial_attended","timestamp":"2026-09-02T09:30:00Z","source":"offline_demo","properties":{"lesson":"lesson_01"}}
```

The default funnel is configurable and intentionally product-centric:

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

Replace these events for another product without changing the core engine.

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

See [ROADMAP.md](ROADMAP.md). The next engineering milestone is the adapter layer: website analytics, CRM, content channels, and product-runtime events, followed by an LLM provider interface and approval queue.

## Status

Experimental / pre-alpha. Interfaces will change quickly while the first end-to-end growth loop is validated.

## License

A project license has not yet been selected. Do not assume permission beyond GitHub's default repository rights.
