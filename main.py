from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from reviewer import review_code
from github_fetch import fetch_code_from_github

app = FastAPI(
    title="AI Code Reviewer",
    description="Review code for bugs, security issues and best practices using AI",
    version="1.0.0"
)

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "auto"

class GitHubReviewRequest(BaseModel):
    github_url: str
    language: str = "auto"

@app.get("/")
def root():
    return {"message": "AI Code Reviewer API is running"}

@app.post("/review/code")
def review_code_endpoint(request: CodeReviewRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    try:
        result = review_code(request.code, request.language)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review/github")
def review_github_endpoint(request: GitHubReviewRequest):
    if not request.github_url.strip():
        raise HTTPException(status_code=400, detail="GitHub URL cannot be empty")
    try:
        repo_data = fetch_code_from_github(request.github_url)
        reviews = {}
        for filename, code in repo_data["files"].items():
            reviews[filename] = review_code(code, request.language)
        return {
            "status": "success",
            "repo": f"{repo_data['owner']}/{repo_data['repo']}",
            "reviews": reviews
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}