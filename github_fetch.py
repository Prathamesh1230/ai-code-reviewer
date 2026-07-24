import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def parse_github_url(url: str) -> tuple:
    url = url.strip().rstrip("/")
    if "github.com" not in url:
        raise ValueError("Not a valid GitHub URL")
    parts = url.split("github.com/")[-1].split("/")
    if len(parts) < 2:
        raise ValueError("URL must include owner and repo name")
    owner = parts[0]
    repo = parts[1]
    return owner, repo


def get_repo_files(owner: str, repo: str, path: str = "") -> list:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        raise Exception("Repository not found. Please check the URL is correct and the repository is public. Private repositories are not supported.")
    elif response.status_code == 401:
        raise Exception("Authentication failed. Please check your GitHub token.")
    elif response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.json().get('message', '')}")
    return response.json()


def get_file_content(download_url: str) -> str:
    response = requests.get(download_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Could not download file content")
    return response.text


def fetch_code_from_github(github_url: str, max_files: int = 5) -> dict:
    owner, repo = parse_github_url(github_url)

    files = get_repo_files(owner, repo)

    code_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs']
    code_files = []

    for f in files:
        if f['type'] == 'file':
            if any(f['name'].endswith(ext) for ext in code_extensions):
                code_files.append(f)

    if not code_files:
        raise Exception("No code files found in this repository root")

    results = {}
    for f in code_files[:max_files]:
        content = get_file_content(f['download_url'])
        results[f['name']] = content

    return {
        "owner": owner,
        "repo": repo,
        "files": results
    }


if __name__ == "__main__":
    url = input("Enter GitHub repo URL: ")
    result = fetch_code_from_github(url)
    print(f"\nRepo: {result['owner']}/{result['repo']}")
    print(f"Files found: {list(result['files'].keys())}")
    for name, content in result['files'].items():
        print(f"\n--- {name} ---")
        print(content[:200])