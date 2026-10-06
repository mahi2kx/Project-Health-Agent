def main():
    """Application entry point — applies styles and routes to the active page."""
    apply_custom_styles()
    selected_page = render_sidebar()
    render_header()
    if selected_page == '🏠  Dashboard':
        render_dashboard()
    elif selected_page == '📁  Upload & Analyze':
        render_upload_page()
    elif selected_page == '📈  Portfolio View':
        render_portfolio_page()
    elif selected_page == '📄  Reports':
        render_reports_page()