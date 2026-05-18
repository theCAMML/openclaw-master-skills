# Fleet Skills — theCAMML Custom Skills

CAMML's curated custom skills. These extend the base LeoYeAI/openclaw-master-skills collection.

## Skills

| Skill | Description |
|---|---|
| agent-audit-trail | Append-only hash-chained audit log for AI agents |
| agent-sentinel | Local-first budget and policy guardrails |
| capability-evolver-pro | Self-improvement via log analysis and evolution proposals |
| deep-research | Multi-source deep research with cited reports |
| error-recovery-automation | Standardized handling of common OpenClaw errors |
| excel-xlsx | Create, inspect, and edit Excel workbooks |
| finance-radar | Stock and crypto analysis via Yahoo Finance |
| fleet | Multi-agent fleet management CLI |
| gamer-news | Latest gaming news from major outlets |
| karpathy-llm-wiki | Persistent LLM-maintained wiki |
| memory-tiering | Multi-tiered memory management (HOT/WARM/COLD) |
| mission-control | Kanban-style task management dashboard |
| newer | Gated session reset with pattern discovery |
| obsidian-wiki-compiler | LLM-maintained Obsidian wiki |
| ontology | Typed knowledge graph for structured agent memory |
| pdf-extract | Extract text from PDF files |
| self-improving-1-2-16 | Self-reflection + self-learning agent |
| skill-scanner | Security scanner for skills and MCP tools |
| skill-trading-journal | Trade logging with performance reports |
| smart-summarize | Summarize URLs, files, documents |
| trading-desk | Institutional-grade options trading system |
| vimax | Multi-agent video generation pipeline |

## Usage

```bash
# Clone the fork
git clone https://github.com/theCAMML/openclaw-master-skills
cd openclaw-master-skills

# Point agent skills.paths to fleet-skills/
# In openclaw.json:
# "skills": { "paths": ["~/.openclaw/workspace/skills", "~/Projects/openclaw-master-skills/fleet-skills"] }
```

## Sync with upstream

```bash
git fetch upstream
git merge upstream/main
git push origin main
```
