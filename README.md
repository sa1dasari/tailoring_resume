# Tailoring Resume

## Files you will edit
- `inputs/resume.txt`: paste your resume text.
- `inputs/job_description.txt`: paste the target job description.

## API key (safe local storage)
1. Copy `.env.example` to `.env`.
2. Put your real Anthropic key in `.env`:
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

Generated files are saved to `output/`.

