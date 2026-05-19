# WeChat Official Account

Research source:

- `geekjourneyx/md2wechat-skill`: agent-native Markdown to WeChat workflow with writing, humanizing, inspect, preview, conversion, draft upload, image generation, and structured layout modules.

## When To Use

Use this path for WeChat Official Account articles, article HTML, draft upload,
cover generation, image posts, or humanizing AI-written drafts.

## Preferred Flow

```bash
md2wechat inspect article.md
md2wechat preview article.md
md2wechat humanize article.md --intensity authentic -o article.human.md
md2wechat convert article.human.md --preview
```

Only create a draft when explicitly asked:

```bash
md2wechat convert article.human.md --draft --cover cover.jpg
```

## Writing Shape

- First screen: title, hook, promise, and reason to keep reading.
- Body: short paragraphs, concrete scenes, strong section breaks.
- Memory: one core judgment, one reusable phrase, one framework.
- Conversion: follow, collect, forward, consult, buy, or next article.

## Layout Diagnosis

Before using layout modules, ask:

1. What should the reader do?
2. What should the reader remember?
3. Is this a series or a standalone piece?

Map modules by purpose:

- attention: hero, verdict, audience fit;
- readability: part, toc, callout, steps;
- memorability: quote, verdict, summary, author card;
- conversion: cta, subscribe, faq.

Do not pile on modules. One article usually needs one hero, one verdict, and
one CTA at most.

## External Links

- https://github.com/geekjourneyx/md2wechat-skill
- https://github.com/doocs/md

