import os
import re

files_to_fix = [
    'ui/layout/header.py',
    'ui/components/cards.py',
    'ui/pages/trends.py',
    'ui/pages/emerging_risks.py',
    'ui/pages/recommendations.py',
    'ui/pages/portfolio.py'
]

for file in files_to_fix:
    with open(file, 'r') as f:
        content = f.read()

    # Add import re if not present
    if 'import re' not in content:
        content = content.replace('import streamlit as st', 'import streamlit as st\nimport re')

    # Replace st.markdown(textwrap.dedent(...) with st.markdown(re.sub(r'^[ \t]+', '', ..., flags=re.MULTILINE)
    content = re.sub(
        r'st\.markdown\(textwrap\.dedent\((.*?)\),\s*unsafe_allow_html=True\)',
        r"st.markdown(re.sub(r'^[ \\t]+', '', \1, flags=re.MULTILINE), unsafe_allow_html=True)",
        content,
        flags=re.DOTALL
    )

    with open(file, 'w') as f:
        f.write(content)

