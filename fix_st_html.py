import re
import os

files_to_fix = [
    'ui/layout/header.py',
    'ui/components/cards.py',
    'ui/pages/trends.py',
    'ui/pages/emerging_risks.py',
    'ui/pages/recommendations.py',
    'ui/pages/portfolio.py'
]

for filepath in files_to_fix:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We want to replace st.markdown(..., unsafe_allow_html=True) with st.html(...)
    # Since we previously used .replace("\n", ""), we will also remove that.
    
    # 1. Replace st.markdown(something.replace("\n", ""), unsafe_allow_html=True) 
    #    with st.html(something)
    content = re.sub(
        r'st\.markdown\((.*?)\.replace\("\\n",\s*""\),\s*unsafe_allow_html=True\)', 
        r'st.html(\1)', 
        content
    )
    
    # 2. Replace any leftover st.markdown(something, unsafe_allow_html=True)
    content = re.sub(
        r'st\.markdown\((.*?),\s*unsafe_allow_html=True\)', 
        r'st.html(\1)', 
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Done")
