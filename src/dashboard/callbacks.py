import json
from dash import Input, Output, State, ALL, dcc, html, dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from sqlalchemy import select, func

from src.database.session import SessionLocal
from src.database.models import Employee, EngagementSurvey, HRTraining, Recruitment
from src.dashboard.layout import layout_overview, layout_capital, layout_risk, layout_workforce, layout_data_table, layout_talent_map

# Estilos globales para gráficos
COLOR_ACCENT = "#2563eb"
COLOR_GRAY = "#cbd5e1"
COLOR_GRAY_DARK = "#64748b"
COLOR_GRAY_LIGHT = "#e2e8f0"
COLOR_DANGER = "#ef4444"
COLOR_SUCCESS = "#10b981"
COLOR_WARNING = "#f59e0b"

def apply_enterprise_layout(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#1e293b", size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=False, zeroline=False, color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="#e2e8f0", zeroline=False, color="#94a3b8"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def apply_emp_filters(query, model, dept_filter, worker_filter):
    q = query
    if dept_filter != 'ALL':
        q = q.filter(func.trim(Employee.department_type) == dept_filter)
    if worker_filter != 'ALL':
        q = q.filter(func.trim(Employee.employee_type) == worker_filter)
    return q

def register_callbacks(app):

    # ==========================================
    # ROUTER Y SIDEBAR STYLING
    # ==========================================
    @app.callback(
        [Output("page-content", "children"),
         Output("link-overview", "className"),
         Output("link-capital", "className"),
         Output("link-risk", "className"),
         Output("link-workforce", "className"),
         Output("link-talent-map", "className"),
         Output("link-data-workers", "className"),
         Output("link-data-trainings", "className"),
         Output("link-data-surveys", "className"),
         Output("link-data-recruitment", "className")],
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        ac = "nav-item active"
        ic = "nav-item"
        r_ac = "nav-item nav-resource active"
        r_ic = "nav-item nav-resource"
        
        # Por defecto
        res = [layout_overview(), ac, ic, ic, ic, ic, r_ic, r_ic, r_ic, r_ic]
        
        if pathname == "/dashboard/capital":
            res = [layout_capital(), ic, ac, ic, ic, ic, r_ic, r_ic, r_ic, r_ic]
        elif pathname == "/dashboard/risk":
            res = [layout_risk(), ic, ic, ac, ic, ic, r_ic, r_ic, r_ic, r_ic]
        elif pathname == "/dashboard/workforce":
            res = [layout_workforce(), ic, ic, ic, ac, ic, r_ic, r_ic, r_ic, r_ic]
        elif pathname == "/dashboard/talent-map":
            res = [layout_talent_map(), ic, ic, ic, ic, ac, r_ic, r_ic, r_ic, r_ic]
        elif pathname == "/dashboard/data/workers":
            res = [layout_data_table("Employees Data", "resources-data-table"), ic, ic, ic, ic, ic, r_ac, r_ic, r_ic, r_ic]
        elif pathname == "/dashboard/data/trainings":
            res = [layout_data_table("HR Trainings Data", "resources-data-table"), ic, ic, ic, ic, ic, r_ic, r_ac, r_ic, r_ic]
        elif pathname == "/dashboard/data/surveys":
            res = [layout_data_table("Surveys Data", "resources-data-table"), ic, ic, ic, ic, ic, r_ic, r_ic, r_ac, r_ic]
        elif pathname == "/dashboard/data/recruitment":
            res = [layout_data_table("Recruitment Data", "resources-data-table"), ic, ic, ic, ic, ic, r_ic, r_ic, r_ic, r_ac]
            
        return res

    # ==========================================
    # 0. UI CALLBACKS (AI CHAT & FILTERS)
    # ==========================================
    @app.callback(
        Output("ai-chat-offcanvas", "is_open"),
        Input("open-ai-chat-btn", "n_clicks"),
        [State("ai-chat-offcanvas", "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @app.callback(
        [Output("ai-chat-history", "children"),
         Output("ai-chat-store", "data"),
         Output("ai-chat-input", "value")],
        [Input("ai-chat-send", "n_clicks"),
         Input("ai-chat-input", "n_submit")],
        [State("ai-chat-input", "value"),
         State("ai-chat-store", "data")],
        prevent_initial_call=True
    )
    def update_chat(n_clicks, n_submit, user_input, chat_history):
        from dash import html
        from src.ai.rag import generate_and_execute_sql
        
        if not user_input:
            raise PreventUpdate

        if chat_history is None:
            chat_history = []
            
        # Append User Message
        chat_history.append({"role": "user", "text": user_input})
        
        # Get LLM Response
        ai_response = generate_and_execute_sql(user_input, chat_history)
        chat_history.append({"role": "ai", "text": ai_response})
        
        # Build UI
        history_ui = []
        for msg in chat_history:
            if msg["role"] == "user":
                history_ui.append(html.Div(
                    msg["text"], 
                    style={"textAlign": "right", "color": "white", "backgroundColor": "#2563eb", "padding": "10px", "borderRadius": "10px", "marginBottom": "10px", "marginLeft": "auto", "maxWidth": "80%", "width": "fit-content"}
                ))
            else:
                history_ui.append(html.Div(
                    msg["text"], 
                    style={"textAlign": "left", "color": "#1e293b", "backgroundColor": "#e2e8f0", "padding": "10px", "borderRadius": "10px", "marginBottom": "10px", "marginRight": "auto", "maxWidth": "90%", "width": "fit-content"}
                ))
                
        return history_ui, chat_history, ""

    @app.callback(
        [Output("global-dept-filter", "options"), Output("global-worker-filter", "options")],
        Input("url", "pathname")
    )
    def populate_filters(pathname):
        with SessionLocal() as db:
            depts = db.query(Employee.department_type).distinct().all()
            types = db.query(Employee.employee_type).distinct().all()
            dept_opts = [{'label': 'All Departments', 'value': 'ALL'}] + [{'label': str(d[0]).strip(), 'value': str(d[0]).strip()} for d in depts if d[0]]
            type_opts = [{'label': 'All Employees', 'value': 'ALL'}] + [{'label': str(t[0]).strip(), 'value': str(t[0]).strip()} for t in types if t[0]]
            return dept_opts, type_opts

    # ==========================================
    # 1. OVERVIEW CALLBACKS
    # ==========================================
    @app.callback(
        [
            Output("kpi-turnover-rate", "children"),
            Output("kpi-turnover-trend", "children"),
            Output("kpi-overview-workforce", "children"),
            Output("kpi-overview-wf-trend", "children"),
            Output("chart-recruitment-status", "figure")
        ],
        [
            Input("global-dept-filter", "value"),
            Input("global-worker-filter", "value"),
            Input("url", "pathname")
        ]
    )
    def update_overview(dept_filter, worker_filter, pathname):
        if pathname not in ["/", "/dashboard/", "/dashboard", None]:
            raise PreventUpdate
            
        from src.database.crud import get_turnover_rate, get_recruitment_status
        
        # 1. KPIs: Turnover and Active Workforce
        turnover_df = get_turnover_rate()
        t_rate = 0
        total_emp = 0
        if not turnover_df.empty:
            t_rate = turnover_df['turnover_rate'].iloc[0]
            total_emp = turnover_df['total_count'].iloc[0]

        # 2. Recruitment Status Line Chart
        recruitment_df = get_recruitment_status()
        fig_rec = go.Figure()
        if not recruitment_df.empty:
            for status in ['applied', 'interviewing', 'under_review', 'rejected', 'offered']:
                fig_rec.add_trace(go.Scatter(
                    x=recruitment_df['month'],
                    y=recruitment_df[status],
                    mode='lines+markers',
                    name=status.capitalize().replace('_', ' ')
                ))
            fig_rec = apply_enterprise_layout(fig_rec)
            fig_rec.update_layout(xaxis_title="Month", yaxis_title="Number of Applicants")

        return (
            f"{t_rate:.2f}%",
            "Company-wide",
            f"{total_emp:,}",
            "Total Employees",
            fig_rec
        )

    # ==========================================
    # 2. CAPITAL EFFICIENCY CALLBACKS
    # ==========================================
    @app.callback(
        [
            Output("kpi-training-investment", "children"),
            Output("kpi-training-count", "children"),
            Output("chart-training-programs", "figure"),
            Output("chart-training-costs", "figure"),
            Output("chart-monthly-frequency", "figure"),
            Output("chart-yearly-outcomes", "figure"),
            Output("chart-monthly-outcomes", "figure")
        ],
        [
            Input("global-dept-filter", "value"),
            Input("global-worker-filter", "value"),
            Input("url", "pathname")
        ]
    )
    def update_capital(dept_filter, worker_filter, pathname):
        if pathname != "/dashboard/capital":
            raise PreventUpdate
            
        from src.database.crud import get_training_costs, get_training_programs, get_frequency_per_year, get_frequency_per_month
        
        df_costs = get_training_costs()
        df_programs = get_training_programs()
        df_year = get_frequency_per_year()
        df_month = get_frequency_per_month()
        
        if df_costs.empty or df_programs.empty:
            empty_fig = apply_enterprise_layout(go.Figure())
            return "$0", "0", empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

        total_cost = df_costs['total_cost'].sum()
        total_trainings = df_programs['total_trainings'].sum()
        
        # Chart 1: Training Programs (Bar)
        fig_prog = go.Figure(go.Bar(
            x=df_programs['Training Program Name'], y=df_programs['total_trainings'],
            marker_color=COLOR_ACCENT,
            text=[f"{count}<br>({pct}%)" for count, pct in zip(df_programs['total_trainings'], df_programs['total_percentage'])],
            textposition='outside',
            cliponaxis=False
        ))
        
        max_y = df_programs['total_trainings'].max() * 1.2 if not df_programs.empty else 100
        fig_prog = apply_enterprise_layout(fig_prog).update_layout(
            yaxis_title="Total Trainings",
            yaxis=dict(range=[0, max_y])
        )
        
        # Chart 2: Training Costs (Bar with Avg Line)
        avg_cost = df_costs['total_cost'].mean()
        fig_costs = go.Figure()
        fig_costs.add_trace(go.Bar(
            x=df_costs['program'], y=df_costs['total_cost'],
            marker_color=COLOR_GRAY_DARK, name="Cost"
        ))
        fig_costs.add_hline(y=avg_cost, line_dash="dash", annotation_text=f"Average: ${avg_cost:,.2f}", line_color="black")
        fig_costs = apply_enterprise_layout(fig_costs).update_layout(yaxis_title="Cost ($)")
        
        # Chart 3: Monthly Frequency (Line)
        df_month['mes_anio'] = df_month['month'] + '-' + df_month['year']
        fig_freq = px.line(df_month, x='mes_anio', y='monthly_trainings', color='Training Program Name', markers=True)
        fig_freq = apply_enterprise_layout(fig_freq).update_layout(xaxis_title="Mes-Año", yaxis_title="Number of Trainings")
        fig_freq.update_xaxes(tickangle=-45)
        
        # Chart 4: Yearly Outcomes (100% Stacked Bar)
        # Average the rates across years so they sum to 100% per program
        df_outcomes = df_year.groupby('program')[['passed_rate', 'failed_rate', 'pending_assessment_rate', 'incomplete_rate']].mean().reset_index()
        
        fig_year = go.Figure()
        outcomes = [('passed_rate', 'Passed', COLOR_SUCCESS), 
                    ('failed_rate', 'Failed', COLOR_DANGER), 
                    ('pending_assessment_rate', 'Pending Assessment', COLOR_ACCENT), 
                    ('incomplete_rate', 'Incomplete', COLOR_GRAY)]
        for col, name, color in outcomes:
            if col in df_outcomes.columns:
                fig_year.add_trace(go.Bar(
                    x=df_outcomes['program'], y=df_outcomes[col], name=name, marker_color=color,
                    text=[f"{val:.1f}%" if val > 2 else "" for val in df_outcomes[col]], textposition='inside'
                ))
        fig_year = apply_enterprise_layout(fig_year).update_layout(barmode='stack', yaxis_title="Percentage (%)")
        
        # Chart 5: Monthly Outcomes (Subplots - simulated by faceting if possible or just returning one large fig)
        # We will use Plotly Express facet_col with wrap for independent titles at the top of each chart
        df_melted = df_month.melt(id_vars=['mes_anio', 'Training Program Name'], 
                                         value_vars=['passed_rate', 'failed_rate', 'pending_assessment_rate', 'incomplete_rate'],
                                         var_name='Outcome', value_name='Rate')
        
        # Format text to show percentage if > 2%
        df_melted['text_label'] = df_melted['Rate'].apply(lambda x: f"{x:.1f}%" if x > 2 else "")

        fig_month = px.bar(df_melted, 
                           x='mes_anio', y='Rate', color='Outcome', 
                           facet_col='Training Program Name', facet_col_wrap=1,
                           text='text_label',
                           color_discrete_map={'passed_rate': COLOR_SUCCESS, 'failed_rate': COLOR_DANGER, 'pending_assessment_rate': COLOR_ACCENT, 'incomplete_rate': COLOR_GRAY})
        
        fig_month = apply_enterprise_layout(fig_month).update_layout(barmode='stack', height=1000)
        # Show tick labels for all subplots, force showing every month, and rotate diagonally
        fig_month.update_xaxes(showticklabels=True, tickmode='linear', tickangle=-45, title_text="", tickfont=dict(color='black'), color='black')
        fig_month.update_yaxes(tickfont=dict(color='black'), color='black')
        # Fix subplot labels to just show the program name
        fig_month.for_each_annotation(lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>", font=dict(size=14, color='black')))

        return (
            f"${total_cost:,.2f}",
            f"{total_trainings:,}",
            fig_prog,
            fig_costs,
            fig_freq,
            fig_year,
            fig_month
        )

    # ==========================================
    # 3. OPERATIONAL RISK CALLBACKS
    # ==========================================
    @app.callback(
        [
            Output("chart-risk-turnover-division", "figure"),
            Output("chart-risk-tenure", "figure")
        ],
        [
            Input("global-dept-filter", "value"),
            Input("global-worker-filter", "value"),
            Input("url", "pathname")
        ]
    )
    def update_risk(dept_filter, worker_filter, pathname):
        if pathname != "/dashboard/risk":
            raise PreventUpdate
            
        from src.database.crud import get_turnover_by_division, get_tenure
        
        df_div = get_turnover_by_division()
        df_tenure = get_tenure()
        
        if df_div.empty or df_tenure.empty:
            empty_fig = apply_enterprise_layout(go.Figure())
            return empty_fig, empty_fig

        # Chart 1: Turnover by Division (Bar Chart)
        # Red if above average, blue if below
        company_avg = 17.32 # Based on notebook
        colors = [COLOR_DANGER if x >= company_avg else COLOR_GRAY for x in df_div['turnover_rate']]
        
        fig_div = go.Figure(go.Bar(
            x=df_div['turnover_rate'], y=df_div['division'], orientation='h',
            marker_color=colors, text=[f"{val}%" for val in df_div['turnover_rate']], textposition='outside'
        ))
        fig_div.add_vline(x=company_avg, line_dash="dash", line_color="black", annotation_text=f"Company avg: {company_avg}%")
        fig_div = apply_enterprise_layout(fig_div).update_layout(xaxis_title="Turnover Rate (%)", yaxis_title="Division", yaxis={'categoryorder':'total ascending'})

        # Chart 2: Employee Tenure Months (Histogram)
        avg_tenure = df_tenure['tenure_months'].mean()
        fig_tenure = go.Figure(go.Histogram(
            x=df_tenure['tenure_months'], nbinsx=30, marker_color=COLOR_GRAY_DARK
        ))
        fig_tenure.add_vline(x=avg_tenure, line_dash="dash", line_color=COLOR_DANGER, annotation_text=f"Average: {avg_tenure:.1f} months")
        fig_tenure = apply_enterprise_layout(fig_tenure).update_layout(xaxis_title="Tenure (Months)", yaxis_title="Number of Employees")
        
        return fig_div, fig_tenure

    # ==========================================
    # 4. WORKFORCE ANALYTICS CALLBACKS
    # ==========================================
    @app.callback(
        [
            Output("chart-wf-engagement", "figure"),
            Output("chart-wf-satisfaction", "figure"),
            Output("chart-wf-wlb", "figure")
        ],
        [
            Input("global-dept-filter", "value"),
            Input("global-worker-filter", "value"),
            Input("url", "pathname")
        ]
    )
    def update_workforce(dept_filter, worker_filter, pathname):
        if pathname != "/dashboard/workforce":
            raise PreventUpdate
            
        from src.database.crud import get_individual_engagement_scores
        
        df = get_individual_engagement_scores()
        
        if df.empty:
            empty_fig = apply_enterprise_layout(go.Figure())
            return empty_fig, empty_fig, empty_fig

        # Map performance to colors and numeric values for jitter
        perf_order = ['PIP', 'Needs Improvement', 'Fully Meets', 'Exceeds']
        color_map = {
            'Exceeds': COLOR_SUCCESS,
            'Fully Meets': COLOR_GRAY_DARK,
            'Needs Improvement': COLOR_ACCENT,
            'PIP': COLOR_DANGER
        }
        
        import numpy as np
        
        def create_jitter_plot(metric_col, title_text):
            fig = go.Figure()
            for i, perf in enumerate(perf_order):
                subset = df[df['Performance Score'] == perf]
                if subset.empty:
                    continue
                # Add jitter
                jitter_y = np.random.uniform(-0.15, 0.15, size=len(subset))
                fig.add_trace(go.Scatter(
                    x=subset[metric_col],
                    y=[i + 1 + jy for jy in jitter_y],
                    mode='markers',
                    name=perf,
                    marker=dict(color=color_map.get(perf, COLOR_GRAY), opacity=0.5, size=8)
                ))
            fig.update_layout(
                yaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3, 4],
                    ticktext=perf_order,
                    title="Performance Score"
                ),
                xaxis_title=metric_col,
                showlegend=True,
                legend=dict(orientation="h", y=-0.2)
            )
            return apply_enterprise_layout(fig)
        
        fig_eng = create_jitter_plot('Engagement Score', 'Engagement')
        fig_sat = create_jitter_plot('Satisfaction Score', 'Satisfaction')
        fig_wlb = create_jitter_plot('Work-Life Balance Score', 'Work-Life Balance')

        return fig_eng, fig_sat, fig_wlb

    # ==========================================
    # 5. DATA TABLES (RESOURCES) CALLBACKS
    # ==========================================
    @app.callback(
        [Output("resources-data-table", "data"), Output("resources-data-table", "columns")],
        [Input("global-dept-filter", "value"), Input("global-worker-filter", "value"), Input("url", "pathname")]
    )
    def update_data_table(dept_filter, worker_filter, pathname):
        if pathname not in ["/dashboard/data/workers", "/dashboard/data/trainings", "/dashboard/data/surveys", "/dashboard/data/recruitment"]:
            raise PreventUpdate
            
        with SessionLocal() as db:
            if pathname == "/dashboard/data/workers":
                query = apply_emp_filters(db.query(Employee.emp_id, Employee.first_name, Employee.last_name, Employee.title, Employee.department_type, Employee.employee_type, Employee.performance_score), Employee, dept_filter, worker_filter)
                df = pd.DataFrame(query.all(), columns=["Emp ID", "First Name", "Last Name", "Title", "Department", "Type", "Performance Score"])
                
            elif pathname == "/dashboard/data/trainings":
                query = apply_emp_filters(db.query(HRTraining.id, HRTraining.employee_id, Employee.department_type, HRTraining.training_program_name, HRTraining.training_type, HRTraining.training_outcome, HRTraining.training_cost, HRTraining.duration_days).outerjoin(Employee, HRTraining.employee_id == Employee.emp_id), Employee, dept_filter, worker_filter)
                df = pd.DataFrame(query.all(), columns=["Training ID", "Emp ID", "Department", "Program Name", "Type", "Outcome", "Cost", "Duration (Days)"])
                
            elif pathname == "/dashboard/data/surveys":
                query = apply_emp_filters(db.query(EngagementSurvey.id, EngagementSurvey.employee_id, Employee.department_type, EngagementSurvey.engagement_score, EngagementSurvey.satisfaction_score, EngagementSurvey.work_life_balance_score).outerjoin(Employee, EngagementSurvey.employee_id == Employee.emp_id), Employee, dept_filter, worker_filter)
                df = pd.DataFrame(query.all(), columns=["Survey ID", "Emp ID", "Department", "Engagement", "Satisfaction", "WLB"])

            elif pathname == "/dashboard/data/recruitment":
                # Note: Recruitment has no department_type so global filters do not apply. We show all or we could join if there was a link, but there isn't.
                query = db.query(Recruitment.applicant_id, Recruitment.job_title, Recruitment.first_name, Recruitment.last_name, Recruitment.education_level, Recruitment.years_of_experience, Recruitment.status)
                df = pd.DataFrame(query.all(), columns=["Applicant ID", "Job Title", "First Name", "Last Name", "Education", "Experience (Years)", "Status"])
            
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict('records')
            return data, columns

    # ==========================================
    # 6. TALENT MAP CALLBACKS
    # ==========================================
    @app.callback(
        Output("chart-talent-map", "figure"),
        [Input("map-filter-status", "value"),
         Input("map-filter-education", "value"),
         Input("map-filter-gender", "value"),
         Input("map-filter-salary", "value"),
         Input("url", "pathname")]
    )
    def update_talent_map(status_val, edu_val, gender_val, salary_range, pathname):
        if pathname != "/dashboard/talent-map":
            raise PreventUpdate
        with SessionLocal() as db:
            query = db.query(Recruitment.state)
            
            if status_val != 'ALL':
                query = query.filter(Recruitment.status == status_val)
            if edu_val != 'ALL':
                query = query.filter(Recruitment.education_level == edu_val)
            if gender_val != 'ALL':
                query = query.filter(Recruitment.gender == gender_val)
                
            min_sal, max_sal = salary_range
            query = query.filter(Recruitment.desired_salary >= min_sal, Recruitment.desired_salary <= max_sal)
            
            df = pd.DataFrame(query.all(), columns=["State"])
            
        if df.empty:
            return apply_enterprise_layout(go.Figure())
            
        state_counts = df['State'].value_counts().reset_index()
        state_counts.columns = ['State', 'Applications']
        
        fig = px.choropleth(
            state_counts,
            locations='State',
            locationmode='USA-states',
            color='Applications',
            scope='usa',
            color_continuous_scale=[COLOR_GRAY, COLOR_ACCENT],
            hover_name='State',
            labels={'Applications': 'Applications'}
        )
        
        fig.update_layout(
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                lakecolor='rgba(255,255,255,1)',
                showlakes=True,
                showsubunits=True,
                subunitcolor=COLOR_GRAY,
            ),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return apply_enterprise_layout(fig)