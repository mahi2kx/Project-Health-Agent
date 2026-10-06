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
    
    # We want to replace st.html(re.sub(r'^[ \t]+', '', html, flags=re.MULTILINE))
    # with st.html(html)
    content = re.sub(
        r'st\.html\(re\.sub\(r\'\^\[ \\t\]\+\', \'\', (.*?), flags=re\.MULTILINE\)\)', 
        r'st.html(\1)', 
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Done")
