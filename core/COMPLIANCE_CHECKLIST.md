# Compliance Checklist

> Pre-execution validation to ensure agents follow `AGENTIC_GUIDE.md`.

---

## Required Before Execution

- [ ] **Persona selected** from `personas/PERSONA_CATALOG.md`
- [ ] **Session initialized**: `docs/SESSION_LOG.md` created from `templates/SESSION_LOG.md`
- [ ] **Context loaded**: Up to 1500 lines from guide and relevant personas
- [ ] **Constraints identified**: From guide section 4 (12 Factor Principles)

---

## Validation Steps

1. Check persona field is populated
2. Verify `docs/SESSION_LOG.md` exists with session metadata
3. Confirm `tmp/SESSION/` directory created for scratchpad
4. Load context from `core/AGENTIC_GUIDE.md` (max 1500 lines)

---

## Remediation

| Issue | Action |
|-------|--------|
| Missing persona | Halt execution, request persona selection |
| SESSION_LOG missing | Create from `templates/SESSION_LOG.md` |
| tmp/SESSION missing | Create directory structure |
| Context not loaded | Load AGENTIC_GUIDE.md and relevant persona file |

---

## Logging Format

Compliance status should be logged to `docs/SESSION_LOG.md`:

```markdown
## Compliance Check @ [timestamp]

- Persona: [persona-name] ✅
- SESSION_LOG: initialized ✅
- Context: loaded (1245 lines) ✅
- Constraints: identified ✅

Status: PASSED
```
