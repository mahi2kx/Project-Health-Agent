import re
import os

files = ['ui/pages/trends.py', 'ui/pages/emerging_risks.py', 'ui/pages/recommendations.py']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    if 'import textwrap' not in content:
        content = content.replace('import streamlit as st', 'import streamlit as st\nimport textwrap')

    # Find st.markdown(..., unsafe_allow_html=True)
    # Using a simple regex to wrap the first argument in textwrap.dedent
    content = re.sub(r'st\.markdown\((.*?),\s*unsafe_allow_html=True\)', r'st.markdown(textwrap.dedent(\1), unsafe_allow_html=True)', content)

    with open(file, 'w') as f:
        f.write(content)
