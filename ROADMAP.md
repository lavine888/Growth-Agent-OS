# Roadmap

## V0.2 — foundation (current)

- [x] explicit agent organization
- [x] shared business context layout
- [x] configurable ordered funnel
- [x] JSONL product event contract
- [x] funnel report + bottleneck detection
- [x] deterministic owner assignment
- [x] CI smoke tests

## V0.3 — adapters

- [ ] generic HTTP event ingestion
- [ ] GA4 / web analytics read adapter
- [ ] CRM read adapter
- [ ] CSV import adapter
- [ ] product-runtime webhook adapter
- [ ] normalized lead and experiment schemas

## V0.4 — experiment engine

- [ ] hypothesis registry
- [ ] experiment lifecycle: proposed → approved → running → concluded
- [ ] exposure tracking
- [ ] success / guardrail metrics
- [ ] experiment memory and learnings
- [ ] weekly growth review artifact

## V0.5 — LLM execution layer

- [ ] provider-neutral model interface
- [ ] Growth Director planning
- [ ] Strategist hypothesis generation
- [ ] Analyst narrative explanation
- [ ] Content brief / variant generation
- [ ] lead qualification and personalization
- [ ] token / latency / cost tracing

## V0.6 — action + approval layer

- [ ] durable approval queue
- [ ] content publishing adapters
- [ ] outbound messaging adapters
- [ ] CRM mutations
- [ ] budget limits and kill switches
- [ ] idempotency + retry policy
- [ ] audit log

## V1 — closed-loop growth system

A user can define a business goal and constraints, ingest real data, approve proposed experiments, execute across channels, observe product and revenue outcomes, and persist learnings into the next planning cycle.

### V1 acceptance test

```text
Goal
→ hypothesis
→ approved experiment
→ execution
→ product/revenue events
→ analysis
→ learning
→ next experiment
```

No step should depend on manually copying chat output between agents.
