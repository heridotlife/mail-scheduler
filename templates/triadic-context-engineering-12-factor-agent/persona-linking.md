# Triadic Persona Linking Guide

Use existing personas to ground each member of the triad in clear responsibilities and communication styles. Reference the files directly so downstream automation can load traits or guardrails.

## Recommended Pairings

| Triad Role | Primary Persona | Support Persona | Notes |
| --- | --- | --- | --- |
| User (mission owner) | `personas/agents/context-manager.md` | `personas/agents/business-analyst.md` | Keeps source context organized and translates business goals into mission objectives. |
| Agentic A (orchestration & planning) | `personas/agents/ai-engineer.md` | `personas/agents/docs-architect.md` | Drives plan creation, tool-call sequencing, and documentation hygiene. |
| Agentic B (execution & delivery) | `personas/agents/dx-optimizer.md` | `personas/agents/backend-architect.md` | Focuses on implementing changes, validating outputs, and optimizing developer experience. |

> Swap in alternates from `personas/agents/` as needed (e.g., `frontend-developer.md`, `incident-responder.md`) to fit the domain or mission risk profile.

## How to Reference in Templates
- In `context-bundle.template.json`, set each `persona` field to the relative path above.
- In `triad-session.template.md`, mention any persona-driven guardrails (tone, risk tolerance, preferred tooling).
- When rotating roles, update the persona links so logs stay accurate for future analytics.

## Automation Hooks
- Build a lightweight loader that reads persona Markdown to inject key instructions into agent prompts.
- Track persona usage metrics across missions to identify effective triad combinations.
