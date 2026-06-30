---
name: hashline-editing-protocol
description: Protocol for precise, hash-anchored code editing inspired by oh-my-pi. Use when editing files to avoid "string not found" errors and ensure idempotent patches.
version: 1.0.0
yao_category: "AI编程"
---

# Hashline Editing Protocol

## Core Concept
Instead of matching raw text (which is brittle to whitespace/indentation changes), use **Hashlines** — lines prefixed with `[L{num}|{crc32}]`. This creates a unique, content-based anchor for every line.

## Workflow

### 1. Reading with Hashlines
When you need to edit a file, **always** read it with `show_hashlines=True`:
```python
read_file(path="target.py", show_hashlines=True)
```
Output format:
```text
[L0012|a1b2c3d4] def my_function():
[L0013|e5f6g7h8]     return "hello"
```

### 2. Patching with Hashlines
When calling `patch`, include the hashline prefixes in your `old_string`. The tool will automatically:
1. Detect the `[L...|...]` format.
2. Strip the prefixes to get the clean text for fuzzy matching.
3. Use the line numbers/hashes as a high-confidence hint for the matcher.

```python
patch(
    mode="replace", 
    path="target.py", 
    old_string="[L0012|a1b2c3d4] def my_function():\n[L0013|e5f6g7h8]     return \"hello\"", 
    new_string="def my_function():\n    return \"world\""
)
```

## Why this works
- **Precision**: The CRC32 hash ensures you are targeting the exact content you saw.
- **Resilience**: If the file has minor formatting changes, the underlying fuzzy matcher still works on the stripped text.
- **Idempotency**: If the hash doesn't match, the tool knows immediately that the file has changed since your last read, preventing silent corruption.

## When to use
- Complex refactoring where indentation might shift.
- Editing files with repeated code blocks (where raw text matching is ambiguous).
- Any time you want to guarantee your patch hits the intended target.