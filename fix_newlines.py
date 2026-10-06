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
    
    # We will replace all occurrences of `unsafe_allow_html=True)` 
    # with `.replace('\n', ''), unsafe_allow_html=True)`
    # Actually, we can just replace the string generation or replace it at the markdown call.
    
    content = re.sub(
        r'st\.markdown\((.*?),\s*unsafe_allow_html=True\)', 
        r'st.markdown(\1.replace("\\n", ""), unsafe_allow_html=True)', 
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Done")
