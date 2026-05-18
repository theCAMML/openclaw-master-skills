---
name: obsidian-wiki-compiler
description: "LLM-maintained Obsidian wiki. Monitors raw/ for new data, compiles into structured .md articles with backlinks and categorization. Supports Q&A research mode against vault. Joint skill: TARS + Jarvis both contribute to shared sections/."
metadata: {"openclaw": {"emoji": "📚", "requires": {"bins": ["obsidian-cli"]}}}
---

# Obsidian Wiki Compiler

Automates LLM-maintained knowledge base following Karpathy's wiki workflow. Raw data goes in, structured wiki articles come out. Both TARS and Jarvis write to shared sections.

## Directory Structure

```
~/Documents/TARS-Vault/
├── raw/                    # Drop zone — anything here gets compiled
│   ├── inbox/              # New items awaiting compilation
│   └── processed/          # Compiled items (archived)
├── sections/               # SHARED — both agents write here
│   ├── security-audits/    # Vetted skills, threat patterns
│   ├── token-optimization/ # Config patterns, benchmarks  
│   ├── agent-protocols/    # Coordination rules, handoff patterns
│   ├── incident-logs/      # Outages, fixes, lessons learned
│   └── tool-patterns/      # Reusable scripts, wrappers
├── topics/                 # Agent-specific topics (existing)
├── channels/               # Channel memory (existing)
└── wiki-index.md           # Auto-generated index of all articles
```

## Article Format

Every compiled article must include frontmatter:

```markdown
---
title: [Article Title]
author: TARS | Jarvis
source: [origin file or URL]
compiled: YYYY-MM-DD HH:MM
last-updated: YYYY-MM-DD HH:MM
section: security-audits | token-optimization | agent-protocols | incident-logs | tool-patterns
tags: [comma, separated, tags]
size: [line count]
---

# [Title]

[Content — max 500 lines]

## Related
- [[linked-article]]
- [[another-article]]
```

## Triggers

### 1. File-Watch (Real-Time)
Monitor `raw/inbox/` for new files. On new file detected:
1. Read file contents
2. Classify into appropriate section
3. Compile article using LLM
4. Write to `sections/[section]/[slug].md`
5. Move source to `raw/processed/`
6. Update `wiki-index.md`

### 2. Daily Cron (Health Check)
Run daily at 06:00 local time:
1. Scan all sections/ for articles
2. Check for broken links (`[[article]]` that don't exist)
3. Check for orphan files (no incoming links)
4. Check size limits (flag articles > 500 lines)
5. Check stale articles (not updated in 30 days)
6. Generate health report → `sections/incident-logs/wiki-health-YYYY-MM-DD.md`

### 3. Manual Trigger
User says: "compile [file/topic]" or "wiki health check"

## Compilation Protocol

When compiling a raw file:

```
1. READ source file
2. CLASSIFY: which section does this belong to?
3. CHECK: does a related article already exist?
   - YES: append/update existing article
   - NO: create new article
4. EXTRACT: key concepts, patterns, rules
5. WRITE: structured article with frontmatter
6. LINK: identify related articles, add [[backlinks]]
7. INDEX: update wiki-index.md
8. ARCHIVE: move source to raw/processed/
```

## Research Mode (Q&A)

Triggered by: "search wiki for [topic]" or "what does the wiki say about [topic]"

```
1. memory_search() against vault (cheap, targeted)
2. Load matching articles from sections/
3. Synthesize answer with citations: "From sections/security-audits/json-rewrite.md:12"
4. Never load full vault — scoped by default, full on explicit request
```

## Conflict Resolution

When both TARS and Jarvis write to the same section:

1. **Same topic, different articles:** Keep both, add cross-link
2. **Same article, different content:** Most recent wins, other agent's content moved to ## Alternative Perspective section
3. **Contradicting facts:** Flag with `<!-- CONFLICT: [description] -->` and notify both agents via coordination-hub

## Size Limits

- Max 500 lines per article
- If article exceeds limit: split into sub-articles with `## Part 1`, `## Part 2`
- wiki-index.md: auto-generated, no manual edits

## Security Rules (from security-audit skill)

- Never compile files containing API keys, passwords, or credentials
- Never write operator-specific personal data to shared sections/
- Sanitize all content before writing to shared sections
- Source attribution required on every article

## Integration Points

### With HEARTBEAT.md
Add to HEARTBEAT.md to enable autonomous compilation:
```
## Wiki Compiler
Check raw/inbox/ for new files. If any found, compile them.
Run wiki health check if last check was >24 hours ago.
```

### With Obsidian CLI
```bash
# List all articles in a section
obsidian-cli list sections/security-audits

# Create new article
obsidian-cli create "sections/security-audits/new-threat" -c "[content]" -o

# Search vault
obsidian-cli search-content "[query]"
```

### With Jarvis (Cross-Agent Sync)
Post compiled article summaries to #coordination-hub:
```
📚 Wiki updated: [article title] added to sections/[section]/
Source: [origin] | Author: TARS/Jarvis | Tags: [tags]
```

## Phase 1 Scope (MVP)

- [ ] raw/inbox/ watcher (manual trigger only for Phase 1)
- [ ] Basic compilation (read → classify → write article)
- [ ] Frontmatter generation
- [ ] wiki-index.md generation
- [ ] Discord notification on compile

## Phase 2 Scope

- [ ] File-watch auto-trigger
- [ ] Backlink generation
- [ ] Daily health check cron
- [ ] Research mode (Q&A)
- [ ] Cross-agent sync protocol

## Phase 3 Scope

- [ ] Visual outputs (Marp slides, mermaid diagrams)
- [ ] Conflict resolution automation
- [ ] Wiki analytics (most linked, most stale, coverage gaps)

---

*Joint skill: TARS (scaffold) + Jarvis (compilation logic)*  
*Created: 2026-04-10*
