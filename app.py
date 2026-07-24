import streamlit as st
import requests

st.set_page_config(
    page_title="AI Code Reviewer",
    layout="centered"
)

API_URL = "http://localhost:8000"

st.title("AI Code Reviewer")
st.caption("Review your code for bugs, security issues and best practices")

st.divider()

tab1, tab2 = st.tabs(["Paste Code", "GitHub URL"])

with tab1:
    language = st.selectbox(
        "Programming Language",
        ["auto", "Python", "JavaScript", "TypeScript", "Java", "C++", "Go"],
        index=0
    )

    code = st.text_area(
        "Paste your code here",
        height=300,
        placeholder="def hello():\n    print('Hello World')"
    )

    if st.button("Review Code", type="primary", use_container_width=True):
        if not code.strip():
            st.warning("Please paste some code first.")
        else:
            with st.spinner("Reviewing your code..."):
                try:
                    response = requests.post(
                        f"{API_URL}/review/code",
                        json={"code": code, "language": language}
                    )
                    if response.status_code == 200:
                        result = response.json()["result"]
                        st.success("Review complete!")
                        st.divider()
                        st.subheader("Review Results")
                        st.markdown(result["review"])
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Something went wrong')}")
                except Exception as e:
                    st.error(f"Could not connect to API: {str(e)}")

with tab2:
    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository"
    )

    if st.button("Review GitHub Repo", type="primary", use_container_width=True):
        if not github_url.strip():
            st.warning("Please enter a GitHub URL.")
        else:
            with st.spinner("Fetching and reviewing code from GitHub..."):
                try:
                    response = requests.post(
                        f"{API_URL}/review/github",
                        json={"github_url": github_url}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Reviewed repo: {data['repo']}")
                        st.divider()
                        for filename, review in data["reviews"].items():
                            with st.expander(f"📄 {filename}"):
                                st.markdown(review["review"])
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Something went wrong')}")
                except Exception as e:
                    st.error(f"Could not connect to API: {str(e)}")

st.divider()
st.markdown(
    "<div style='text-align: right; color: #555; font-size: 0.8rem;'>Built with FastAPI · Groq · GitHub API · Streamlit &nbsp;|&nbsp; Made by <b>Prathamesh Jadhav</b></div>",
    unsafe_allow_html=True
)