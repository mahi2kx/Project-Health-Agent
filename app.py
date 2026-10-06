"""
Project Health Reporting Agent — Main Application
==================================================
Enterprise PMO Dashboard (v2.0)
"""

import os
from dotenv import load_dotenv

load_dotenv()
_api_key = os.getenv("OPENAI_API_KEY")
if _api_key:
    try:
        from services.llm_client import create_llm_client
        _client = create_llm_client()
    except Exception:
        pass

import streamlit as st

# Set up page configuration FIRST before any other st commands
st.set_page_config(
    page_title="Project Health Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# UI Imports
from ui.theme.styles import apply_enterprise_styles
from ui.layout.sidebar import render_sidebar
from ui.pages.upload import render_upload_page
from ui.pages.explorer import render_explorer_page
from ui.pages.dashboard import render_dashboard_page
from ui.pages.portfolio import render_portfolio_page
from ui.pages.trends import render_trends_page
from ui.pages.emerging_risks import render_emerging_risks_page
from ui.pages.recommendations import render_recommendations_page
from ui.pages.reports import render_reports_page

def main():
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'upload'
        
    # Apply Enterprise Custom CSS
    apply_enterprise_styles()
    
    # Render global sidebar navigation
    render_sidebar()
    
    # Page Routing
    page = st.session_state.current_page
    
    if page == 'upload':
        render_upload_page()
    elif page == 'explorer':
        render_explorer_page()
    elif page == 'dashboard':
        render_dashboard_page()
    elif page == 'portfolio':
        render_portfolio_page()
    elif page == 'trends':
        render_trends_page()
    elif page == 'risks':
        render_emerging_risks_page()
    elif page == 'recommendations':
        render_recommendations_page()
    elif page == 'reports':
        render_reports_page()
    else:
        render_upload_page()

if __name__ == "__main__":
    main()
