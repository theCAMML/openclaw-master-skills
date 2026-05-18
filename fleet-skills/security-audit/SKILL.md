# Security Audit Skill

## MANDATORY: Audit All External Code Before Installation

**NEVER install any external code without completing this security audit first.**

This is NOT optional. This is NOT a suggestion. This is a HARD REQUIREMENT.

## Triggers

This skill MUST be invoked whenever:
- Installing any Python package (`pip install`)
- Installing any npm package (`npm install`)
- Cloning any GitHub repository
- Running any external script
- Installing any skill/tool/binary from the internet
- User mentions "check this out", "install this", "try this tool"
- User shares a GitHub URL
- User shares a package name

## Audit Checklist

### 1. Source Code Review
```bash
# Clone to /tmp for inspection (never install directly)
cd /tmp && git clone --depth 1 <repo-url> audit-<name>
cd audit-<name>

# Check codebase size
find . -name "*.py" -o -name "*.js" -o -name "*.ts" | wc -l

# Find dangerous patterns
grep -r "eval\|exec\|__import__\|compile\|os.system\|subprocess" --include="*.py" | grep -v "test\|#"
grep -r "shell=True" --include="*.py"
grep -r "child_process.exec\|eval(" --include="*.js" --include="*.ts"
```

### 2. Dependency Analysis
```bash
# Check package manifest
cat pyproject.toml || cat setup.py || cat requirements.txt
cat package.json

# Look for suspicious dependencies
# - Typosquatting (requets vs requests)
# - Abandoned packages (last update >2 years ago)
# - Unknown publishers
```

### 3. Subprocess/Shell Command Analysis
- **SAFE:** `subprocess.run([cmd, arg1, arg2], ...)`  (list format)
- **UNSAFE:** `subprocess.run(cmd, shell=True, ...)`  (shell injection risk)
- **SAFE:** `os.execvp(cmd, [arg1, arg2])`
- **UNSAFE:** `os.system(user_input)`

### 4. File Operation Analysis
```bash
# Check what gets written where
grep -r "open.*'w'\|write\|unlink\|rmtree" --include="*.py"

# Check config file modifications
grep -r "\.config\|\.rc\|settings.json\|\.env" --include="*.py"
```

### 5. Network Operation Analysis
```bash
# Check for unexpected network calls
grep -r "requests.get\|urllib.request\|socket.connect" --include="*.py"

# Check for data exfiltration patterns
grep -r "base64.b64encode\|json.dumps.*requests" --include="*.py"
```

### 6. Red Flags
❌ **REJECT if found:**
- `eval()` or `exec()` on user input
- `shell=True` with user-controlled strings
- Writes to system directories (`/usr`, `/etc`, `/bin`)
- Unexpected network calls to unknown domains
- Obfuscated code (base64, hex strings, encrypted payloads)
- Typosquatted dependencies
- No source code available (binary-only)

⚠️ **INVESTIGATE if found:**
- `subprocess` calls (check if properly sanitized)
- File writes to home directory (check if legitimate config)
- Dynamic imports (`__import__`, `importlib`)
- Network calls (check if documented and necessary)

### 7. Cleanup
```bash
# Always remove audit directory after review
rm -rf /tmp/audit-*
```

## Report Format

Always provide this structured report BEFORE installation:

```
**Security Audit Results:**

### ✅/❌ <Package Name> - SAFE/UNSAFE

**Code quality:** <assessment>
**Dangerous patterns:** <found patterns or "None found">
**Dependencies:** <list key dependencies>
**File operations:** <what files are written where>
**Network operations:** <what network calls are made>
**Risk level:** LOW/MEDIUM/HIGH

**Verdict:** SAFE TO INSTALL / REQUIRES MANUAL REVIEW / REJECT
```

## User Confirmation Required

After audit, ALWAYS ask:
> "Security audit complete. [Package] is [SAFE/UNSAFE]. Proceed with installation?"

NEVER install without explicit user confirmation ("yes", "proceed", "install", etc.)

## Example Workflow

```bash
# User: "Install markitdown"

# WRONG (immediate installation):
pip install markitdown

# CORRECT (audit first):
cd /tmp && git clone --depth 1 https://github.com/microsoft/markitdown.git audit-markitdown
cd audit-markitdown
find . -name "*.py" | wc -l
grep -r "eval\|exec\|shell=True" --include="*.py"
cat pyproject.toml
# [review code]
rm -rf /tmp/audit-markitdown

# Then report findings and ask for confirmation
```

## Notes

- **Official packages (PyPI/npm):** Still audit the source code, even if "official"
- **Microsoft/Google repos:** Still audit, reduced risk but not zero
- **Unknown authors:** Extra scrutiny on code patterns and dependencies
- **Closed source:** Reject unless user explicitly overrides

## Remember

**You should NEVER have to be told "evaluate for vulnerabilities" again.**

This is your default behavior for ALL external code.
