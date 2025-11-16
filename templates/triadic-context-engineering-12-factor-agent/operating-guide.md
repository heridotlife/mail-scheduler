# Triadic Operating Guide

Use this checklist to apply the triadic context engineering pattern without overwhelming ceremony.

## Before the Session
- Confirm the triad: user, Agentic A focus, Agentic B focus.
- Populate `context-bundle.template.json` with mission objective, participants, and critical inputs.
- Align on tooling channels (chat, docs, repos, APIs) and configure access keys securely.
- Schedule checkpoints for context compression and health assessment.

## During the Session
- Log each significant turn in `triad-session.template.md`; capture tool calls and decisions.
- Keep responses tight by summarizing state snapshots and linking raw artifacts instead of embedding full text.
- Alternate Agentic A and Agentic B contributions so each has clear ownership moments.
- Run quick drift checks: Are objectives, constraints, and metrics still aligned with the latest context?

## After the Session
- Review the session log; mark final decisions and unresolved risks.
- Update the context bundle with the latest state snapshot and archive outputs.
- Assess 12-factor compliance: stateless execution, config via environment or injected secrets, logging coverage, disposable processes.
- File follow-up tasks or handoffs using your preferred issue tracker or `handoffs/plan.template.md`.

## Tips
- Automate bundle validation against `schemas/context-contract.json` to catch missing fields early.
- Keep triad cadence predictable: if one agent falls behind, pause and realign objectives.
- Rotate retrospectives among the triad members to surface different insights.
