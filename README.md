# Growth Agent OS

> An open-source operating system for agentic growth: research → strategy → content → distribution → leads → experiments → learning.

Growth Agent OS is an experimental framework for building a small AI-native growth team instead of a single marketing chatbot.

## Why this exists

Most "marketing agents" are prompt wrappers around content generation. Growth Agent OS starts one level higher: shared business context, explicit agent roles, measurable experiments, work-item state, human approval boundaries, and a feedback loop.

```text
Goal
  ↓
Research → Strategy → Execute → Measure → Learn
   ↑                                  ↓
   └──────────── next experiment ─────┘
```

## v0.1 foundation

Six roles are modeled explicitly:

- **Growth Manager** — goals, prioritization, experiments, handoffs
- **Researcher** — ICP, market, competitors, channel evidence
- **Content Strategist** — campaign hypotheses and content systems
- **Content Producer** — channel-specific drafts and creative assets
- **Acquisition Agent** — distribution, outreach, lead generation
- **Analyst** — measurement, experiment evaluation, next-step learning

These are roles, not six permanently running processes. A runtime may map several roles to one model, or one role to multiple workers.

## Safety boundary

Growth Agent OS separates reasoning from side effects. External publishing, outbound sending, campaign launch, and spend should require an approval policy. v0.1 marks likely side-effecting work as `blocked_for_approval` rather than executing it.

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/lavine888/Growth-Agent-OS.git
cd Growth-Agent-OS
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -e .
growth-os config/example_business.json
```

Or run without installing the console command:

```bash
python -m growth_agent_os.cli config/example_business.json
```

Write the generated plan to a file:

```bash
growth-os config/example_business.json --out output/plan.json
```

Run the current test suite:

```bash
python -m unittest discover -s tests
```

## Repository structure

```text
Growth-Agent-OS/
├── config/
│   └── example_business.json
├── docs/
│   └── ARCHITECTURE.md
├── growth_agent_os/
│   ├── __init__.py
│   ├── agents.py
│   ├── cli.py
│   ├── models.py
│   └── orchestrator.py
├── tests/
│   └── test_orchestrator.py
├── pyproject.toml
└── README.md
```

## Architecture

The core domain model is intentionally provider-agnostic:

```text
Business Context
      ↓
Growth Orchestrator
      ↓
Agents + Experiments + Work Items
      ↓
Approval Policy
      ↓
Tool Adapters
  ├─ Search / Browser
  ├─ LLM Provider
  ├─ Content Publisher
  ├─ CRM / Lead Store
  ├─ Analytics
  └─ n8n / MCP / other runtimes
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for design decisions and extension boundaries.

## What comes next

The useful next milestone is not "more agents". It is connecting this operating model to real evidence and state:

1. persistent business/experiment memory;
2. LLM and search adapters;
3. structured research evidence;
4. approval queue;
5. CRM/lead store;
6. analytics snapshots and experiment evaluation;
7. n8n/MCP integrations for real workflows.

## Design principles

1. Shared context before autonomous action.
2. Every action maps to a measurable growth hypothesis.
3. Human approval for external publishing, outreach, and spend.
4. Structured outputs over opaque chat logs.
5. Learning is persisted and reused by the next cycle.
6. LLM providers and channel APIs stay behind adapters.

## Status

**v0.1 foundation — experimental.** The current implementation produces a deterministic growth plan. It does not yet call an LLM or perform external actions.

## License

License to be defined before the first public release.
