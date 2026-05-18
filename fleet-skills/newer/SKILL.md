---
name: Gated Session Reset
slug: newer
version: 1.0.0
description: Run the session-end enforcement gate, then call /new if all checks pass. Use instead of /new to ensure memory and logs are written before context is cleared. Includes mandatory pattern discovery check.
---

# /newer

Run the session-end gate before resetting the session. **Do not call /new directly — let the gate decide.**

## Steps

**1. Run the gate:**
```
python scripts/session_end_check.py
```

**2. Read the exit code:**

- **Exit 0 (pass):** Reply with the gate output, then immediately issue `/new`.
- **Exit 1 (blocked):** Report exactly what failed. Do NOT issue `/new`. Tell the user what needs to be fixed.

## If the user replies "force"

Run with override flag and then issue `/new`:
```
python scripts/session_end_check.py --force
```
Note the forced override in today's memory log before resetting.

## What the Gate Checks

The `session_end_check.py` script verifies:

1. **Memory files written** — `memory/learnings.md` exists and has content
2. **Session logs backed up** — logs are persisted before context clear
3. **Patterns discovered?** — Did this session uncover any patterns? (NEW)
   - If yes → Gate prompts for pattern details (uses PATTERN_DISCOVERY.md template)
   - If no → Confirms "no patterns found" and proceeds
4. **Peer sync ready** — (if configured) SSH connection to peer agent

Only when ALL checks pass does the gate exit with code 0.

## Pattern Discovery Gate (New)

When the gate detects a session ending, it asks:

```
📋 PATTERN CHECK — Before session reset

Did you discover any patterns this session?
(errors fixed, edge cases, workarounds, unexpected behaviors)

Pattern = reusable lesson worth 2+ hours for next operator.

Reply: yes/no
```

**If yes:**
```
Pattern Title: ___
Trigger (what caused it): ___
Impact (how it affected session): ___
Fix/Workaround: ___
Rule for new members (one-liner): ___
```

Gate captures the pattern and appends to `memory/learnings.md` under "## Patterns Discovered" with timestamp + agent name.

**If no:**
```
Confirming: no patterns discovered this session.
Proceeding to session reset.
```

## Why This Exists

Models skip end-of-session housekeeping under compaction pressure or after long conversations. The gate turns "should do" into "must do." Type `/newer` instead of `/new` as a habit — the check costs nothing when clean, and catches the gaps when it's not.

Pattern discovery adds a **knowledge capture loop** at session close — ensures hard-won lessons aren't lost to context resets.

## Related Files

- **scripts/session_end_check.py** — The gate implementation
- **PATTERN_DISCOVERY.md** — Full pattern guide, cron spec, GitHub strategy  
- **memory/learnings.md** — Where patterns are stored
- **weekly-pattern-digest.sh** — Sunday 10 AM cron (aggregates patterns)

---

*Canonical version: April 16, 2026 thread. Updated with pattern discovery integration: May 6, 2026.*
