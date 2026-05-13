# Resume Tailoring & Job Search Automation

Automated and manual resume tailoring using Anthropic Claude.

## Project Structure

```
tailoring_resume/
├── local/                 # Manual resume tailoring
│   ├── tailor_resume.py   # Local tailoring script
│   ├── inputs/            # Job descriptions & resume
│   ├── output/            # Generated resumes
│   └── rules/             # Formatting rules
│
├── agent/                 # Managed agent automation
│   ├── trigger_session.py # Session trigger script
│   └── system_prompt.txt  # Agent instructions
│
├── docs/                  # Documentation
│   ├── AGENT_SETUP.md     # Complete setup guide
│   └── ...                # Additional docs
│
├── .github/workflows/     # GitHub Actions
│   └── managed-agent-cron.yml
│
├── .env                   # API keys (git-ignored)
└── requirements.txt       # Python dependencies
```

## Two Workflows

### 1. Local Manual Tailoring

Tailor a single resume to a specific job description.

```powershell
# Edit inputs
notepad local/inputs/job_description.txt

# Run tailoring
python local/tailor_resume.py

# Review output
# local/output/tailored_resume_<Company>.docx
# local/output/changes_summary_<Company>.docx
```

See [`local/README.md`](local/README.md) for details.

### 2. Agent Automation

Automated LinkedIn job search + resume tailoring + email digest.

**Runs automatically** on Wed/Fri/Sat/Sun at 8 AM & 5 PM ET via GitHub Actions.

**Or trigger manually**:
```powershell
python agent/trigger_session.py
```

**What it does**:
1. Searches LinkedIn for recent Software Engineer jobs (< 24 hours old)
2. Tailors resume for each position
3. Drafts application essay answers
4. Sends consolidated email digest with all resumes

See [`agent/README.md`](agent/README.md) for details.

---

## Documentation

| Document | Description |
|----------|-------------|
| **[docs/AGENT_SETUP.md](docs/AGENT_SETUP.md)** | Complete agent configuration guide |
| **[agent/README.md](agent/README.md)** | Agent automation details |
| **[local/README.md](local/README.md)** | Manual tailoring guide |
| **[docs/README.md](docs/README.md)** | Documentation index |

