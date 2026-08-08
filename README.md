# AI Code Reviewer

An AI-powered code review tool that instantly analyzes any code for bugs, security vulnerabilities, and best practices — like having a senior developer review your code in seconds.

## What it does

Most developers either skip code review or wait days for a senior to review their code. This tool automates that process completely.

You paste any code or enter a GitHub repository URL, and the AI reviews it across three dimensions:

- **Bugs** — logical errors, runtime errors, edge cases not handled
- **Security Issues** — SQL injection, hardcoded passwords, input validation gaps
- **Best Practices** — naming conventions, code structure, missing error handling

It then provides a fully corrected version of the code and a quality score out of 10 with reasoning.

## Features

- Paste code directly for instant review
- Enter any public GitHub repository URL to review all code files automatically
- Supports Python, JavaScript, TypeScript, Java, C++, Go and more
- Returns structured review with bugs, security issues, best practices and improved code
- Scores code quality out of 10
- Private repository detection with clear error messaging
- REST API with auto-generated Swagger documentation at `/docs`
- Dark themed developer-friendly UI

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| LLM | Groq API (LLaMA 3.3 70B) | AI code analysis and review generation |
| Backend | FastAPI | REST API with automatic documentation |
| Frontend | Streamlit | Web UI for code input and results display |
| GitHub Integration | GitHub REST API | Fetch and parse public repository files |
| Validation | Pydantic | Request and response data validation |
| Security | python-dotenv | Secure API key management |

## Project Structure
