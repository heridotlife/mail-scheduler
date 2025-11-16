# SESSION_LOG.md

> This file is a structured scratchpad for session-scoped state, reasoning, and observability.  
> It is separate from conversational context to prevent pollution and enable clean handoffs.

---

## Session: [session_id] @ [timestamp]

**Session Date**: YYYY-MM-DD (local system time)  
**Session Timestamp**: YYYY-MM-DDTHH:MM:SS±HH:MM  
**Persona**: [persona-name]  
**Token Budget**: [budget] tokens  
**Trace Enabled**: [true/false]  
**Verbosity**: [silent/normal/verbose/debug]

---

## Task

[Original user request or task objective]

---

## Plan

1. Step 1 description
2. Step 2 description
3. Step 3 description
4. ...

---

## Triadic Handoff (optional)

| Stage | Owner | Artefact | Status |
|-------|-------|----------|--------|
| Brief | User | `handoffs/mission.md` or Task section | [ ] Pending / [ ] Complete |
| Plan | GPT-5 Codex | `handoffs/plan.md`, context bundle, Claude prompt | [ ] Pending / [ ] Complete |
| Execute | Claude Code Sonne 4.5 | `handoffs/claude_output.md` | [ ] Pending / [ ] Complete |
| Review | GPT-5 Codex + User | Acceptance notes in SESSION_LOG | [ ] Pending / [ ] Complete |

- **Notes**: Capture blockers, deviations, or escalations related to the triad handoff here.

---

## Reasoning

- **Decision**: Why tool X was chosen over tool Y
- **Constraint**: Token budget = 8000, must stay under 50%
- **Observation**: User prefers local dates for version checks
- **Trade-off**: Chose speed over accuracy for initial prototype

---

## Tool Calls

- `tool_name(arg1, arg2)` → result summary (tokens: ~234)
- `another_tool()` → ERROR: [error message] (tokens: ~45)
- `file_read("path/to/file")` → 500 lines, summarized to 50 (tokens: ~180)

---

## State Checkpoints

- **After step 2**: [checkpoint_id or state snapshot]
- **Before multi-agent handoff**: [serialized state]
- **After context summarization**: [checkpoint with summary]

---

## Token Usage @ [timestamp]

- **LLM Call** (agent node): input=234, output=156, total=390
- **Tool Call** (search): ~180 tokens
- **Tool Call** (file_read): ~500 tokens (summarized to ~200)
- **Cumulative**: 1,245 / 8,000 (15.6%)

---

## Health Check @ [timestamp]

- **Token utilization**: 50% (WARN) → Triggered summarization
- **Message count**: 12 messages
- **Contradictions**: None detected
- **Staleness**: None detected
- **Completeness**: All required fields present
- **Action taken**: Summarized 8 messages → 1 summary (saved ~1,200 tokens)

---

## Trace (if trace=true)

- `[2025-11-09T10:35:22]` [INFO] Loaded persona: backend-architect
- `[2025-11-09T10:35:25]` [DEBUG] LLM call: {input: "...", output: "..."}
- `[2025-11-09T10:35:28]` [INFO] Tool call: search("latest Python version")
- `[2025-11-09T10:35:30]` [WARN] Token budget at 60% utilization
- `[2025-11-09T10:35:32]` [INFO] Triggered context summarization
- `[2025-11-09T10:35:35]` [DEBUG] Validation: TOON format round-trip successful

---

## Notes

- This file is append-only during active session
- Archive to `.session-archive/` at session end
- Use structured sections above for consistency
- Log all major decisions, tool calls, and health checks
- Keep summaries concise (preserve detail in isolated artifacts)

---

**Session Status**: [IN_PROGRESS | COMPLETED | FAILED]  
**Last Updated**: [timestamp]
