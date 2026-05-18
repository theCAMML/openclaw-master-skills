---
name: deep-research
description: "Multi-source deep research with cited reports. Searches DuckDuckGo (no API key needed), reads key sources in full, and delivers structured reports with inline citations. Use when the user asks to research, investigate, deep dive, or analyze any topic. Also use for 'find out about', 'what's the latest on', 'compare', or any request requiring multiple sources and synthesis."
---

# Deep Research

Produce thorough, cited research reports from multiple web sources. No paid APIs.

## Workflow

### 1. Clarify (optional)

If the topic is ambiguous, ask 1-2 quick questions. If the user says "just research it" — skip with defaults.

### 2. Plan

Break the topic into 3-5 sub-questions. Write them down before searching.

### 3. Search

For each sub-question, run the DDG search script:

```bash
python {baseDir}/scripts/ddg_search.py "search terms" --max 8
```

For current events:
```bash
python {baseDir}/scripts/ddg_search.py "topic" --news --max 5
```

Search strategy:
- 2-3 keyword variations per sub-question
- Mix web + news searches
- Target 15-30 unique sources total
- Prioritize: academic/official/reputable news > blogs > forums

### 4. Deep-Read

For the most promising URLs, extract full content:

```bash
python {baseDir}/scripts/url_extract.py "https://..." --max 10000
```

Read 3-5 key sources in full for depth. Don't rely on search snippets alone.

### 5. Synthesize

Write the report using this structure:

```markdown
# [Topic]: Research Report
*Date | Sources: N | Confidence: High/Medium/Low*

## Executive Summary
3-5 sentence overview of key findings

## 1. [First Major Theme]
- Key point ([Source Name](url))
- Supporting data ([Source Name](url))

## 2. [Second Major Theme]
...

## Key Takeaways
- Actionable insight 1
- Actionable insight 2

## Sources
1. [Title](url) — one-line summary
2. ...
```

### 6. Deliver

- Short topics: post full report
- Long reports: post executive summary + key takeaways, offer full report as file

## Quality Rules

1. Every claim needs a source. No unsourced assertions.
2. Cross-reference. Single-source claims flagged as unverified.
3. Prefer recent sources (last 12 months) unless historical context needed.
4. Acknowledge gaps. If good info wasn't found, say so.
5. No hallucination. "Insufficient data found" when unsure.

## Sub-Agent Usage

For large research tasks, spawn as sub-agent:

```
sessions_spawn(
  task: "Run deep research on [TOPIC]. Follow the deep-research SKILL.md workflow.
  Read {baseDir}/SKILL.md first.
  Goal: [user's goal]
  Save report to workspace.",
  label: "research-[slug]"
)
```
