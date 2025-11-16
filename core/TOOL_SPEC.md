# Tool Specification Template

> Template for defining tools available to agents. External runtimes parse these definitions.

---

## YAML Format

```yaml
id: tool_name
name: Human Readable Name
description: What this tool does and when to use it

inputs:
  type: object
  required: [field1, field2]
  properties:
    field1:
      type: string
      description: Field description
    field2:
      type: number
      description: Field description

outputs:
  type: object
  required: [ok]
  properties:
    ok:
      type: boolean
      description: Success status
    data:
      type: object
      description: Result data
      additionalProperties: true
    meta:
      type: object
      description: Metadata (timestamps, token counts)
      additionalProperties: true

safety:
  rate_limit: 10  # calls per minute
  pii_allowed: false

permissions:
  allowed_roles: [orchestrator, researcher, verifier]
```

---

## Standard Output Format

All tools must return this structure:

```json
{
  "tool": "tool_name",
  "ok": true,
  "data": { /* tool-specific result */ },
  "meta": {
    "timestamp": "2025-11-16T10:00:00Z",
    "tokens": 123
  }
}
```

---

## Example Tools

### Search Tool

```yaml
id: web_search
name: Web Search
description: Search the web for current information

inputs:
  type: object
  required: [query]
  properties:
    query:
      type: string
      description: Search query
    max_results:
      type: number
      default: 5

outputs:
  type: object
  properties:
    ok: { type: boolean }
    data:
      type: array
      items:
        type: object
        properties:
          title: { type: string }
          url: { type: string }
          snippet: { type: string }
```

### File Read Tool

```yaml
id: file_read
name: Read File
description: Read contents of a file

inputs:
  type: object
  required: [path]
  properties:
    path:
      type: string
      description: File path
    max_lines:
      type: number
      default: 1000

outputs:
  type: object
  properties:
    ok: { type: boolean }
    data:
      type: object
      properties:
        content: { type: string }
        lines: { type: number }
```
