def render_portfolio_page():
    """Render the portfolio analysis page."""
    st.subheader('📈 Portfolio Overview')
    if 'portfolio_analytics' in st.session_state and st.session_state['portfolio_analytics']:
        pa: PortfolioAnalyticsResult = st.session_state['portfolio_analytics']
        dist = pa.portfolio_health_distribution
        c1, c2, c3, c4 = st.columns(4)
        c1.metric('Total Projects', dist.total_projects)
        c2.metric('🟢 Green', f'{dist.green_count} ({dist.green_percent}%)')
        c3.metric('🟡 Amber', f'{dist.amber_count} ({dist.amber_percent}%)')
        c4.metric('🔴 Red', f'{dist.red_count} ({dist.red_percent}%)')
        st.markdown(f'**Portfolio Summary:** {pa.portfolio_summary}')
        if pa.executive_summary:
            st.info(f'**Executive Briefing:** {pa.executive_summary}')
        t_attn, t_trends, t_risks, t_blockers = st.tabs(['🚨 Executive Attention List', '📈 Trends & Trajectories', '⚠️ Top Risks', '🛑 Active Blockers'])
        with t_attn:
            if pa.executive_attention_list:
                for item in pa.executive_attention_list:
                    st.markdown(f'### `[{item.priority.upper()}]` {item.project_name} ({item.current_rag})')
                    st.markdown(f'**Reason:** {item.reason_for_escalation}')
                    st.markdown(f'**Impact:** {item.business_impact}')
                    st.divider()
            else:
                st.success('No projects currently require executive escalation.')
        with t_trends:
            if pa.trend_analysis:
                for t in pa.trend_analysis:
                    st.markdown(f'- **[{t.category}] {t.trend_name}** (Impacts {t.affected_project_count} projects): {t.description}')
            else:
                st.info('No cross-project trends detected.')
        with t_risks:
            if pa.risk_analysis:
                for r in pa.risk_analysis:
                    st.markdown(f"- **[{r.severity}] {r.risk_title}** ({r.frequency} occurrences across: {', '.join(r.affected_projects)})")
            else:
                st.info('No major portfolio risks aggregated.')
        with t_blockers:
            if pa.blocker_analysis:
                for b in pa.blocker_analysis:
                    st.markdown(f'- **{b.blocker_title}** ({b.category}, {b.frequency} occurrences): {b.business_impact}')
            else:
                st.info('No active blockers detected across portfolio.')
    else:
        st.info('When multiple projects are analyzed, this page will display portfolio-wide health distribution, trends, recurring risks, and projects requiring executive attention.', icon='ℹ️')
        st.markdown('<div class="section-card"><p>Portfolio analytics will be generated after project plans have been analyzed.</p></div>', unsafe_allow_html=True)