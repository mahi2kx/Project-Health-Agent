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
    
    # We want to find all occurrences of st.markdown(..., unsafe_allow_html=True)
    # Since they could span multiple lines, let's use a robust approach:
    # We will just strip leading whitespace from EVERY line in the file that looks like HTML
    # Actually, simpler: write a regex that finds lines starting with spaces followed by '<' 
    # and removes those leading spaces, but only inside triple quotes.
    
    # Even simpler: Just replace all sequences of \n followed by spaces followed by <
    # with \n<
    
    new_content = re.sub(r'\n[ \t]+<', '\n<', content)
    
    with open(filepath, 'w') as f:
        f.write(new_content)

print("Done")
