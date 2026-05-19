# Platform Writing

This method teaches an agent to separate writing quality from platform layout.

The mistake is to ask: "How do I publish this Markdown?"

The better question is:

```text
What should this content do for the reader, and which platform form best serves
that purpose?
```

## Layers

1. **Writing core**: reader, promise, memory point, next action.
2. **Content structure**: hook, context, claim, evidence, method, payoff.
3. **Platform layout**:
   - WeChat Official Account optimizes attention, phone readability, sharing,
     and follow/convert behavior.
   - Feishu Docs optimizes collaboration, durability, traceability, and
     updateability.
   - Tencent Docs optimizes online document creation and SmartCanvas-style
     presentation.
4. **Tool execution**: use md2wechat, feishu-cli/feishu-docx, or Tencent Docs
   MCP only after the content shape is clear.
5. **Verification**: preview, inspect, export/read-back, or permission check.

## Reusable Prompt

```text
Turn this material into a platform-ready document.

First identify reader, promise, memory point, and next action.
Then draft the content once.
Then choose the target platform:
- WeChat: optimize first screen, rhythm, shareability, CTA.
- Feishu: optimize structure, collaboration, future updates, permissions.
- Tencent Docs: optimize SmartCanvas readability and verify real rendering.

Do not publish or write to a shared document until I explicitly ask.
```

