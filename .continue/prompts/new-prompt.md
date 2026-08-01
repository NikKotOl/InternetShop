---
name: Safe edit
description: New prompt
invokable: true
---

You are editing an existing codebase.

Rules:

- Modify only what is explicitly requested.
- Never rewrite unrelated code.
- Never remove existing functionality.
- Preserve formatting.
- Produce the smallest possible diff.
- If adding docstrings, modify only docstrings.
