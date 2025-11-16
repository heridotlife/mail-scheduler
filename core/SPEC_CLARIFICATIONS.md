# Spec Clarifications

> Design decisions and answers to common questions about `AGENTIC_GUIDE.md` implementation.

---

## 1. Memory Management

**Q: Should agents maintain a scratchpad during execution?**

A: **YES**. Use `docs/SESSION_LOG.md` with this structure:

```markdown
## Session: [id] @ [timestamp]
**Persona**: [name]

## Task
[User request]

## Plan
1. Step 1
2. Step 2

## Reasoning & Decisions
- Decision: [what + why]
- Constraint: [limitation]

## Tool Calls
- `tool(args)` → result (tokens: ~N)

## State Checkpoints
- After step N: [checkpoint]

## Token Usage @ [timestamp]
- Cumulative: N / budget (%)

## Health Check @ [timestamp]
- Status: healthy/warning/critical
- Action: [if needed]
```

**Lifecycle**:
1. Initialize on session start
2. Update after significant operations
3. Archive to `.session-archive/` on session end

---

## 2. Context Compression

**Q: When should agents auto-summarize context?**

A: **YES**, trigger at **50%** token usage:
- Strategy: Single-pass LLM summarization
- What to summarize: Reasoning traces, tool outputs, old messages
- Protected: Latest 2-3 message pairs, active results, current plan

**Q: Should agents trim old context?**

A: **YES**, before every LLM call:
- Keep last 2-3 human/AI pairs
- Remove duplicates
- Protect: system message, active tool results, key facts

---

## 3. Multi-Agent Workflows

**Q: Does the spec support multi-agent?**

A: **YES**, using **supervisor pattern**:
- Planner delegates to specialist agents
- Context handoff: necessary context only
- Coordination via SESSION_LOG

**State isolation**:
```javascript
{
  "messages": [],        // Exposed to LLM (trimmed)
  "summary": "",         // Selective exposure
  "context": {},         // Scratchpad (isolated)
  "tool_outputs": {},    // Isolated by default
  "large_artifacts": {}  // Never to LLM unless requested
}
```

---

## 4. Tool Selection

**Q: How many tools should agents have access to?**

A: **~30 tools** using **PERSONA-FIXED** approach:
- Each persona defines fixed tool set
- Can request additional tools mid-task if needed
- No dynamic RAG over tools (kept simple)

---

## 5. Testing & Commits

**Q: Should agents auto-run tests?**

A: **YES**, after task completion:
- Test command from project placeholders
- On failure: Report error, max 3 retries, then request help

**Q: Should agents auto-commit?**

A: **NO** - Manual commits only

---

## 6. Compliance Enforcement

**Q: Are compliance checks mandatory?**

A: **YES** - Agents must:
- Select persona before execution
- Refuse to proceed without persona
- Initialize SESSION_LOG before starting

---

## 7. Context Health

**Q: Should agents validate context integrity?**

A: **YES**, on-demand:
- Check for contradictions
- Identify potential hallucinations
- Request clarification on conflicts

**Health metrics**:
- Token utilization (warn >50%, critical >80%)
- Message count tracking
- Contradiction detection
- Staleness checks

---

## 8. Project Customization

**Q: Is this a template?**

A: **YES** - Users fill placeholders in:
- `core/AGENTIC_GUIDE.md` section 7
- Project-specific commands, frameworks, architecture

**Approach**: Manual (no setup script)

---

## 9. TOON Validation

**Q: Is round-trip validation required?**

A: **YES** - JSON → TOON → JSON must match

**Q: When to use TOON?**

A: **AUTO-DETECT** at >1000 tokens:
- Convert if payload >1KB
- Validate round-trip
- Log token savings

---

## 10. Observability

**Q: Should agents track tokens?**

A: **ON-DEMAND** via `docs/SESSION_LOG.md`:
- Per-LLM-call: input/output tokens
- Per-tool: estimated tokens
- Cumulative session total

**Q: Trace verbosity?**

A: **PERSONA-DEPENDENT**:
- Developer personas: verbose by default
- Production personas: normal by default
- Always apply privacy filtering (redact keys, PII)

**Format**: STRUCTURED-MARKDOWN in SESSION_LOG.md
