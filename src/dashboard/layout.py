from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# ==========================================
# CÁSCARA DE LA APLICACIÓN (Sidebar + Navbar)
# ==========================================
def create_sidebar():
    return html.Div(id="sidebar", children=[
        # Logo and Branding
        html.Div(className="sidebar-header", children=[
            html.I(className="bi bi-bar-chart-fill", style={"fontSize": "24px", "color": "var(--color-primary)"}),
            html.H3("Employee-LMS", className="mb-0", style={"color": "var(--color-primary)", "fontWeight": "700", "fontSize": "20px"})
        ]),
        
        # Navigation Links
        html.Div(className="sidebar-nav", id="sidebar-nav-container", children=[
            html.Div("NAVEGACIÓN", className="sidebar-section-title"),
            
            dcc.Link([
                html.I(className="bi bi-speedometer2"),
                html.Span("Dashboard")
            ], href="/dashboard/", id="link-overview", className="nav-item"),
            
            dcc.Link([
                html.I(className="bi bi-graph-up-arrow"),
                html.Span("Eficiencia de Capital")
            ], href="/dashboard/capital", id="link-capital", className="nav-item"),
            
            dcc.Link([
                html.I(className="bi bi-pie-chart"),
                html.Span("Riesgo Operativo")
            ], href="/dashboard/risk", id="link-risk", className="nav-item"),
            
            dcc.Link([
                html.I(className="bi bi-people"),
                html.Span("Fuerza Laboral")
            ], href="/dashboard/workforce", id="link-workforce", className="nav-item"),
            
            dcc.Link([
                html.I(className="bi bi-globe-americas"),
                html.Span("Mapa de Talento")
            ], href="/dashboard/talent-map", id="link-talent-map", className="nav-item"),
            
            html.Div("INFO EMPRESA", className="sidebar-section-title mt-4"),
            html.Div(className="company-info-box", children=[
                html.Div(className="company-info-row", children=[
                    html.Span("Empresa:", className="company-info-key"),
                    html.Span("Acme Corp", className="company-info-value fw-bold text-dark")
                ]),
                html.Div(className="company-info-row", children=[
                    html.Span("Industria:", className="company-info-key"),
                    html.Span("Tecnología", className="company-info-value fw-bold text-dark")
                ]),
                html.Div(className="company-info-row", children=[
                    html.Span("Estado:", className="company-info-key"),
                    html.Span("Activo", className="badge bg-success company-info-value")
                ])
            ]),
            
            html.Div("RECURSOS", className="sidebar-section-title mt-4"),
            
            dcc.Link([
                html.I(className="bi bi-file-earmark-text"),
                html.Span("Datos de Empleados"),
                html.I(className="bi bi-box-arrow-up-right nav-item-external")
            ], href="/dashboard/data/workers", id="link-data-workers", className="nav-item nav-resource"),
            
            dcc.Link([
                html.I(className="bi bi-file-earmark-text"),
                html.Span("Datos de Capacitación"),
                html.I(className="bi bi-box-arrow-up-right nav-item-external")
            ], href="/dashboard/data/trainings", id="link-data-trainings", className="nav-item nav-resource"),
            
            dcc.Link([
                html.I(className="bi bi-file-earmark-text"),
                html.Span("Datos de Encuestas"),
                html.I(className="bi bi-box-arrow-up-right nav-item-external")
            ], href="/dashboard/data/surveys", id="link-data-surveys", className="nav-item nav-resource"),
            
            dcc.Link([
                html.I(className="bi bi-file-earmark-text"),
                html.Span("Datos de Reclutamiento"),
                html.I(className="bi bi-box-arrow-up-right nav-item-external")
            ], href="/dashboard/data/recruitment", id="link-data-recruitment", className="nav-item nav-resource"),
        ]),
        
        # Global Filters
        html.Div(className="sidebar-filters", children=[
            html.Div("FILTROS GLOBALES", className="sidebar-section-title"),
            html.Div(className="mb-3", children=[
                html.Label("Tipo de Departamento", className="filter-label"),
                dcc.Dropdown(
                    id="global-dept-filter",
                    options=[{'label': 'Todos los Departamentos', 'value': 'ALL'}], # Populated via callback
                    value='ALL',
                    clearable=False,
                    className="custom-dropdown"
                )
            ]),
            html.Div(className="mb-3", children=[
                html.Label("Tipo de Empleado", className="filter-label"),
                dcc.Dropdown(
                    id="global-worker-filter",
                    options=[{'label': 'Todos los Empleados', 'value': 'ALL'}], # Populated via callback
                    value='ALL',
                    clearable=False,
                    className="custom-dropdown"
                )
            ])
        ])
    ])

def layout_topbar():
    return html.Div(className="topbar", children=[
        html.Div(className="topbar-title", children="Análisis de Empleados"),
        html.Div(className="topbar-actions d-flex align-items-center", children=[
            html.Div(className="status-indicator me-3", children=[
                html.Div(className="status-dot"),
                html.Span("Sistema Activo", className="fw-bold text-dark")
            ]),
            html.Span("|"),
            html.Span("Última actualización: Recién", className="ms-3 text-muted")
        ])
    ])

# ==========================================
# VISTAS ESPECIALIZADAS (Páginas)
# ==========================================

# 1. Dashboard Overview
def layout_overview():
    return html.Div([
        dbc.Row(className="mb-24", children=[
            dbc.Col(lg=6, md=6, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card", children=[
                    html.Div(className="kpi-header-row", children=[html.Span("Tasa de Rotación", className="kpi-title"), html.I(className="bi bi-person-x text-danger")]),
                    html.Div(className="kpi-value-row", children=[html.H3(id="kpi-turnover-rate", className="kpi-value text-danger", children="..."), html.Span(id="kpi-turnover-trend", className="trend-up", children="...")]),
                    html.Div(id="kpi-turnover-subtext", className="kpi-subtext", children="Calculado sobre la base promedio")
                ])
            ]),
            dbc.Col(lg=6, md=6, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card", children=[
                    html.Div(className="kpi-header-row", children=[html.Span("Fuerza Laboral Activa", className="kpi-title"), html.I(className="bi bi-people text-success")]),
                    html.Div(className="kpi-value-row", children=[html.H3(id="kpi-overview-workforce", className="kpi-value text-success", children="..."), html.Span(id="kpi-overview-wf-trend", className="trend-up", children="...")]),
                    html.Div(id="kpi-overview-wf-subtext", className="kpi-subtext", children="Empleados actualmente activos")
                ])
            ])
        ]),
        dbc.Row(children=[
            dbc.Col(lg=12, md=12, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card", children=[
                    html.Div(className="chart-header", children="Estado de Reclutamiento Mensual"),
                    html.P("Número de postulantes en cada etapa a lo largo del tiempo.", className="text-muted small mb-2"),
                    dcc.Loading(dcc.Graph(id="chart-recruitment-status", style={"height": "400px"}, config={'displayModeBar': False}))
                ])
            ])
        ]),
        # Textual Insights
        dbc.Row(className="mt-4", children=[
            dbc.Col(lg=12, md=12, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card h-100", children=[
                    html.H5("Estado de Reclutamiento - Resultados e Interpretaciones", className="mb-4 fw-bold"),
                    html.Ul(children=[
                        html.Li("Las actividades de reclutamiento presentan un aumento constante en mayo, luego se observa un aumento en revisiones y entrevistas en junio, finalizando en julio con una ola de ofertas y rechazos."),
                        html.Li("La tasa de rotación de la empresa se encuentra en un nivel relativamente saludable. Sin embargo, equipos específicos muestran una rotación muy alta que debe ser investigada.")
                    ])
                ])
            ])
        ])
    ])

# 2. Capital Efficiency (Fees Blueprint)
def layout_capital():
    return html.Div([
        # Page Header
        html.Div(className="d-flex justify-content-between align-items-center mb-4", children=[
            html.Div(children=[
                html.H2("Capacitación y Desarrollo", className="page-title"),
                html.P("Análisis de actividades, costos y resultados de capacitación a lo largo del tiempo", className="text-muted small")
            ])
        ]),

        # KPIs row
        dbc.Row(className="mb-4", children=[
            dbc.Col(lg=6, md=6, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card h-100", children=[
                    html.Span("Inversión Total en Capacitación", className="text-muted small d-block mb-2"),
                    html.H4(id="kpi-training-investment", className="text-success fw-bold mb-0", children="..."),
                    html.Span("Gasto total en todos los programas", className="text-muted small mt-2 d-block")
                ])
            ]),
            dbc.Col(lg=6, md=6, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card h-100", children=[
                    html.Span("Capacitaciones Realizadas", className="text-muted small d-block mb-2"),
                    html.H4(id="kpi-training-count", className="fw-bold mb-0", children="..."),
                    html.Span("Sesiones totales", className="text-muted small mt-2 d-block")
                ])
            ])
        ]),

        # Visualizations Row 1 (Totals & Costs)
        dbc.Row(className="mb-4", children=[
            dbc.Col(lg=6, children=[
                html.Div(className="premium-card h-100", children=[
                    html.H5("Número Total de Capacitaciones Realizadas (Por Programa)", className="card-title fw-bold mb-3"),
                    dcc.Loading(dcc.Graph(id="chart-training-programs", style={"height": "350px"}, config={'displayModeBar': False}))
                ])
            ]),
            dbc.Col(lg=6, children=[
                html.Div(className="premium-card h-100", children=[
                    html.H5("Costos de Capacitación (Por Programa)", className="card-title fw-bold mb-3"),
                    dcc.Loading(dcc.Graph(id="chart-training-costs", style={"height": "350px"}, config={'displayModeBar': False}))
                ])
            ])
        ]),

        # Visualizations Row 2 (Monthly Frequency & Yearly Outcomes)
        dbc.Row(className="mb-4", children=[
            dbc.Col(lg=6, children=[
                html.Div(className="premium-card h-100", children=[
                    html.H5("Frecuencia Mensual de Capacitación por Programa", className="card-title fw-bold mb-3"),
                    dcc.Loading(dcc.Graph(id="chart-monthly-frequency", style={"height": "350px"}, config={'displayModeBar': False}))
                ])
            ]),
            dbc.Col(lg=6, children=[
                html.Div(className="premium-card h-100", children=[
                    html.H5("Resultados Anuales de Capacitación (Por Programa)", className="card-title fw-bold mb-3"),
                    dcc.Loading(dcc.Graph(id="chart-yearly-outcomes", style={"height": "350px"}, config={'displayModeBar': False}))
                ])
            ])
        ]),
        
        # Visualizations Row 3 (Monthly Outcomes subplots)
        dbc.Row(className="mb-4", children=[
            dbc.Col(lg=12, children=[
                html.Div(className="premium-card", children=[
                    html.H5("Resultados Mensuales de Capacitación (Por Programa)", className="card-title fw-bold mb-3"),
                    dcc.Loading(dcc.Graph(id="chart-monthly-outcomes", style={"height": "1000px"}, config={'displayModeBar': False}))
                ])
            ])
        ]),

        # Textual Insights
        dbc.Row(className="mb-4", children=[
            dbc.Col(lg=12, md=12, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card h-100", children=[
                    html.H5("Capacitación y Desarrollo - Resultados e Interpretaciones", className="mb-4 fw-bold"),
                    html.Ul(children=[
                        html.Li("De todos los programas, Habilidades de Comunicación y Gestión de Proyectos tienen mayor cantidad de sesiones realizadas, representando el 22.43% y 20.30% del total respectivamente."),
                        html.Li("En cuanto a la frecuencia mensual, todos los programas se realizan con frecuencia variable sin patrones consistentes. Sin embargo, las capacitaciones en habilidades de comunicación presentan mayor volatilidad."),
                        html.Li("Los empleados aprueban más la capacitación de Desarrollo de Liderazgo (28.2%), mientras que aprueban menos la de Habilidades Técnicas (21.8%). Las capacitaciones en habilidades técnicas tienen la mayor tasa de no completados con un 30.7%."),
                        html.Li("Un gran porcentaje de los resultados de capacitación se encuentran incompletos o pendientes de evaluación, lo que sugiere la necesidad de mejorar las evaluaciones y los procesos administrativos.")
                    ])
                ])
            ])
        ])
    ])

# 3. Operational Risk (Portfolio Blueprint)
def layout_risk():
    return html.Div([
        # Page Header & Tabs
        html.Div(className="d-flex flex-column mb-4", children=[
            html.H2("Riesgo y Retención", className="page-title"),
            html.P("Análisis de las tasas de rotación y tendencias de retención en distintas divisiones", className="text-muted small mb-3")
        ]),

        html.Div(id="risk-tab-content", children=[
            dbc.Row(className="mb-4", children=[
                dbc.Col(lg=6, children=[
                    html.Div(className="premium-card h-100", children=[
                        html.H5("Tasa de Rotación por División", className="card-title fw-bold mb-3"),
                        dcc.Loading(dcc.Graph(id="chart-risk-turnover-division", style={"height": "400px"}, config={'displayModeBar': False})),
                        html.P("Las barras rojas indican tasas de rotación superiores al promedio de la empresa.", className="text-muted small mt-2")
                    ])
                ]),
                dbc.Col(lg=6, children=[
                    html.Div(className="premium-card h-100", children=[
                        html.H5("Antigüedad de Empleados (Meses) Antes de Salir", className="card-title fw-bold mb-3"),
                        dcc.Loading(dcc.Graph(id="chart-risk-tenure", style={"height": "400px"}, config={'displayModeBar': False})),
                        html.P("Distribución de los meses de antigüedad para los empleados que han abandonado la empresa.", className="text-muted small mt-2")
                    ])
                ])
            ]),
            
            # Textual Insights
            dbc.Row(className="mb-4", children=[
                dbc.Col(lg=12, md=12, className="mb-3 mb-lg-0", children=[
                    html.Div(className="premium-card h-100", children=[
                        html.H5("Riesgo y Retención - Resultados e Interpretaciones", className="mb-4 fw-bold"),
                        html.Ul(children=[
                            html.Li("La tasa de rotación general de la empresa es del 17.32%, lo cual puede considerarse saludable a nivel compañía. Sin embargo, equipos como Isp (28.57%), Servicios de Personal (20.0%) y Taller (Flota) (19.3%) tienen las tasas de rotación más altas. Sería beneficioso analizar con más detalle por qué los empleados dejan estos equipos."),
                            html.Li("Si bien la mayoría de los equipos presentan tasas de rotación normales, ciertos equipos con gran número de empleados, específicamente Operaciones de Campo y General - Con, también presentan un alto número de empleados que se retiran (113 finalizados en Operaciones de Campo y 63 en General - Con)."),
                            html.Li("Según los datos, se observa que la mayoría de los empleados que finalizaron su contrato lo hicieron dentro de los primeros 5 meses de empleo. Esto sugiere un problema de desgaste temprano. Es posible que existan problemas en la inducción o las expectativas del puesto y se debería mejorar la retención de los empleados en sus primeros 6 meses.")
                        ])
                    ])
                ])
            ])
        ])
    ])

# 4. Workforce Analytics (Performance Blueprint)
def layout_workforce():
    return html.Div([
        # Title Block
        html.Div(className="d-flex justify-content-between align-items-center mb-4", children=[
            html.Div(children=[
                html.H2("Compromiso de los Empleados", className="page-title"),
                html.P("Análisis de las puntuaciones individuales de la encuesta de compromiso y su relación con el desempeño", className="text-muted small mb-0")
            ])
        ]),

        # Charts Section
        dbc.Row(className="mb-4", children=[
            dbc.Col(lg=12, children=[
                html.Div(className="premium-card", children=[
                    html.H5("Puntuaciones Individuales vs Desempeño", className="card-title fw-bold mb-3"),
                    html.P("Estos gráficos muestran cómo las puntuaciones de Compromiso, Satisfacción y Equilibrio Trabajo-Vida se correlacionan con la calificación de desempeño del empleado.", className="text-muted small"),
                    dbc.Row(children=[
                        dbc.Col(lg=4, children=[
                            dcc.Loading(dcc.Graph(id="chart-wf-engagement", style={"height": "400px"}, config={'displayModeBar': False}))
                        ]),
                        dbc.Col(lg=4, children=[
                            dcc.Loading(dcc.Graph(id="chart-wf-satisfaction", style={"height": "400px"}, config={'displayModeBar': False}))
                        ]),
                        dbc.Col(lg=4, children=[
                            dcc.Loading(dcc.Graph(id="chart-wf-wlb", style={"height": "400px"}, config={'displayModeBar': False}))
                        ])
                    ])
                ])
            ])
        ]),

        # Textual Insights
        dbc.Row(className="mb-4", children=[
            dbc.Col(lg=12, md=12, className="mb-3 mb-lg-0", children=[
                html.Div(className="premium-card h-100", children=[
                    html.H5("Compromiso de los Empleados - Resultados e Interpretaciones", className="mb-4 fw-bold"),
                    html.Ul(children=[
                        html.Li("Basado en los gráficos de dispersión, la mayoría de los promedios de las puntuaciones de compromiso no predicen directamente el desempeño de los empleados. Existe mucha varianza."),
                        html.Li("Sin embargo, existen algunos valores atípicos, como Ventas y Marketing, que presentan altas puntuaciones de 'Necesita Mejorar' en desempeño a pesar de tener altos puntajes en la encuesta de compromiso."),
                        html.Li("El análisis a nivel individual es más confiable ya que captura la variación entre empleados que se pierde al agregar los datos por división.")
                    ])
                ])
            ])
        ])
    ])

# 5. Data Tables (Resources)
def layout_data_table(title, table_id):
    return html.Div([
        dbc.Row(className="mb-24", children=[
            dbc.Col(lg=12, children=[
                html.Div(className="premium-card", children=[
                    html.Div(className="chart-header", children=title),
                    html.P("Usa los filtros debajo de cada columna para buscar. Haz clic en 'Export' para descargar los datos en formato CSV.", className="text-muted small mb-3"),
                    dcc.Loading(
                        dash_table.DataTable(
                            id=table_id,
                            filter_action="native",
                            sort_action="native",
                            export_format="csv",
                            page_size=20,
                            style_table={'overflowX': 'auto'},
                            style_header={'backgroundColor': 'white', 'fontWeight': 'bold', 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'},
                            style_cell={'textAlign': 'left', 'padding': '12px', 'fontFamily': 'Inter', 'color': '#1e293b', 'borderBottom': '1px solid #f1f5f9', 'fontSize': '13px'},
                        )
                    )
                ])
            ])
        ])
    ])

def layout_talent_map():
    return html.Div([
        html.Div(className="d-flex justify-content-between align-items-center mb-4", children=[
            html.H2("Distribución Geográfica del Talento", className="page-title"),
        ]),
        
        # Filters Row
        html.Div(className="row mb-4", children=[
            html.Div(className="col-md-3", children=[
                html.Label("Estado de la Solicitud", className="filter-label"),
                dcc.Dropdown(
                    id="map-filter-status",
                    options=[
                        {'label': 'Todos los Estados', 'value': 'ALL'},
                        {'label': 'En Entrevista', 'value': 'Interviewing'},
                        {'label': 'Rechazado', 'value': 'Rejected'},
                        {'label': 'En Revisión', 'value': 'In Review'},
                        {'label': 'Oferta Realizada', 'value': 'Offered'}
                    ],
                    value='ALL',
                    clearable=False,
                    className="custom-dropdown"
                )
            ]),
            html.Div(className="col-md-3", children=[
                html.Label("Nivel Educativo", className="filter-label"),
                dcc.Dropdown(
                    id="map-filter-education",
                    options=[
                        {'label': 'Todos los Niveles', 'value': 'ALL'},
                        {'label': 'Secundaria', 'value': 'High School'},
                        {'label': 'Licenciatura', 'value': "Bachelor's Degree"},
                        {'label': 'Maestría', 'value': "Master's Degree"},
                        {'label': 'Doctorado', 'value': 'PhD'}
                    ],
                    value='ALL',
                    clearable=False,
                    className="custom-dropdown"
                )
            ]),
            html.Div(className="col-md-3", children=[
                html.Label("Género", className="filter-label"),
                dcc.Dropdown(
                    id="map-filter-gender",
                    options=[
                        {'label': 'Todos los Géneros', 'value': 'ALL'},
                        {'label': 'Masculino', 'value': 'Male'},
                        {'label': 'Femenino', 'value': 'Female'},
                        {'label': 'Otro', 'value': 'Other'}
                    ],
                    value='ALL',
                    clearable=False,
                    className="custom-dropdown"
                )
            ]),
            html.Div(className="col-md-3", children=[
                html.Label("Rango Salarial Deseado (USD)", className="filter-label"),
                dcc.RangeSlider(
                    id="map-filter-salary",
                    min=30000,
                    max=100000,
                    step=1000,
                    value=[30047.22, 99992.66],
                    marks={
                        30000: {'label': '$30k', 'style': {'color': '#64748b'}},
                        50000: {'label': '$50k', 'style': {'color': '#64748b'}},
                        75000: {'label': '$75k', 'style': {'color': '#64748b'}},
                        100000: {'label': '$100k', 'style': {'color': '#64748b'}}
                    },
                    tooltip={"placement": "bottom", "always_visible": False}
                )
            ])
        ]),
        
        # Map Container
        html.Div(className="content-card", children=[
            html.H5("Solicitudes Recibidas por Estado (EE.UU.)", className="card-title"),
            dcc.Graph(id="chart-talent-map", style={"height": "600px"})
        ])
    ])

# Base Layout
def create_layout():
    return html.Div(className="app-container", children=[
        dcc.Location(id="url", refresh=False),
        create_sidebar(),
        html.Div(className="main-content", children=[
            layout_topbar(),
            html.Div(id="page-content", className="page-content")
        ]),
        
        # --- Floating AI Button & Offcanvas ---
        html.Div(
            className="ai-floating-btn-container",
            style={
                "position": "fixed",
                "bottom": "30px",
                "right": "30px",
                "zIndex": "1050"
            },
            children=[
                html.Div(
                    "¡Pregúntame sobre los datos!",
                    className="bg-white text-primary px-3 py-2 rounded shadow-sm border border-primary",
                    style={
                        "position": "absolute", 
                        "bottom": "75px", 
                        "right": "0px", 
                        "whiteSpace": "nowrap",
                        "fontWeight": "bold",
                        "fontSize": "0.9rem",
                        "borderRadius": "20px 20px 0 20px"
                    }
                ),
                dbc.Button(
                    html.I(className="bi bi-robot fs-4"),
                    id="open-ai-chat-btn",
                    className="rounded-circle shadow-lg",
                    color="primary",
                    style={"width": "60px", "height": "60px"}
                )
            ]
        ),
        dbc.Offcanvas(
            html.Div([
                dcc.Store(id="ai-chat-store", data=[]),
                html.P("Hola, soy Gemini. Estoy aquí para analizar los datos de los empleados."),
                dcc.Loading(
                    id="loading-chat",
                    type="dot",
                    color="#0d6efd",
                    children=[
                        html.Div(id="ai-chat-history", className="ai-chat-history", style={"height": "600px", "backgroundColor": "#f8f9fa", "borderRadius": "8px", "padding": "15px", "marginBottom": "15px", "overflowY": "auto"})
                    ]
                ),
                dbc.InputGroup([
                    dbc.Input(id="ai-chat-input", placeholder="Pregúntame algo sobre los datos..."),
                    dbc.Button(
                        html.Span([html.I(className="bi bi-send"), ""]),
                        id="ai-chat-send",
                        color="primary"
                    )
                ])
            ]),
            id="ai-chat-offcanvas",
            title="AI Insights (Gemini)",
            is_open=False,
            placement="end",
            style={"width": "600px"}
        )
    ])

layout = create_layout()