import streamlit as st
import google.generativeai as genai
import re

# Configure Google AI API
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-pro')

def review_code(code):
    prompt = f"""
    Review the following Python code for bugs. Provide:
    1. A bug report describing each bug found.
    2. The complete fixed code for all bugs.

    Format your response exactly as follows:
    BUG REPORT:
    [List each bug with a brief description]

    FIXED CODE:
    ```python
    [The entire fixed code, not just the changed parts]
    ```

    If no bugs are found, state "No bugs found in the provided code." under BUG REPORT and repeat the original code under FIXED CODE.

    Code to review:
    {code}
    """
    
    response = model.generate_content(prompt)
    return response.text

def split_feedback(feedback):
    # Split the feedback into bug report and fixed code
    parts = re.split(r'FIXED CODE:', feedback, flags=re.IGNORECASE)
    bug_report = parts[0].replace("BUG REPORT:", "").strip()
    fixed_code = parts[1].strip() if len(parts) > 1 else "No fixed code provided."
    
    # Remove the ```python and ``` from the fixed code
    fixed_code = re.sub(r'```python\s*|\s*```', '', fixed_code).strip()
    
    return bug_report, fixed_code


st.title("AI Code Reviewer")

user_code = st.text_area("Enter your Python code here:")

if st.button("Generate"):
    if user_code:
        with st.spinner("Analyzing code..."):
            feedback = review_code(user_code)
            bug_report, fixed_code = split_feedback(feedback)
            
            st.subheader("Bug Report:")
            st.write(bug_report)
            
            st.subheader("Fixed Code:")
            st.code(fixed_code, language="python")
    else:
        st.warning("Please enter some code to review.")

