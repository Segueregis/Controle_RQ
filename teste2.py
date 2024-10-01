import pandas as pd
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO

# Carregar a planilha Excel com as despesas, incluindo a coluna "Despesas Fixas"
df_excel = pd.read_excel('Controle_orcamento.xlsx', sheet_name='Base')

# Remover colunas com valores NaN
df_cru = df_excel.loc[:, ~df_excel.columns.isna()]

# Adicionar a coluna 'Conta' caso não exista
if 'Conta' not in df_cru.columns:
    raise KeyError("A coluna 'Conta' não foi encontrada na planilha.")

# Substituir as despesas e adicionar as categorias
df_cru['Despesas'] = df_cru['Despesas Fixas']
df_cru['Diferença'] = df_cru['Orçamento'] - df_cru['Despesas']

# Função para filtrar e calcular as informações por UTS
def gerar_dados_uts(uts):
    df_uts = df_cru[df_cru['UTS'] == uts].copy()
    print(f"Dados para {uts}:")
    print(df_uts)  # Adiciona esta linha para verificar os dados
    df_uts['Diferença'] = df_uts['Orçamento'] - df_uts['Despesas']

    orçamento_total_uts = df_uts['Orçamento'].sum()
    despesas_totais_uts = df_uts['Despesas'].sum()
    saldo_final_uts = orçamento_total_uts - despesas_totais_uts

    return df_uts, orçamento_total_uts, despesas_totais_uts, saldo_final_uts


# Gerando dados para cada UTS
df_ut12, orçamento_ut12, despesas_ut12, saldo_ut12 = gerar_dados_uts("UT-12")
df_ut20, orçamento_ut20, despesas_ut20, saldo_ut20 = gerar_dados_uts("UT-20")
df_ut26, orçamento_ut26, despesas_ut26, saldo_ut26 = gerar_dados_uts("UT-26")
df_ut31, orçamento_ut31, despesas_ut31, saldo_ut31 = gerar_dados_uts("UT-31")

# Função para criar gráfico de barras para cada UTS
def criar_grafico(df, titulo):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df['Conta'],
        x=df['Orçamento'],
        name='Orçamento',
        orientation='h',
        marker=dict(color='rgba(58, 71, 80, 0.6)')
    ))

    fig.add_trace(go.Bar(
        y=df['Conta'],
        x=df['Despesas'],
        name='Despesas',
        orientation='h',
        marker=dict(color='rgba(246, 78, 139, 0.6)')
    ))

    fig.add_trace(go.Bar(
        y=df['Conta'],
        x=df['Diferença'],
        name='Diferença',
        orientation='h',
        marker=dict(color=df['Diferença'].apply(lambda x: 'red' if x < 0 else 'green'))
    ))

    fig.update_layout(
        title=titulo,
        xaxis_title="Valor em R$",
        yaxis_title="Contas",
        barmode='stack',
        template="plotly_white"
    )

    return fig

# Criando gráficos para cada UTS
fig_ut12 = criar_grafico(df_ut12, "Controle Financeiro UT-12")
fig_ut20 = criar_grafico(df_ut20, "Controle Financeiro UT-20")
fig_ut26 = criar_grafico(df_ut26, "Controle Financeiro UT-26")
fig_ut31 = criar_grafico(df_ut31, "Controle Financeiro UT-31")

# ========== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor": "top",
               "y": 0.9,
               "xanchor": "left",
               "x": 0.1,
               "title": {"text": None},
               "font": {"color": "white"},
               "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# ======== Layout =========== #
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.themes.DARKLY])

app.layout = dbc.Container(children=[
    # Row 1: Painel de título e tema
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Controle de Orçamento", style={'font-size': '20px', 'font-weight': 'bold'}),
                        ], sm=12, md=8),

                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("UT JOHNSON", style={'display': 'inline-block', 'text-align': 'center',
                                                             'margin-left': '10px'})
                        ], sm=12, md=8)
                    ], style={'margin-top': '10px'}),

                    dbc.Row([
                        dbc.Button("Oracle", href="https://login-euld-saasfaprod1.fa.ocs.oraclecloud.com/",
                                   target="_blank", color="danger")
                    ], style={'margin-top': '20px'})
                ])
            ], style=tab_card)
        ], sm=12, lg=4),

        # Row 2: Resumo geral para cada UTS
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.H5(f"Orçamento Total UT-12: R$ {orçamento_ut12:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Total Gasto UT-12: R$ {despesas_ut12:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Saldo Final UT-12: R$ {saldo_ut12:,.2f}",
                                        style={"color": "red" if saldo_ut12 < 0 else "green"}), width=12),
                        html.Hr(),
                        dbc.Col(html.H5(f"Orçamento Total UT-20: R$ {orçamento_ut20:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Total Gasto UT-20: R$ {despesas_ut20:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Saldo Final UT-20: R$ {saldo_ut20:,.2f}",
                                        style={"color": "red" if saldo_ut20 < 0 else "green"}), width=12),
                        html.Hr(),
                        dbc.Col(html.H5(f"Orçamento Total UT-26: R$ {orçamento_ut26:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Total Gasto UT-26: R$ {despesas_ut26:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Saldo Final UT-26: R$ {saldo_ut26:,.2f}",
                                        style={"color": "red" if saldo_ut26 < 0 else "green"}), width=12),
                        html.Hr(),
                        dbc.Col(html.H5(f"Orçamento Total UT-31: R$ {orçamento_ut31:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Total Gasto UT-31: R$ {despesas_ut31:,.2f}"), width=12),
                        dbc.Col(html.H5(f"Saldo Final UT-31: R$ {saldo_ut31:,.2f}",
                                        style={"color": "red" if saldo_ut31 < 0 else "green"}), width=12),
                    ], style={'text-align': 'center'}),
                ])
            ], style=tab_card)
        ], sm=12, lg=8)
    ], style={'margin-bottom': '20px'}),

    # Row 3: Gráficos de barras horizontais para cada UTS
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut12, config=config_graph)
                ])
            ], style=tab_card)
        ], width=12),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut20, config=config_graph)
                ])
            ], style=tab_card)
        ], width=12),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut26, config=config_graph)
                ])
            ], style=tab_card)
        ], width=12),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut31, config=config_graph)
                ])
            ], style=tab_card)
        ], width=12)
    ])
])

# Rodando o app
if __name__ == '__main__':
    app.run_server(debug=True)
