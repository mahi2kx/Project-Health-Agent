def render_sidebar():
    """Render the sidebar with navigation and module status placeholders."""
    with st.sidebar:
        st.markdown('## 📊 Health Agent')
        st.caption('AI-Powered Project Reporting')
        st.divider()
        st.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)
        page = st.radio(label='Navigate', options=['🏠  Dashboard', '📁  Upload & Analyze', '📈  Portfolio View', '📄  Reports'], label_visibility='collapsed')
        st.divider()
        st.markdown('<p class="sidebar-title">Module Status</p>', unsafe_allow_html=True)
        is_analyzed = 'analyzed_projects' in st.session_state and bool(st.session_state['analyzed_projects'])
        has_portfolio = 'portfolio_analytics' in st.session_state and bool(st.session_state['portfolio_analytics'])
        modules = {'File Upload': 'Ready', 'Excel Reader': 'Ready', 'Data Validator': 'Ready', 'Health Indicators': 'Ready' if is_analyzed else 'Pending', 'AI Reasoning': 'Ready' if is_analyzed else 'Pending', 'RAG Engine': 'Ready' if is_analyzed else 'Pending', 'Recommendations': 'Ready' if is_analyzed else 'Pending', 'Report Generator': 'Ready' if is_analyzed else 'Pending', 'Portfolio Analyzer': 'Ready' if has_portfolio else 'Pending', 'PPT Generator': 'Ready' if has_portfolio else 'Pending'}
        for module_name, status in modules.items():
            badge_class = 'badge-ready' if status == 'Ready' else 'badge-pending'
            st.markdown(f'{module_name} &nbsp; <span class="status-badge {badge_class}">{status}</span>', unsafe_allow_html=True)
        st.divider()
        st.markdown('<p class="sidebar-title">About</p>', unsafe_allow_html=True)
        st.caption('Version 0.1.0')
        st.caption('Python 3.13 · Streamlit · OpenAI')
    return page