
import pandas as pd
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO

# Exemplo de Orçamento Fixo
data_ut12 = {
    'Conta': ['UNIFORME', 'EPI', 'FERRAMENTAS', 'MATERIAL APLICADO', 'MATERIAL CONSUMO', 'LOCAÇÃO MÁQUINAS',
              'DESPESA INFORMÁTICA', 'DESPESA TELEFONES CELULARES', 'SERVIÇOS CONTRATADOS',
              'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.', 'MANUTENÇÃO DE VEÍCULOS', 'CARTÃO COMBUSTÍVEL'],
    'Orçamento': [1459.10, 3315.28, 1633.50, 3448.50, 889.35, 381.15, 80.00, 419.35, 1089.00, 290.40, 108.90, 0.00]
}

data_ut31 = {
    'Conta': ['UNIFORME', 'EPI', 'FERRAMENTAS', 'MATERIAL APLICADO', 'MATERIAL CONSUMO', 'LOCAÇÃO MÁQUINAS',
              'DESPESA INFORMÁTICA', 'DESPESA TELEFONES CELULARES', 'SERVIÇOS CONTRATADOS',
              'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.', 'MANUTENÇÃO DE VEÍCULOS', 'CARTÃO COMBUSTÍVEL'],
    'Orçamento': [1200.50, 3150.30, 1500.20, 3350.00, 850.00, 400.00, 100.00, 450.00, 1150.00, 320.00, 150.00, 50.00]
}

# Carregar as despesas da planilha para UT-12 e UT-31
df_excel = pd.read_excel('Controle_orcamento.xlsx', sheet_name='Base')

# Filtrar os dados para UT-12 e UT-31
df_ut12_cru = df_excel[df_excel['UTS'] == 'UT-12']
df_ut31_cru = df_excel[df_excel['UTS'] == 'UT-31']

# Criar DataFrames baseados nos dados filtrados
df_ut12 = pd.DataFrame(data_ut12)
df_ut31 = pd.DataFrame(data_ut31)

# Adicionar despesas e categorias às tabelas de UT-12 e UT-31
df_ut12['Despesas'] = df_ut12_cru['Despesas']
df_ut12['Categoria'] = df_ut12_cru['CATEGORIA']
df_ut31['Despesas'] = df_ut31_cru['Despesas']
df_ut31['Categoria'] = df_ut31_cru['CATEGORIA']

# Calcular as diferenças entre Orçamento e Despesas
df_ut12['Diferença'] = df_ut12['Orçamento'] - df_ut12['Despesas']
df_ut31['Diferença'] = df_ut31['Orçamento'] - df_ut31['Despesas']

# Cálculos do resultado final para UT-12 e UT-31
orçamento_total_ut12 = df_ut12['Orçamento'].sum()
despesas_totais_ut12 = df_ut12['Despesas'].sum()
saldo_final_ut12 = orçamento_total_ut12 - despesas_totais_ut12

orçamento_total_ut31 = df_ut31['Orçamento'].sum()
despesas_totais_ut31 = df_ut31['Despesas'].sum()
saldo_final_ut31 = orçamento_total_ut31 - despesas_totais_ut31

# Gráfico de barras horizontais para UT-12
fig_ut12 = go.Figure()
fig_ut12.add_trace(go.Bar(
    y=df_ut12['Conta'], x=df_ut12['Orçamento'], name='Orçamento', orientation='h',
    marker=dict(color='rgba(58, 71, 80, 0.6)')
))
fig_ut12.add_trace(go.Bar(
    y=df_ut12['Conta'], x=df_ut12['Despesas'], name='Despesas', orientation='h',
    marker=dict(color='rgba(246, 78, 139, 0.6)')
))
fig_ut12.add_trace(go.Bar(
    y=df_ut12['Conta'], x=df_ut12['Diferença'], name='Diferença', orientation='h',
    marker=dict(color=df_ut12['Diferença'].apply(lambda x: 'red' if x < 0 else 'green'))
))
fig_ut12.update_layout(title="Controle Financeiro UT-12", xaxis_title="Valor em R$", yaxis_title="Contas", barmode='stack')

# Gráfico de barras horizontais para UT-31
fig_ut31 = go.Figure()
fig_ut31.add_trace(go.Bar(
    y=df_ut31['Conta'], x=df_ut31['Orçamento'], name='Orçamento', orientation='h',
    marker=dict(color='rgba(58, 71, 80, 0.6)')
))
fig_ut31.add_trace(go.Bar(
    y=df_ut31['Conta'], x=df_ut31['Despesas'], name='Despesas', orientation='h',
    marker=dict(color='rgba(246, 78, 139, 0.6)')
))
fig_ut31.add_trace(go.Bar(
    y=df_ut31['Conta'], x=df_ut31['Diferença'], name='Diferença', orientation='h',
    marker=dict(color=df_ut31['Diferença'].apply(lambda x: 'red' if x < 0 else 'green'))
))
fig_ut31.update_layout(title="Controle Financeiro UT-31", xaxis_title="Valor em R$", yaxis_title="Contas", barmode='stack')

# Configurações de estilo
tab_card = {'height': '100%'}
config_graph = {"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# Layout
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.themes.DARKLY])

app.layout = dbc.Container([
    # Troca de tema e título
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
                        ], sm=12, md=8),
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Oracle", href="https://login-euld-saasfaprod1.fa.ocs.oraclecloud.com/", target="_blank", color="danger")
                    ], style={'margin-top': '20px'})
                ])
            ], style=tab_card)
        ], sm=12, lg=4)
    ]),

    # Resumo e gráficos de UT-12 e UT-31
    dbc.Row([
        # Coluna UT-12
        dbc.Col([
            # Resumo UT-12
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"Orçamento Total UT-12: R$ {orçamento_total_ut12:,.2f}"),
                    html.H5(f"Total Gasto UT-12: R$ {despesas_totais_ut12:,.2f}"),
                    html.H5(f"Saldo Final UT-12: R$ {saldo_final_ut12:,.2f}",
                            style={"color": "red" if saldo_final_ut12 < 0 else "green"}),
                ], style={'padding': '10px'})  # Diminuir o padding
            ], style={'height': '120px', 'margin-bottom': '10px'}),  # Definir altura menor

            # Gráfico UT-12
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut12, config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=6),

        # Coluna UT-31
        dbc.Col([
            # Resumo UT-31
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"Orçamento Total UT-31: R$ {orçamento_total_ut31:,.2f}"),
                    html.H5(f"Total Gasto UT-31: R$ {despesas_totais_ut31:,.2f}"),
                    html.H5(f"Saldo Final UT-31: R$ {saldo_final_ut31:,.2f}",
                            style={"color": "red" if saldo_final_ut31 < 0 else "green"}),
                ], style={'padding': '10px'})  # Diminuir o padding
            ], style={'height': '120px', 'margin-bottom': '10px'}),  # Definir altura menor

            # Gráfico UT-31
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut31, config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=6)
    ])
], fluid=True)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
