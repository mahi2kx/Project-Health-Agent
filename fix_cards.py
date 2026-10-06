import re

with open('ui/components/cards.py', 'r') as f:
    content = f.read()

if 'import textwrap' not in content:
    content = content.replace('import streamlit as st', 'import streamlit as st\nimport textwrap')

# Replace st.markdown(html, unsafe_allow_html=True)
content = content.replace('st.markdown(html, unsafe_allow_html=True)', 'st.markdown(textwrap.dedent(html), unsafe_allow_html=True)')

with open('ui/components/cards.py', 'w') as f:
    f.write(content)
