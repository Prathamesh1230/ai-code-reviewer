# AI Code Reviewer

Paste any code or drop a GitHub repo URL and get an instant structured review — 
bugs, security issues, best practices, improved code, and a score out of 10.

---

## What it does

Two ways to use it:

**Paste code** — select the language, paste your code, get a review in 10-15 seconds.

**GitHub repo** — paste a public repo URL, it fetches up to 5 code files 
using the GitHub API and reviews each one separately.

Every review has 6 sections:
- Summary
- Bugs Found
- Security Issues
- Best Practices
- Improved Code
- Score (out of 10)

---

## How it works

**Four files, one job each**

`main.py` — routing only. `reviewer.py` — LLM prompt and response parsing. 
`github_fetch.py` — GitHub API calls. `app.py` — Streamlit UI.

If Groq changes their API, only reviewer.py needs updating. 
If GitHub changes theirs, only github_fetch.py needs updating. 
Nothing bleeds into anything else.

**Structured prompt**

The prompt tells LLaMA 3.3 70B to always output in exactly those 6 sections. 
Temperature is 0.3 — low enough for consistent format, not so low that 
every review reads identically.

**Score extraction**

The prompt guarantees the score appears as X/10 on its own line. 
The code scans each line for "/10" and pulls the number.

**GitHub integration**

Uses the official GitHub REST API, not scraping. Returns file content as 
clean JSON. Filters by file extension, takes the first 5 code files from root, 
reviews each one.

**Request validation**

Pydantic validates every incoming request. Empty code field returns a 422 
with a clear message instead of a Python traceback.

---

## Tech stack

- Python
- FastAPI — REST API backend
- Pydantic — request validation
- Groq (LLaMA 3.3 70B) — code review LLM
- GitHub REST API — repo file fetching
- Streamlit — frontend (two tabs)
- python-dotenv — API key management

---

## API endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | /review/code | Reviews pasted code |
| POST | /review/github | Reviews files from a GitHub repo |
| GET | /health | Health check |

---

## Numbers

| What | Value |
|------|-------|
| Languages supported | 8 (Python, JS, TS, Java, C++, Go, Rust, auto-detect) |
| Max GitHub files per review | 5 |
| LLM model | LLaMA 3.3 70B via Groq |
| Temperature | 0.3 |
| Max tokens | 2000 |
| Review time | 10-15 seconds per file |
| API cost | Zero — Groq free tier |

---

## Limitations

- Needs two terminals to run locally — FastAPI on 8000, Streamlit on 8501. 
  Docker Compose would fix this.
- Score extraction breaks if the LLM writes "seven out of ten" instead of "7/10". 
  Fix is JSON mode or structured outputs.
- Only reviews root-level files in GitHub repos. Most real repos have 
  code in subdirectories.
- No auth on the API — anyone who finds the URL can drain the Groq quota.
- LLM reviews can be wrong. This assists code review, it doesn't replace it.

---

## What I'd add next

- Async FastAPI endpoints so concurrent reviews don't block each other
- Caching by code hash so the same snippet isn't reviewed twice
- Recursive GitHub file listing with depth limit for real repo structure
- Private repo support via GitHub OAuth
- Docker Compose to run both servers with one command

---

## Why Groq and not Gemini

Had significant quota and permission issues with Gemini on deployed apps. 
Groq is completely free, higher rate limits, and LLaMA 3.3 70B gives 
comparable quality for code review tasks.
