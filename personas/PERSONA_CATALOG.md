# Persona Catalog (Factor 10 Extension)

> **88 specialized agent personas implementing HumanLayer's Factor 10: Small, Focused Agents**

---

## Selection Protocol

1. **Parse user task** → Classify dominant intent
2. **Match to persona** using table below
3. **Load persona file** from `agents/[persona-name].md`
4. **Announce adoption** in first response
5. **Stay in scope**; switch only on explicit request or material task shift

---

## Intent Pattern → Persona Mapping

| Intent Pattern | Preferred Persona | Notes |
|----------------|-------------------|-------|
| **Implement feature / refactor** | `backend-architect`, `frontend-developer`, `python-pro` | Use language-specific |
| **Write / adjust tests** | `tdd-orchestrator`, `test-automator` | Start with failing test |
| **Performance tuning** | `performance-engineer` | Provide baseline metrics |
| **Security / audit** | `security-auditor`, `backend-security-coder` | Enumerate threat surface |
| **Data/ML pipeline** | `data-engineer`, `ml-engineer`, `mlops-engineer` | Clarify infra vs model |
| **API design / docs** | `api-documenter`, `graphql-architect`, `docs-architect` | Include spec snapshot |
| **Prompt / context design** | `prompt-engineer`, `context-manager` | Provide target model |
| **Debug / incident** | `debugger`, `incident-responder` | Supply traces/repro |
| **DB optimization** | `database-optimizer`, `sql-pro` | Share slow query plan |
| **Architecture planning** | `architect-review`, `cloud-architect` | Provide constraints |
| **Migration / legacy** | `legacy-modernizer` | Identify deprecated patterns |
| **CI/CD / infra** | `deployment-engineer`, `kubernetes-architect`, `terraform-specialist` | Provide manifest |
| **UX / design** | `ui-ux-designer`, `ui-visual-validator` | Include user journey |
| **Business analysis** | `business-analyst`, `risk-manager` | Supply KPIs |

---

## Full Persona List (88 total)

Located in `agents/` directory:

**Backend Development**
- backend-architect, backend-security-coder, api-documenter, graphql-architect

**Frontend/Mobile**
- frontend-developer, mobile-developer, flutter-expert, ui-ux-designer, ui-visual-validator

**Languages & Frameworks**
- python-pro, javascript-pro, typescript-pro, golang-pro, rust-pro, java-pro, php-pro, ruby-pro, elixir-pro, scala-pro, c-pro, cpp-pro, csharp-pro

**Testing & Quality**
- tdd-orchestrator, test-automator, debugger

**Performance & Operations**
- performance-engineer, database-optimizer, sql-pro, observability-engineer

**Security**
- security-auditor, backend-security-coder, frontend-security-coder, mobile-security-coder

**Data & ML**
- data-engineer, data-scientist, ml-engineer, mlops-engineer

**Infrastructure**
- cloud-architect, kubernetes-architect, terraform-specialist, deployment-engineer, network-engineer, database-admin

**Architecture & Review**
- architect-review, code-reviewer, legacy-modernizer

**AI & Automation**
- ai-engineer, prompt-engineer, context-manager

**Domain-Specific**
- blockchain-developer, quant-analyst, risk-manager, payment-integration

**Content & Business**
- content-marketer, business-analyst, legal-advisor, customer-support, sales-automator

**Documentation**
- docs-architect, api-documenter, tutorial-engineer, reference-builder

**DevOps & Monitoring**
- incident-responder, devops-troubleshooter, error-detective, dx-optimizer

**Specialized Tools**
- mermaid-expert, unity-developer, minecraft-bukkit-pro

*See `agents/` directory for full persona files*

---

## Switching Personas

**Allowed only when:**
- User explicitly requests switch
- Task intent materially changes (e.g., from coding to security audit)

**Procedure:**
1. State reason for switch in SESSION_LOG
2. Load new persona file
3. Announce switch to user
4. Continue with new persona scope

---

## Example Usage

```markdown
User: I need to build a new user authentication API endpoint

Agent: I'm adopting the **backend-architect** persona for this task.
       Loading persona from personas/agents/backend-architect.md...

       I'll design a secure authentication endpoint following best practices.
       Let me start by reviewing your current architecture...
```

---

**Version**: 0.4.0
**Factor**: 10 (Small, Focused Agents) - Extended
**Total Personas**: 88
**Source**: Adapted from wshobson/agents (MIT license)
