import re

with open('ui/components/cards.py', 'r') as f:
    content = f.read()

# Replace all occurrences of broken imports inside the file
# We know they look like:
#    import streamlit as st
#import re
#import textwrap
content = content.replace('    import streamlit as st\nimport re\nimport textwrap', '    import streamlit as st')
content = content.replace('    import streamlit as st\nimport textwrap', '    import streamlit as st')
content = content.replace('    import streamlit as st\nimport re', '    import streamlit as st')
# Also remove them if they happen to be 8 spaces indented:
content = content.replace('        import streamlit as st\nimport re\nimport textwrap', '        import streamlit as st')
content = content.replace('        import streamlit as st\nimport textwrap', '        import streamlit as st')
content = content.replace('        import streamlit as st\nimport re', '        import streamlit as st')

with open('ui/components/cards.py', 'w') as f:
    f.write(content)

