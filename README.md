# Tailoring Resume

## Files you will edit
- `inputs/Sawan_Dasari_Resume.docx`: place your resume DOCX file here (or update `RESUME_PATH` in `tailor_resume.py`).
- `inputs/job_description.txt`: paste the target job description.

## API key (safe local storage)
1. Create `.env` in the project root 

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

