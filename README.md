# Tailoring Resume

This project tailors your resume to a target job description using Anthropic Claude.
It reads your resume and JD, generates ATS-friendly tailored documents, and saves:
- a tailored resume (`.docx`)
- a tailored CV (`.docx`)
- a change summary (`.docx`) showing what was kept/modified/removed from the resume

## What it does
- Uses your existing resume content only (no fabricated experience/metrics)
- Reorders and refines content for the target role
- Detects likely required JD tools/technologies missing from the resume and asks the model to add them only when they fit existing experience context
- Writes polished output files to `output/`
- Produces both short-form resume and full-length CV outputs from one run
- Creates a local comparison summary between original and tailored resume

## Input files
- `inputs/Sawan_Dasari_Resume.docx`: your source resume
- `inputs/job_description.txt`: the target job description text
- `rules/resume_rules.txt`: tailoring rules and output format used by the script

If your resume file name is different, update `RESUME_PATH` in `tailor_resume.py`.

## API key (safe local storage)
1. Create `.env` in the project root.
2. Put your Anthropic key in `.env`:
   `ANTHROPIC_API_KEY=sk-ant-...`

`.env` is ignored by git via `.gitignore`.

## Install
```powershell
python -m pip install -r requirements.txt
```

## Run
```powershell
python tailor_resume.py
```

## Output files
Generated files are saved to `output/`, typically:
- `tailored_resume_<Company>.docx`
- `tailored_cv_<Company>.docx`
- `changes_summary_<Company>.docx`

