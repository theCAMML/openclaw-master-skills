# Project Bootstrapper Skill

## Purpose
Automatically create new project agents following polyrepo architecture. **NEVER create projects in TARS workspace again.**

## Triggers
- User says "start a new project"
- User mentions "create [project name]"
- User asks to work on a new domain/codebase
- Any mention of "new agent" or "new workspace"

## Polyrepo Architecture (Mandatory)

**Rule:** One agent per major project. No project code in TARS workspace.

### When to Create a New Agent

Create a separate agent when:
- ✅ Project has >10 files
- ✅ Project has distinct domain/purpose (trading ≠ community ≠ CAD work)
- ✅ Project will be actively developed (not one-off scripts)
- ✅ Project needs isolated context (no bleed from other projects)

Keep in TARS when:
- ❌ One-off scripts or utilities (<10 files)
- ❌ Meta-tasks (cron jobs, email, memory management)
- ❌ Research or planning (no executable code)

## Creation Process

### Step 0: Backup First (MANDATORY)
```bash
# ALWAYS backup before structural changes
cd ~/.openclaw/agents/tars
mkdir -p backups/pre-[project-name]-$(date +%Y%m%d-%H%M%S)
tar -czf backups/pre-[project-name]-$(date +%Y%m%d-%H%M%S)/workspace-backup.tar.gz workspace/
```

### Step 1: Create Agent Directory
```bash
mkdir -p ~/.openclaw/agents/[project-name]/workspace
```

### Step 2: Create Core Files

**AGENTS.md** (defines agent purpose and responsibilities)
**README.md** (navigation and usage guide)
**memory/** (project-specific learnings)
**skills/** (copy security-audit + git, add project-specific skills)

### Step 3: Move/Create Project Code
```bash
# If code exists in TARS workspace, MOVE it:
mv ~/.openclaw/agents/tars/workspace/[project] ~/.openclaw/agents/[project-name]/workspace/

# If starting fresh, create structure:
mkdir -p ~/.openclaw/agents/[project-name]/workspace/[project]
```

### Step 4: Update Agent Router

Add keywords to `~/.openclaw/agents/tars/workspace/skills/agent-router/SKILL.md`:

```markdown
### [project-name]
**Keywords:** [key, terms, for, detection]
**Path:** `~/.openclaw/agents/[project-name]`
**Use for:** [brief description]
```

### Step 5: Build Knowledge Graph
```bash
cd ~/.openclaw/agents/[project-name]/workspace
code-review-graph build
```

### Step 6: Test Routing

Verify automatic routing works:
- Ask a project-specific question
- TARS should route to new agent automatically
- Response should be project-focused (no context bleed)

## File Templates

### AGENTS.md Template
```markdown
# AGENTS.md - [Project Name]

## Purpose
[Brief description of what this agent does]

## Every Session
1. **Check [primary resource]** - [what to monitor]
2. **Review [secondary resource]** - [what to track]
3. **[Main action]** - [core responsibility]
4. **Log activity** - maintain audit trail

## Files & Structure
- `[project-dir]/` - Main codebase
- `memory/` - Project learnings
- `data/` - Project data (if applicable)

## Core Responsibilities
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

---

*Isolated [domain] environment - no other project context.*
```

### README.md Template
```markdown
# [Project Name] Agent

**Role:** [One-line description]

## Quick Start
\`\`\`bash
cd ~/.openclaw/agents/[project-name]
claude
\`\`\`

## Responsibilities
- [What this agent handles]

## Related Agents
- **TARS** - Meta-coordinator (spawns this agent automatically)
- **[other-agent]** - [relationship if any]

## Knowledge Graph
\`\`\`bash
code-review-graph status        # Check graph health
code-review-graph visualize     # View graph
code-review-graph update        # Refresh after changes
\`\`\`
```

## Examples

### Example 1: New Trading Bot
**User:** "I want to build a crypto trading bot"

**Actions:**
1. Create `~/.openclaw/agents/crypto-trader/`
2. Create AGENTS.md (purpose: crypto trading)
3. Copy skills (security-audit, git)
4. Update agent-router with keywords: "crypto, bitcoin, ethereum, trading"
5. User never needs to manually switch - routing handles it

### Example 2: New Client Project
**User:** "Start work on the [Client Name] project"

**Actions:**
1. Create `~/.openclaw/agents/client-[name]/`
2. Create AGENTS.md (purpose: client deliverables)
3. Move/create project code
4. Update agent-router with keywords: "client name, project codename"
5. Build knowledge graph for client code only

### Example 3: One-Off Script (Stay in TARS)
**User:** "Write a quick script to parse this CSV"

**Actions:**
1. ❌ Don't create new agent (one-off, <10 files)
2. ✅ Create in `~/.openclaw/agents/tars/workspace/scripts/`
3. ✅ Handle directly in TARS

## Migration Checklist

When creating a new project agent:

- [ ] **BACKUP FIRST** (workspace tarball with timestamp)
- [ ] Create agent directory structure
- [ ] Write AGENTS.md (purpose, responsibilities, structure)
- [ ] Write README.md (usage, navigation)
- [ ] Copy core skills (security-audit, git)
- [ ] Move project code from TARS workspace (if exists)
- [ ] Create .code-review-graphignore
- [ ] Update agent-router keywords
- [ ] Build knowledge graph
- [ ] Test automatic routing
- [ ] Document in TARS README.md

## TARS Workspace Rules

**TARS workspace should ONLY contain:**
- ✅ `memory/` - Cross-project learnings
- ✅ `skills/` - Global skills (security-audit, agent-router, etc.)
- ✅ `scripts/` - Meta scripts (briefings, email, cron helpers)
- ✅ `docs/` - Documentation
- ✅ `obsidian-vault/` - Personal knowledge base
- ✅ `backups/` - System backups
- ❌ **NO PROJECT CODE** (should be in separate agents)

## Benefits Reminder

**Why polyrepo?**
- 85% token cost reduction ($765/month savings)
- No context bleed between projects
- Fast, focused responses (15k vs 100k tokens per query)
- Knowledge graph actually works (1k vs 70k nodes)
- Clean visualization per project
- Automatic routing (user never switches manually)

---

**Default action when user mentions new project: CREATE SEPARATE AGENT.**
