# Managed Agent Automation

This directory contains the managed agent automation that searches LinkedIn for jobs and tailors resumes automatically.

## Files

- **`system_prompt.txt`** - Agent system prompt (instructions)
  - Copy this to Anthropic Console to update the agent
  - Contains full workflow, rules, and requirements
  
- **`trigger_session.py`** - Session trigger script
  - Creates managed agent sessions
  - Sends initial message to start workflow
  - Streams events for real-time monitoring

## Usage

### Manual Trigger (Ad-hoc)

```powershell
python agent/trigger_session.py
```

This creates a new session and runs the full job search workflow.

### Scheduled Trigger (GitHub Actions)

The agent runs automatically on Wed/Fri/Sat/Sun at 8 AM and 5 PM ET via GitHub Actions workflow (`.github/workflows/managed-agent-cron.yml`).

## Configuration

### Environment Variables

Required in `.env` file at project root:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...
MANAGED_AGENT_ID=agent_011CaSW...
SESSION_ENVIRONMENT_ID=env_01S2uLu...
VAULT_IDS=vlt_011Cawo...
SESSION_INPUT=Run the twice-daily LinkedIn job search and resume/CV tailoring workflow.
```

### GitHub Secrets

For scheduled runs, configure these in the GitHub repository settings:
- `ANTHROPIC_API_KEY`
- `MANAGED_AGENT_ID`
- `SESSION_ENVIRONMENT_ID`
- `VAULT_IDS`
- `SESSION_INPUT`

## Workflow Overview

1. **Search LinkedIn** - Find jobs posted in last 24 hours
2. **Tailor Resumes** - Create customized resume for each job
3. **Draft Essays** - Answer application questions
4. **Send Email** - Consolidated digest with all resumes attached
5. **Log Results** - Write run summary

## Documentation

See [`../docs/AGENT_SETUP.md`](../docs/AGENT_SETUP.md) for complete setup guide.

## Agent Details

- **Agent ID**: `agent_011CaSWBYohyTtssbr3xEg6k`
- **Model**: Claude Haiku 4.5 (standard speed)
- **Tools**: Web search, File management, Gmail MCP, GitHub MCP
- **Schedule**: Wed/Fri/Sat/Sun at 8 AM & 5 PM ET

## Updating the Agent

When modifying `system_prompt.txt`:

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Navigate to Managed Agents
3. Locate the agent
4. Edit system prompt
5. Paste contents of `system_prompt.txt`
6. Save

The agent will use the new instructions on the next session.

