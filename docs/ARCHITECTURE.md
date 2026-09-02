# Architecture

## 1. Scope of v0.1

Growth Agent OS separates the **growth operating model** from any specific LLM, browser, CRM, social platform, or workflow engine.

The foundation has four layers:

```text
Business Context
      ↓
Growth Orchestrator
      ↓
Agent Roles + Experiments + Work Items
      ↓
Approval / Tool Adapters (next milestone)
```

The core is deliberately deterministic. LLMs should help agents reason and create artifacts, but they should not define the system's state model.

## 2. Domain model

### BusinessContext
Persistent source of truth for product, goal, ICP, channels, constraints, and metrics.

### Experiment
Every growth cycle should have a falsifiable hypothesis, an owner, a primary metric, and a success criterion.

### WorkItem
The unit of execution. A work item has an owner, inputs, expected output, status, and an explicit approval requirement.

### AgentRole
v0.1 defines six roles:

1. Growth Manager
2. Researcher
3. Content Strategist
4. Content Producer
5. Acquisition Agent
6. Analyst

These are roles, not six permanently running processes. A future runtime can map multiple roles to one model or one role to multiple workers.

## 3. Safety and control boundary

Planning is safe to automate aggressively. Side effects are not.

The following actions should require an approval policy by default:

- publishing or posting externally;
- sending outbound messages;
- launching campaigns;
- spending money;
- modifying production customer data.

The current implementation flags likely side-effecting work as `blocked_for_approval`.

## 4. Planned adapter boundary

Future integrations should implement narrow adapters rather than leaking vendor APIs into the domain layer.

```text
                 ┌─ Search / Browser
Agent Runtime ───┼─ LLM Provider
                 ├─ Content Publisher
                 ├─ CRM / Lead Store
                 ├─ Analytics (GA4/GSC/etc.)
                 └─ Workflow Engine (n8n/MCP/etc.)
```

This allows Codex, Claude Code, Hermes, n8n, or another harness to use the same growth state model.

## 5. Persistence direction

The next milestone should persist:

- business context versions;
- experiments and hypotheses;
- work-item state transitions;
- approvals;
- artifacts and evidence;
- metric snapshots;
- learnings and decisions.

SQLite is sufficient for a local v0.2. PostgreSQL becomes useful once multiple workers or users write concurrently.

## 6. Execution loop

```text
1. Load shared business context
2. Research evidence
3. Propose hypothesis
4. Create measurable experiment
5. Generate work items
6. Request approval for side effects
7. Execute through adapters
8. Collect metrics
9. Evaluate outcome
10. Persist learning
11. Generate next experiment
```

The important invariant is that an agent action should be traceable back to a business goal and an experiment hypothesis.
