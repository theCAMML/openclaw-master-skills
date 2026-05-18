---
name: smart-summarize
description: "Summarize URLs, local files, transcripts, and documents using built-in tools and local extraction. No external APIs needed. Use when the user asks to summarize, condense, extract key points, give me the TLDR, or digest any content. Supports web pages, local .txt/.md/.json/.csv/.srt/.html files, and transcript files."
---

# Smart Summarize

Summarize any content — URLs, local files, transcripts — without external APIs.

## Workflow

### 1. Identify Source Type

| Source | Method |
|---|---|
| URL (web page) | `web_fetch` tool |
| Local file (.txt, .md, .json, .csv, .srt, .vtt, .html) | `python {baseDir}/scripts/file_extract.py` |
| Transcript JSON | `file_extract.py` (auto-extracts `text` or `segments` field) |
| YouTube URL | `web_fetch` on page (gets description/transcript if available) |

### 2. Extract Content

**URL:**
```
web_fetch(url="https://...", extractMode="markdown", maxChars=12000)
```

**Local file:**
```bash
python {baseDir}/scripts/file_extract.py "path/to/file" --max 12000
```

**Long files** (books, transcripts): Extract in chunks with `--max` and process sections.

### 3. Summarize

Produce a structured summary:

```markdown
# [Title]: Summary

## Key Points
- Point 1
- Point 2
- Point 3

## Main Content
[2-3 paragraph synthesis of the material]

## Notable Details
- Detail 1
- Detail 2

## Action Items (if applicable)
- [ ] Item 1
```

### 4. Adjust Depth

Match depth to the user's request:
- **TLDR**: 3-5 bullet points only
- **Summary**: Key points + main content (default)
- **Deep summary**: Full structured summary with notable details + action items
- **Section-by-section**: For long content, summarize each section separately

### 5. Save (optional)

If the summary is substantial or the user may want it later:
```bash
# Save alongside the source file or in workspace
write to: [same-dir]/[name]-summary.md
```

## Quality Rules

1. Preserve the author's intent — don't inject opinions
2. Quantify when possible ("3 strategies" not "several strategies")
3. Flag uncertainty — if the source is ambiguous, say so
4. Keep proportional — don't over-summarize short content or under-summarize long content
5. For transcripts: preserve speaker attributions if identifiable

## Batch Mode

When summarizing multiple files (e.g., a folder of transcripts):
1. List the files
2. Extract each one
3. Summarize individually first
4. Then produce a meta-summary across all files
