---
description: "Use when changing account mapping flow across configuration, grouping, or mapper modules. Keeps category and pattern matching behavior consistent."
name: "Mapping Flow Conventions"
applyTo: "src/{configuration.py,transactionGrouper.py,accountMapper.py}"
---
# Mapping Flow Conventions

- Keep configuration validation strict and fail fast for invalid or missing mapping fields.
- Preserve category and pattern matching semantics, including case-insensitive regex handling.
- Keep grouping and mapping behavior aligned so grouped outputs remain predictable.
- Avoid silent fallback changes; if fallback behavior changes, document and test it explicitly.
- Cover mapping-flow changes with focused unit tests and at least one integration test path.
