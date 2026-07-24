import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def review_code(code: str, language: str = "auto") -> dict:
    prompt = f"""You are an expert code reviewer. Review the following {language} code and provide detailed feedback.

Analyze the code for:
1. Bugs - logical errors, runtime errors, edge cases not handled
2. Security Issues - vulnerabilities, unsafe practices, injection risks
3. Best Practices - code style, naming conventions, code smells

Code to review:
{code}

Respond in this exact format:

## Summary
Write 2-3 sentence overall assessment here

## Bugs Found
List each bug with line reference and explanation. Write No bugs found if clean.

## Security Issues
List each security issue with explanation. Write No security issues found if clean.

## Best Practices
List improvements for code quality, readability, structure.

## Improved Code
Provide the corrected and improved version of the code here.

## Score
Give a score out of 10 with one line reason.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000
    )

    review_text = response.choices[0].message.content

    score = "N/A"
    for line in review_text.split('\n'):
        if '/10' in line:
            score = line.strip()
            break

    return {
        "review": review_text,
        "score": score,
        "language": language
    }


if __name__ == "__main__":
    test_code = """
def divide(a, b):
    return a / b

password = "admin123"
user_input = input("Enter name: ")
query = "SELECT * FROM users WHERE name = " + user_input

result = divide(10, 0)
print(result)
"""

    print("Testing code reviewer...")
    result = review_code(test_code, "Python")
    print(result["review"])
    print(f"\nScore: {result['score']}")