# Local Manual Resume Tailoring

This directory contains the local script for manually tailoring a single resume to a job description.

## Files

- **`tailor_resume.py`** - Main tailoring script
- **`inputs/`** - Input files
  - `job_description.txt` - Target job description
  - `Sawan_Dasari_Resume.docx` - Source resume
- **`output/`** - Generated output files
  - `tailored_resume_<Company>.docx` - Tailored resume
  - `changes_summary_<Company>.docx` - What changed
- **`rules/`** - Resume formatting rules
  - `resume_rules.txt` - Tailoring guidelines for Claude

## Usage

### 1. Prepare Input Files

Edit the input files:

```powershell
# Edit job description
notepad local/inputs/job_description.txt

# Edit or replace resume if needed
# local/inputs/Sawan_Dasari_Resume.docx
```

### 2. Run the Script

```powershell
python local/tailor_resume.py
```

### 3. Review Output

Generated files appear in `local/output/`:
- Tailored resume (DOCX)
- Change summary (DOCX) showing what was modified

## Features

### What It Does

- Reads resume and job description
- Uses Claude to generate ATS-friendly tailored resume
- Creates a detailed change summary
- Uses only existing resume content (no fabrication)
- Contextually integrates JD-relevant technologies when appropriate
- Formats bullets with action verbs (no "I" or "For...I")

### Resume Tailoring Rules

The script follows strict rules defined in `rules/resume_rules.txt`:

1. **ATS-Friendly Format** - Standard headers, plain text, keyword optimization
2. **Technology Injection** - Names JD technologies where contextually appropriate
3. **Action Verbs** - Bullets start with strong verbs (Developed, Implemented, Built...)
4. **No Fabrication** - Only uses information from source resume
5. **Quantified Results** - Includes metrics when available
6. **Relevance** - Prioritizes skills/experience relevant to the role

### Example Output

**Input**: Generic resume + Netflix job description  
**Output**: 
- Resume tailored to Netflix's tech stack (Java, Kafka, AWS, microservices)
- Bullets rewritten to emphasize relevant experience
- Summary adjusted to match role requirements
- Skills section prioritized for Netflix's needs

## Configuration

### API Key

Store the Anthropic API key in `.env` at project root:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Model

Default model is `claude-sonnet-4-5`. Change in `tailor_resume.py`:

```python
MODEL = "claude-sonnet-4-5"  # or "claude-opus-4-5"
```

## Dependencies

Installed via `requirements.txt` at project root:

- `anthropic` - API client
- `python-docx` - DOCX file handling

## Related

- **Agent Automation**: See [`../agent/`](../agent/) for automated LinkedIn job search workflow
- **Documentation**: See [`../docs/`](../docs/) for setup guides

