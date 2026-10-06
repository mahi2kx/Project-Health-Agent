def render_dashboard():
    """Render the dashboard page with summary metric cards."""
    if 'portfolio_analytics' in st.session_state and st.session_state['portfolio_analytics']:
        pa = st.session_state['portfolio_analytics']
        dist = pa.portfolio_health_distribution
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label='Projects Analyzed', value=f'{dist.total_projects}')
        col2.metric(label='🟢 Green', value=f'{dist.green_count} ({dist.green_percent}%)')
        col3.metric(label='🟡 Amber', value=f'{dist.amber_count} ({dist.amber_percent}%)')
        col4.metric(label='🔴 Red', value=f'{dist.red_count} ({dist.red_percent}%)')
    elif 'analyzed_projects' in st.session_state and st.session_state['analyzed_projects']:
        projs = st.session_state['analyzed_projects']
        total = len(projs)
        g = sum((1 for p in projs.values() if p['decision'].overall_rag.value.lower() == 'green'))
        a = sum((1 for p in projs.values() if p['decision'].overall_rag.value.lower() == 'amber'))
        r = sum((1 for p in projs.values() if p['decision'].overall_rag.value.lower() == 'red'))
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label='Projects Analyzed', value=f'{total}')
        col2.metric(label='🟢 Green', value=f'{g}')
        col3.metric(label='🟡 Amber', value=f'{a}')
        col4.metric(label='🔴 Red', value=f'{r}')
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label='Projects Analyzed', value='—')
        col2.metric(label='🟢 Green', value='—')
        col3.metric(label='🟡 Amber', value='—')
        col4.metric(label='🔴 Red', value='—')
    st.markdown('---')
    left, right = st.columns(2)
    with left:
        st.markdown('\n            <div class="section-card">\n                <h3>🚀 Getting Started</h3>\n                <p>\n                    Upload one or more project plan spreadsheets (.xlsx) to begin\n                    automated health analysis. The agent will extract tasks,\n                    milestones, risks, and comments to determine each project\'s\n                    RAG status.\n                </p>\n            </div>\n            ', unsafe_allow_html=True)
    with right:
        st.markdown('\n            <div class="section-card">\n                <h3>📋 What You Get</h3>\n                <p>\n                    • Overall RAG status with AI reasoning<br>\n                    • Identified risks and blockers<br>\n                    • Actionable recommendations<br>\n                    • Weekly health reports<br>\n                    • Executive PowerPoint presentations\n                </p>\n            </div>\n            ', unsafe_allow_html=True)