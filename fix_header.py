import re

with open('ui/layout/header.py', 'r') as f:
    content = f.read()

# Remove textwrap.dedent
content = content.replace('textwrap.dedent(\n        f"""', 'f"""')
content = content.replace('textwrap.dedent(', '')
content = content.replace('""",\n        unsafe_allow_html=True\n    )', '"""\n    st.markdown(html_str, unsafe_allow_html=True)')
content = content.replace('st.markdown(\n        f"""', 'html_str = f"""')
content = content.replace('st.markdown(\nf"""', 'html_str = f"""')
content = content.replace('st.markdown(f"""', 'html_str = f"""')
content = content.replace('st.markdown("""', 'html_str = """')
# Wait, the best way to remove newlines from the f-string is just to use a python script to parse it or just use re.sub on the string variable.

with open('ui/layout/header.py', 'w') as f:
    f.write(content)
