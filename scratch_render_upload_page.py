def render_upload_page():
    """Render the file upload page with validation and metadata display."""
    st.subheader('📁 Upload Project Plans')
    st.info('Upload one or more Excel files (.xlsx) containing your project plans. The agent will validate, extract, and analyze project health automatically.', icon='ℹ️')
    uploaded_files = st.file_uploader('Choose Excel files', type=['xlsx'], accept_multiple_files=True, help='Supported format: Microsoft Excel (.xlsx). Max 50 MB per file.')
    if uploaded_files:
        results = process_uploads(uploaded_files)
        valid = get_valid_uploads()
        invalid = get_invalid_uploads()
        if valid:
            st.success(f'{len(valid)} file(s) uploaded and validated successfully.', icon='✅')
        if invalid:
            for f_info in invalid:
                st.error(f'❌ **{f_info.filename}** — {f_info.error}', icon='🚫')
        st.markdown('#### 📋 Uploaded Files')
        table_header = '| # | Filename | Size | Uploaded At | Status |\n|---|----------|------|-------------|--------|\n'
        table_rows = ''
        for idx, f_info in enumerate(results, start=1):
            status_icon = '✅' if f_info.status == 'Uploaded' else '❌'
            table_rows += f'| {idx} | 📄 {f_info.filename} | {f_info.size_display} | {f_info.uploaded_at_display} | {status_icon} {f_info.status} |\n'
        st.markdown(table_header + table_rows)
        col_analyze, col_clear = st.columns([3, 1])
        with col_analyze:
            analyze_disabled = not has_uploads()
            if st.button('🔍 Analyze Projects', type='primary', use_container_width=True, disabled=analyze_disabled):
                with st.spinner('Executing end-to-end AI project health pipeline...'):
                    valid_infos = get_valid_uploads()
                    valid_files = [f for f in uploaded_files if any((info.filename == f.name for info in valid_infos))]
                    analyzed_projects = {}
                    weekly_reports = []
                    engine = HealthIndicatorEngine()
                    sentiment_agent = StakeholderSentimentAgent()
                    rag_agent = RAGDecisionAgent()
                    rca_agent = RootCauseAnalysisAgent()
                    rec_agent = RecommendationAgent()
                    report_generator = WeeklyReportGenerator()
                    for file in valid_files:
                        wb_info = read_workbook(file)
                        sheet_list = wb_info.sheet_names if wb_info else []
                        if not sheet_list:
                            continue
                        sheet_name = next((s for s in sheet_list if not wb_info.get_worksheet(s).is_empty), sheet_list[0])
                        sheet_df = read_sheet_dataframe(file, sheet_name)
                        schema = detect_schema(sheet_df, sheet_name)
                        norm_result = normalize_dataframe(sheet_df, schema)
                        cmt_result = extract_comments(file, sheet_list, normalized_df=norm_result.normalized_df)
                        st.session_state[f'comments_{file.name}'] = cmt_result
                        comments_input = cmt_result.to_ai_input() if cmt_result.has_comments else []
                        p_info = ProjectInfo(project_name=file.name, comments=comments_input)
                        project_obj = Project(project_name=file.name, comments=comments_input)
                        st.session_state['project_objects'] = st.session_state.get('project_objects', {})
                        st.session_state['project_objects'][file.name] = project_obj
                        st.session_state['uploaded_workbooks'] = st.session_state.get('uploaded_workbooks', {})
                        st.session_state['uploaded_workbooks'][file.name] = wb_info
                        st.session_state['projects'] = st.session_state.get('projects', {})
                        st.session_state['projects'][file.name] = norm_result.normalized_df
                        scorecard = engine.evaluate(norm_result.normalized_df, project_name=file.name, comments=comments_input)
                        st.session_state['scorecards'] = st.session_state.get('scorecards', {})
                        st.session_state['scorecards'][file.name] = scorecard
                        sentiment = sentiment_agent.analyze(comments=comments_input, project_name=file.name)
                        st.session_state['ai_analyses'] = st.session_state.get('ai_analyses', {})
                        st.session_state['ai_analyses'][file.name] = sentiment
                        decision = rag_agent.decide(scorecard, sentiment)
                        st.session_state['rag_results'] = st.session_state.get('rag_results', {})
                        st.session_state['rag_results'][file.name] = decision
                        rca = rca_agent.analyze(scorecard, decision, comments=comments_input)
                        recs = rec_agent.generate(scorecard, decision, rca, comments=comments_input)
                        st.session_state['recommendations'] = st.session_state.get('recommendations', {})
                        st.session_state['recommendations'][file.name] = recs
                        weekly_report_obj = report_generator.build_report_data(p_info, scorecard, decision, rca, recs)
                        weekly_report_md = report_generator.generate_report(p_info, scorecard, decision, rca, recs, format_type='markdown')
                        weekly_reports.append(weekly_report_obj)
                        st.session_state['weekly_reports'] = st.session_state.get('weekly_reports', {})
                        st.session_state['weekly_reports'][file.name] = weekly_report_md
                        analyzed_projects[file.name] = {'scorecard': scorecard, 'sentiment': sentiment, 'decision': decision, 'rca': rca, 'recommendations': recs, 'weekly_report_obj': weekly_report_obj, 'weekly_report_md': weekly_report_md, 'project': project_obj, 'project_info': p_info}
                    st.session_state['analyzed_projects'] = analyzed_projects
                    if weekly_reports:
                        portfolio_engine = PortfolioAnalyticsEngine()
                        portfolio_result = portfolio_engine.analyze(weekly_reports)
                        st.session_state['portfolio_analytics'] = portfolio_result
                        pptx_gen = ExecutivePowerPointGenerator()
                        pptx_result = pptx_gen.generate(portfolio_result)
                        st.session_state['pptx_presentation'] = pptx_result
                        st.session_state['pptx_path'] = pptx_result.file_path
                st.success('✅ Analysis Complete! All modules executed successfully.')
                st.rerun()
        with col_clear:
            if st.button('🗑️ Clear All', use_container_width=True):
                clear_uploads()
                st.rerun()
    else:
        st.markdown('\n            <div class="section-card" style="text-align:center; padding:2.5rem;">\n                <h3 style="color:#94a3b8;">📂 No files uploaded yet</h3>\n                <p>Drag and drop Excel files above, or click <b>Browse files</b> to begin.</p>\n            </div>\n            ', unsafe_allow_html=True)
    st.markdown('---')
    if uploaded_files and has_uploads():
        st.subheader('📖 Workbook Explorer')
        valid_files = [f for f in uploaded_files if any((info.filename == f.name and info.status == 'Uploaded' for info in results))]
        if not valid_files:
            st.caption('No valid workbooks to explore.')
        else:
            file_names = [f.name for f in valid_files]
            selected_file_name = st.selectbox('Select a workbook to explore', options=file_names, key='workbook_selector')
            selected_file = next((f for f in valid_files if f.name == selected_file_name))
            cache_key = f'workbook_info_{selected_file_name}'
            if cache_key not in st.session_state:
                with st.spinner(f'Reading {selected_file_name}...'):
                    st.session_state[cache_key] = read_workbook(selected_file)
            wb_info = st.session_state[cache_key]
            if wb_info.has_errors:
                for err in wb_info.errors:
                    st.error(err, icon='⚠️')
            m1, m2, m3 = st.columns(3)
            m1.metric('Workbook', wb_info.filename)
            m2.metric('Worksheets', wb_info.sheet_count)
            non_empty = len(wb_info.get_non_empty_sheets())
            m3.metric('Non-Empty Sheets', non_empty)
            st.markdown('---')
            if wb_info.sheet_names:
                selected_sheet = st.selectbox('Select a worksheet to inspect', options=wb_info.sheet_names, format_func=lambda s: wb_info.worksheets[s].summary, key='sheet_selector')
                ws_info = wb_info.get_worksheet(selected_sheet)
                if ws_info and (not ws_info.is_empty):
                    c1, c2, c3 = st.columns(3)
                    c1.metric('Rows', f'{ws_info.num_rows:,}')
                    c2.metric('Columns', ws_info.num_columns)
                    c3.metric('Status', 'Has Data' if not ws_info.is_empty else 'Empty')
                    with st.expander(f'📋 Column Names ({ws_info.num_columns} columns)', expanded=True):
                        cols_per_row = 4
                        for row_start in range(0, len(ws_info.column_names), cols_per_row):
                            row_cols = st.columns(cols_per_row)
                            for i, col_widget in enumerate(row_cols):
                                idx = row_start + i
                                if idx < len(ws_info.column_names):
                                    col_widget.code(ws_info.column_names[idx], language=None)
                    st.markdown('#### 🔬 Data Preview')
                    df_cache_key = f'sheet_df_{selected_file_name}_{selected_sheet}'
                    if df_cache_key not in st.session_state:
                        with st.spinner('Loading sheet data...'):
                            st.session_state[df_cache_key] = read_sheet_dataframe(selected_file, selected_sheet)
                    sheet_df = st.session_state[df_cache_key]
                    if sheet_df.empty:
                        st.warning('Could not read sheet data.', icon='⚠️')
                    else:
                        preview_cache_key = f'preview_{selected_file_name}_{selected_sheet}'
                        if preview_cache_key not in st.session_state:
                            st.session_state[preview_cache_key] = generate_data_preview(sheet_df, selected_sheet)
                        preview = st.session_state[preview_cache_key]
                        tab_rows, tab_types, tab_missing, tab_stats = st.tabs(['📄 First 10 Rows', '🧮 Data Types', '❓ Missing Values', '📊 Statistics'])
                        with tab_rows:
                            st.dataframe(preview.preview_df, use_container_width=True, hide_index=False)
                            st.caption(f'Showing {len(preview.preview_df)} of {preview.total_rows:,} rows')
                        with tab_types:
                            st.dataframe(preview.dtype_df, use_container_width=True, hide_index=True)
                            st.caption(f'{preview.total_columns} columns total')
                        with tab_missing:
                            missing = preview.missing_df
                            has_nulls = missing['Missing'].sum() > 0
                            if has_nulls:
                                missing_only = missing[missing['Missing'] > 0].sort_values('Missing', ascending=False)
                                st.warning(f'{len(missing_only)} column(s) have missing values.', icon='⚠️')
                                st.dataframe(missing_only, use_container_width=True, hide_index=True)
                            else:
                                st.success('No missing values found in this worksheet.', icon='✅')
                            with st.expander('View all columns'):
                                st.dataframe(missing, use_container_width=True, hide_index=True)
                        with tab_stats:
                            if preview.stats_df is not None:
                                st.dataframe(preview.stats_df, use_container_width=True, hide_index=True)
                                st.caption('Descriptive statistics for numeric columns (count, mean, std, min, 25%, 50%, 75%, max)')
                            else:
                                st.info('No numeric columns found in this worksheet. Statistics are only generated for numeric data.', icon='ℹ️')
                    st.markdown('#### 🧩 Schema Detection')
                    schema_cache_key = f'schema_{selected_file_name}_{selected_sheet}'
                    if schema_cache_key not in st.session_state:
                        st.session_state[schema_cache_key] = detect_schema(sheet_df, selected_sheet)
                    schema = st.session_state[schema_cache_key]
                    sc1, sc2, sc3 = st.columns(3)
                    sc1.metric('Mapped Columns', f'{len(schema.mapped_columns)} / {schema.total_columns}')
                    sc2.metric('Coverage', f'{schema.coverage_percent}%')
                    sc3.metric('Categories Detected', len(schema.detected_categories))
                    if schema.mapped_columns:
                        with st.expander(f'✅ Mapped Columns ({len(schema.mapped_columns)})', expanded=True):
                            table_hdr = '| Raw Column | → | Standard Field | Category | Match | Confidence |\n|------------|---|----------------|----------|-------|------------|\n'
                            table_rows = ''
                            for m in schema.mapped_columns:
                                conf_icon = '🟢' if m.confidence == 'high' else '🟡'
                                table_rows += f'| `{m.raw_name}` | → | **{m.standard_name}** | {m.category} | {m.match_type} | {conf_icon} {m.confidence} |\n'
                            st.markdown(table_hdr + table_rows)
                    if schema.unmapped_columns:
                        with st.expander(f'❓ Unmapped Columns ({len(schema.unmapped_columns)})', expanded=False):
                            st.caption('These columns were not matched to any standard field. They will be available as raw data during analysis.')
                            cols_per_row = 4
                            for row_start in range(0, len(schema.unmapped_columns), cols_per_row):
                                row_cols = st.columns(cols_per_row)
                                for i, col_w in enumerate(row_cols):
                                    idx = row_start + i
                                    if idx < len(schema.unmapped_columns):
                                        col_w.code(schema.unmapped_columns[idx], language=None)
                    if schema.detected_categories:
                        with st.expander(f'🏷️ Detected Categories ({len(schema.detected_categories)})', expanded=False):
                            st.write(' · '.join((f'**{cat}**' for cat in schema.detected_categories)))
                    st.markdown('#### 🔄 Data Normalization')
                    norm_cache_key = f'norm_{selected_file_name}_{selected_sheet}'
                    if norm_cache_key not in st.session_state:
                        with st.spinner('Normalizing data...'):
                            st.session_state[norm_cache_key] = normalize_dataframe(sheet_df, schema)
                    norm_result = st.session_state[norm_cache_key]
                    nm1, nm2, nm3, nm4 = st.columns(4)
                    nm1.metric('Transformations', norm_result.total_transformations)
                    nm2.metric('Date Columns', len(norm_result.date_columns))
                    nm3.metric('Status Columns', len(norm_result.status_columns))
                    nm4.metric('Progress Columns', len(norm_result.progress_columns))
                    if norm_result.logs:
                        with st.expander(f'📝 Normalization Log ({norm_result.total_transformations} actions)', expanded=True):
                            log_header = '| Column | Action | Before | After | Details |\n|--------|--------|--------|-------|---------|\n'
                            log_rows = ''
                            for log in norm_result.logs:
                                log_rows += f'| `{log.column}` | {log.action} | {log.original_values} | {log.normalized_values} | {log.details} |\n'
                            st.markdown(log_header + log_rows)
                    n_tab_data, n_tab_status, n_tab_dates = st.tabs(['📄 Normalized Data', '🎨 Status Distribution', '📅 Date Columns'])
                    with n_tab_data:
                        st.dataframe(norm_result.normalized_df.head(10), use_container_width=True, hide_index=True)
                        st.caption(f'Showing first 10 of {len(norm_result.normalized_df):,} rows ({len(norm_result.normalized_df.columns)} columns)')
                    with n_tab_status:
                        if norm_result.status_columns:
                            for col in norm_result.status_columns:
                                counts = norm_result.normalized_df[col].value_counts().reset_index()
                                counts.columns = ['Status', 'Count']
                                st.dataframe(counts, use_container_width=True, hide_index=True)
                        else:
                            st.info('No status columns detected in this sheet.', icon='ℹ️')
                    with n_tab_dates:
                        if norm_result.date_columns:
                            for col in norm_result.date_columns:
                                series = norm_result.normalized_df[col]
                                valid = series.notna().sum()
                                total = len(series)
                                st.markdown(f'**{col}** — {valid}/{total} valid dates')
                                if valid > 0:
                                    min_d = series.min()
                                    max_d = series.max()
                                    st.caption(f'Range: {min_d} → {max_d}')
                        else:
                            st.info('No date columns detected in this sheet.', icon='ℹ️')
                    if norm_result.renamed_columns:
                        with st.expander('🔀 Column Name Comparison', expanded=False):
                            cmp_header = '| # | Original Column | → | Normalized Column |\n|---|-----------------|---|-------------------|\n'
                            cmp_rows = ''
                            for i, (raw, std) in enumerate(norm_result.renamed_columns.items(), 1):
                                cmp_rows += f'| {i} | `{raw}` | → | **{std}** |\n'
                            st.markdown(cmp_header + cmp_rows)
                elif ws_info:
                    st.warning(f'Worksheet **{selected_sheet}** is empty.', icon='📭')
            else:
                st.warning('No worksheets found in this workbook.', icon='📭')
    st.markdown('---')
    if uploaded_files and has_uploads():
        st.subheader('💬 Project Comments')
        valid_files = [f for f in uploaded_files if any((info.filename == f.name and info.status == 'Uploaded' for info in results))]
        if valid_files:
            sel_name = st.session_state.get('workbook_selector')
            sel_file = next((f for f in valid_files if f.name == sel_name), valid_files[0])
            wb_cache = st.session_state.get(f'workbook_info_{sel_file.name}')
            sheet_list = wb_cache.sheet_names if wb_cache else []
            cmt_cache_key = f'comments_{sel_file.name}'
            if cmt_cache_key not in st.session_state:
                norm_df = st.session_state.get('projects', {}).get(sel_file.name)
                with st.spinner('Extracting comments...'):
                    st.session_state[cmt_cache_key] = extract_comments(sel_file, sheet_list, normalized_df=norm_df)
            cmt_result = st.session_state[cmt_cache_key]
            for w in cmt_result.warnings:
                st.warning(w, icon='⚠️')
            if cmt_result.has_comments:
                cm1, cm2, cm3, cm4 = st.columns(4)
                cm1.metric('Source Sheet', cmt_result.source_sheet)
                cm2.metric('Total Rows', cmt_result.total_rows)
                cm3.metric('Valid Comments', cmt_result.valid_comments)
                cm4.metric('Skipped Rows', cmt_result.skipped_rows)
                if cmt_result.column_mapping:
                    with st.expander('🔗 Detected Column Mapping', expanded=False):
                        for std, raw in cmt_result.column_mapping.items():
                            st.markdown(f'  `{raw}` → **{std}**')
                comments_df = cmt_result.to_dataframe()
                search = st.text_input('🔍 Search comments', placeholder='Type to filter comments...', key='comment_search')
                if search:
                    mask = comments_df.apply(lambda row: row.astype(str).str.contains(search, case=False, na=False).any(), axis=1)
                    filtered_df = comments_df[mask]
                else:
                    filtered_df = comments_df
                st.dataframe(filtered_df, use_container_width=True, hide_index=True, column_config={'task_name': st.column_config.TextColumn('Task', width='medium'), 'comment': st.column_config.TextColumn('Comment', width='large'), 'owner': st.column_config.TextColumn('Owner', width='small'), 'date': st.column_config.TextColumn('Date', width='small')})
                st.caption(f'Showing {len(filtered_df)} of {cmt_result.valid_comments} comments')
                with st.expander('🤖 AI-Ready Output Preview', expanded=False):
                    ai_data = cmt_result.to_ai_input()
                    st.code(json.dumps(ai_data[:3], indent=2, default=str), language='json')
                    st.caption(f'{len(ai_data)} comment(s) prepared for AI analysis')
            elif not cmt_result.warnings:
                st.info('No comments found in this workbook.', icon='ℹ️')
    st.markdown('---')
    st.subheader('📊 Project Summary')
    if 'analyzed_projects' in st.session_state and st.session_state['analyzed_projects']:
        proj_names = list(st.session_state['analyzed_projects'].keys())
        sel_proj = st.selectbox('Select Project to View Analysis', options=proj_names, key='sel_proj_view')
        proj_data = st.session_state['analyzed_projects'][sel_proj]
        scorecard: ProjectHealthScorecard = proj_data['scorecard']
        decision: RAGDecisionResult = proj_data['decision']
        rca: RootCauseAnalysisResult = proj_data['rca']
        recs: RecommendationResult = proj_data['recommendations']
        sentiment = proj_data['sentiment']
        c1, c2, c3 = st.columns(3)
        c1.metric('Overall RAG Status', decision.overall_rag.value if decision else scorecard.overall_status.value)
        c2.metric('Overall Health Score', f'{round(scorecard.overall_score)} / 100')
        c3.metric('Indicators Evaluated', len(scorecard.indicators))
        st.markdown('#### 📈 Health Indicators Breakdown')
        ind_rows = []
        for cat, ind_res in scorecard.indicators.items():
            ind_rows.append({'Indicator Category': cat.value.title(), 'Status': ind_res.rag_status.value, 'Score': round(ind_res.score, 1) if ind_res.data_available else 'N/A', 'Summary': ind_res.summary})
        st.dataframe(ind_rows, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="section-card"><p>Project summary will appear here after analysis is complete.</p></div>', unsafe_allow_html=True)
    st.subheader('🤖 AI Analysis')
    if 'analyzed_projects' in st.session_state and st.session_state['analyzed_projects']:
        sel_proj = st.session_state.get('sel_proj_view', list(st.session_state['analyzed_projects'].keys())[0])
        proj_data = st.session_state['analyzed_projects'][sel_proj]
        decision = proj_data['decision']
        rca = proj_data['rca']
        sentiment = proj_data['sentiment']
        recs = proj_data['recommendations']
        t_rag, t_rca, t_sent, t_recs = st.tabs(['🎯 RAG Decision Reasoning', '🔍 Root Cause Analysis', '💬 Stakeholder Sentiment', '💡 Recommendations'])
        with t_rag:
            st.markdown(f'**Final RAG:** `{decision.overall_rag.value}` (Confidence: {decision.confidence_score}%)')
            st.markdown(f'**Decision Summary:** {decision.decision_summary}')
            st.markdown(f'**Business Impact:** {decision.business_impact}')
            if decision.decision_trace:
                with st.expander('Detailed Decision Trace'):
                    for t in decision.decision_trace:
                        st.markdown(f'- **[{t.influence.upper()}]** {t.indicator}: {t.reason}')
        with t_rca:
            st.markdown(f'**Executive Summary:** {rca.executive_summary}')
            st.markdown(f'**Risk Escalation Level:** `{rca.risk_escalation}`')
            if rca.root_causes:
                st.markdown('**Identified Root Causes:**')
                for rc in rca.root_causes:
                    ev_str = ', '.join(rc.evidence) if rc.evidence else 'No direct evidence cited'
                    st.markdown(f'- **{rc.category}** ({rc.severity}): **{rc.cause}** — {rc.description} *(Evidence: {ev_str})*')
            elif rca.summary:
                st.markdown(f'**Summary:** {rca.summary}')
        with t_sent:
            st.markdown(f'**Overall Sentiment:** `{sentiment.overall_sentiment.value}` (Confidence: {sentiment.confidence_score}%)')
            st.markdown(f"**Concern Areas:** {(', '.join(sentiment.concern_areas) if sentiment.concern_areas else 'None detected')}")
            st.markdown(f'**Summary:** {sentiment.summary}')
            if sentiment.supporting_evidence:
                with st.expander('Supporting Evidence'):
                    for ev in sentiment.supporting_evidence:
                        st.markdown(f'- {ev}')
        with t_recs:
            if recs.all_recommendations:
                for act in recs.all_recommendations:
                    prio_icon = '🔴' if act.priority == 'Critical' else '🟡' if act.priority == 'High' else '🟢'
                    st.markdown(f'#### {prio_icon} [{act.priority.upper()}] {act.category}: {act.action}')
                    if act.rationale:
                        st.markdown(f'**Rationale:** {act.rationale}')
                    st.markdown(f'*Timeframe: {act.timeframe} | Impact: {act.expected_impact}*')
                    st.divider()
            else:
                st.info('No recommendations generated.')
    else:
        st.markdown('<div class="section-card"><p>AI-generated health assessment, reasoning, and risk analysis will be displayed here.</p></div>', unsafe_allow_html=True)