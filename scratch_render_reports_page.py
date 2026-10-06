def render_reports_page():
    """Render the reports and presentations page."""
    st.subheader('📄 Generated Reports')
    left, right = st.columns(2)
    with left:
        st.markdown('\n            <div class="section-card">\n                <h3>📝 Weekly Health Report</h3>\n                <p>\n                    A structured project health report including RAG status,\n                    health indicators, AI reasoning, risks, and recommendations.\n                </p>\n            </div>\n            ', unsafe_allow_html=True)
        if 'analyzed_projects' in st.session_state and st.session_state['analyzed_projects']:
            proj_names = list(st.session_state['analyzed_projects'].keys())
            sel_report_proj = st.selectbox('Select Project for Report', options=proj_names, key='sel_rep_proj')
            report_md = st.session_state['analyzed_projects'][sel_report_proj].get('weekly_report_md', '')
            if report_md:
                st.download_button(label='📥 Download Weekly Report (.md)', data=report_md, file_name=f'{sel_report_proj}_Weekly_Report.md', mime='text/markdown', use_container_width=True, type='primary')
                with st.expander('Preview Weekly Report', expanded=True):
                    st.markdown(report_md)
            else:
                st.button('📥 Download Weekly Report', disabled=True, use_container_width=True)
        else:
            st.button('📥 Download Weekly Report', disabled=True, use_container_width=True)
    with right:
        st.markdown('\n            <div class="section-card">\n                <h3>📊 Executive Presentation</h3>\n                <p>\n                    An auto-generated 5–7 slide PowerPoint deck summarizing\n                    portfolio health, emerging risks, trends, and strategic\n                    recommendations for leadership.\n                </p>\n            </div>\n            ', unsafe_allow_html=True)
        if 'pptx_presentation' in st.session_state and st.session_state['pptx_presentation'] and st.session_state['pptx_presentation'].success:
            pptx_obj = st.session_state['pptx_presentation']
            try:
                with open(pptx_obj.file_path, 'rb') as f:
                    pptx_bytes = f.read()
                st.download_button(label='📥 Download Executive PPT (.pptx)', data=pptx_bytes, file_name=Path(pptx_obj.file_path).name, mime='application/vnd.openxmlformats-officedocument.presentationml.presentation', use_container_width=True, type='primary')
                with st.expander('Slide Deck Summary & Structure', expanded=True):
                    st.markdown(f'**Summary:** {pptx_obj.presentation_summary}')
                    for sm in pptx_obj.slides_metadata:
                        st.markdown(f'- **Slide {sm.slide_number}:** {sm.title} *(Type: {sm.slide_type})*')
            except Exception as e:
                st.error(f'Error reading presentation file: {e}')
        else:
            st.button('📥 Download Executive PPT', disabled=True, use_container_width=True)