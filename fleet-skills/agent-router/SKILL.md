# Agent Router Skill

## Purpose
Automatically detect which project agent should handle a query and route accordingly. User should NEVER need to manually switch agents.

## Triggers
**EVERY user message** - this skill runs first, before any other response.

## Agent Registry

### kalshi-trader
**Keywords:** kalshi, prediction market, trading signals, market scan, opportunities, arbitrage, positions, kalshi api, trade execution, market data
**Path:** `~/.openclaw/agents/kalshi-trader`
**Use for:** Kalshi prediction market trading operations

### ibkr-trader  
**Keywords:** ibkr, interactive brokers, stocks, options, portfolio, equity, broker, stock signals, option chain, ibkr api
**Path:** `~/.openclaw/agents/ibkr-trader`
**Use for:** Interactive Brokers trading operations

### agent-syndicate
**Keywords:** discord, agent syndicate, recruitment, community, agents, discord bot, channels, moderation, #recruitment, server
**Path:** `~/.openclaw/agents/agent-syndicate`
**Use for:** Discord community and bot operations

### kalshi-accountant
**Keywords:** trade report, pnl, profit loss, accounting, reconcile trades, trade history, performance report
**Path:** `~/.openclaw/agents/kalshi-accountant`
**Use for:** Trading accounting and reporting

### kalshi-analyst
**Keywords:** market analysis, research, market research, analyze market, market trends, forecast
**Path:** `~/.openclaw/agents/kalshi-analyst`
**Use for:** Market research and analysis

## Routing Logic

### Step 1: Keyword Matching
```python
def detect_project(query: str) -> Optional[str]:
    query_lower = query.lower()
    
    # Check each agent's keywords
    for agent, keywords in AGENT_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            return agent
    
    return None  # Stay in current agent (TARS)
```

### Step 2: Execute Routing
If a project agent is detected:

1. **Use sessions_spawn** with `runtime="subagent"` to delegate to the project agent
2. **Pass the full query** to the target agent
3. **Return the response** to the user
4. **User never knows** the routing happened

If no project detected:
- Stay in TARS (meta-coordinator)
- Handle meta-tasks (email, briefings, research, planning)

## Implementation

**On every user message:**

```python
# Detect target agent
target_agent = detect_project(user_message)

if target_agent:
    # Route to project agent using subagent spawn
    response = sessions_spawn(
        runtime="subagent",
        mode="run",
        task=user_message,
        cwd=f"~/.openclaw/agents/{target_agent}/workspace",
        label=f"{target_agent}-task"
    )
    return response
else:
    # Handle in current agent (TARS)
    return handle_meta_task(user_message)
```

## Examples

**User:** "Check Kalshi for trading opportunities"
→ **Routes to:** kalshi-trader agent (keyword: "Kalshi")

**User:** "What's happening in the Discord?"
→ **Routes to:** agent-syndicate agent (keyword: "Discord")

**User:** "Run morning briefing"
→ **Stays in:** TARS (no project keywords, meta-task)

**User:** "Show me the IBKR portfolio"
→ **Routes to:** ibkr-trader agent (keyword: "IBKR")

**User:** "Generate trade report for last month"
→ **Routes to:** kalshi-accountant agent (keyword: "trade report")

## Edge Cases

### Multi-Project Queries
**User:** "Compare Kalshi vs IBKR performance"
→ **Stay in TARS**, spawn both agents as subagents, aggregate results

### Ambiguous Queries  
**User:** "What's the status?"
→ **Stay in TARS**, ask which project or report on all

### Context Switching
**User in kalshi-trader:** "Now check Discord"
→ **Route to agent-syndicate** (keywords override current context)

## Critical Rules

1. **Routing is invisible** - User never sees "Switching to agent X"
2. **Response is seamless** - Just answer the question
3. **No confirmation needed** - Don't ask "Should I switch to X?" - just do it
4. **Preserve context** - If routed agent needs more info, ask within that context
5. **Fast routing** - Keyword detection takes <10ms, no overhead

## Never Do This

❌ "I'll switch to the kalshi-trader agent to check that..."
❌ "Would you like me to route this to agent-syndicate?"
❌ "You need to switch to the trading agent for that."

## Always Do This

✅ Just answer the question (after routing invisibly)
✅ If routing fails, stay in current agent and do your best
✅ If multi-project query, coordinate from TARS

---

**User should never know agent routing exists. It just works.**
