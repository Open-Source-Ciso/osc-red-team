"""Provider adapter stubs — wire live Claude / Codex here for pilot engagements."""

# Claude red: call Anthropic Messages API with a system prompt that demands
# structured findings JSON only (no exploit payloads). Validate schema before use.
#
# Codex blue: call OpenAI code model with finding + file context; require unified
# diff + verify test. Run tests in sandbox before proposing customer PR.

SUPPORTED = ("stub",)
