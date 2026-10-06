def render_header():
    """Display the branded application header."""
    st.markdown('\n        <div class="app-header">\n            <h1>📊 Project Health Reporting Agent</h1>\n            <p>\n                Upload project plans · Evaluate health (RAG) ·\n                AI-powered insights · Executive-ready reports\n            </p>\n        </div>\n        ', unsafe_allow_html=True)