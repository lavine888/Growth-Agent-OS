# Architecture

## 1. System boundary

Growth Agent OS separates four concerns that are commonly mixed together in agent projects:

- **Control plane** — goals, roles, delegation, approvals.
- **Context plane** — product truth, ICP, positioning, metrics, experiment history.
- **Execution plane** — content, acquisition, activation, revenue, retention actions.
- **Measurement plane** — channel, product, CRM, and revenue events.

The core rule is that execution is downstream of context and measurement.

## 2. Reference architecture

```text
Human Owner
   │
   ├── goals / constraints / approval
   ▼
Growth Director
   │
   ├── Strategist
   ├── Content
   ├── Acquisition
   ├── Activation
   ├── Revenue
   ├── Retention
   └── Analyst
           │
           ▼
      Experiment Queue
           │
           ▼
      Action Adapters
           │
   ┌───────┼────────┐
   ▼       ▼        ▼
Channels Product   CRM
   │       │        │
   └───────┼────────┘
           ▼
        Events
           │
           ▼
      Funnel / Cohort
           │
           ▼
       Learning Log
           └────────→ next planning cycle
```

## 3. Why deterministic core first

The first implementation deliberately does not require an LLM. Funnel state, experiment IDs, approvals, budgets, and event attribution must remain deterministic and auditable.

LLMs will later operate behind interfaces such as:

```text
StrategyProvider.generate_hypotheses(context, evidence)
ContentProvider.create_variants(brief)
AcquisitionProvider.rank_leads(records, icp)
AnalystProvider.explain(report, experiments)
```

Replacing one model provider must not invalidate stored data or workflow state.

## 4. Agent contract

Every agent definition should include:

- `mission`
- `owns`
- `inputs`
- `outputs`
- `approval_required_for`
- `success_metrics`

Agents should not share an unrestricted mutable scratchpad. Durable learning belongs in structured context or experiment artifacts.

## 5. Event model

Required fields:

```json
{
  "actor_id": "stable pseudonymous identifier",
  "event": "canonical_event_name",
  "timestamp": "ISO-8601 timestamp",
  "source": "acquisition or system source",
  "properties": {}
}
```

Avoid storing secrets or unnecessary personal information in growth events. Use pseudonymous IDs and keep identity mapping in the source system.

## 6. Funnel semantics

The current funnel implementation is **ordered**: a user only counts at step N if the preceding steps have appeared first for that actor in the event stream. This avoids counting out-of-order analytics noise as real conversion.

Future work:

- event-time ordering and late-arriving events;
- cohort windows;
- multi-touch attribution;
- experiment exposure events;
- revenue and CAC/LTV calculations;
- warehouse adapters.

## 7. Approval model

Default policy:

**Auto:** read data, calculate metrics, draft plans, generate internal artifacts.

**Approval required:** publish content, send outreach, spend money, change pricing, mutate CRM records, contact minors/consumers, or execute destructive actions.

This boundary is a product feature, not a prompt convention.

## 8. Inspiration vs implementation

The architecture borrows patterns from multi-agent marketing organizations, shared-context marketing systems, and AI-SDR pipelines. The implementation in this repository is independent and is intended to combine those patterns with first-party product analytics.
