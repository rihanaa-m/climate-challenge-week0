# Climate Challenge Week 0

This repository contains the initial Python environment setup for the project.

## Reproduce the environment

1. Create a virtual environment:
   - Windows PowerShell:
     - `python -m venv .venv`
2. Activate the environment:
   - Windows PowerShell:
     - `.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`

## Basic CI

GitHub Actions workflow lives at `.github/workflows/ci.yml`.
It runs on every push to the `main` branch and installs dependencies using `requirements.txt`.

## Suggested folder structure

```text
climate-challenge-week0/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── README.md
└── requirements.txt
```
