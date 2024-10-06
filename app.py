import pandas as pd
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
from flask import Flask


# Inicializando o app Dash com tema Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



# Exemplo de Orçamento Fixo para UT-12, UT-31, UT-26 e UT-20
data_ut12 = {
    'Conta': ['UNIFORME', 'EPI', 'FERRAMENTAS', 'MATERIAL APLICADO', 'MATERIAL CONSUMO', 'LOCAÇÃO MÁQUINAS',
              'DESPESA INFORMÁTICA', 'DESPESA TELEFONES CELULARES', 'SERVIÇOS CONTRATADOS',
              'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.', 'MANUTENÇÃO DE VEÍCULOS', 'CARTÃO COMBUSTÍVEL'],
    'Orçamento': [1459.10, 3315.28, 1633.50, 3448.50, 889.35, 381.15, 80.00, 419.35, 1089.00, 290.40, 108.90, 100.00]
}

data_ut31 = {
    'Conta': ['UNIFORME', 'EPI', 'FERRAMENTAS', 'MATERIAL APLICADO', 'MATERIAL CONSUMO', 'LOCAÇÃO MÁQUINAS',
              'DESPESA INFORMÁTICA', 'DESPESA TELEFONES CELULARES', 'SERVIÇOS CONTRATADOS',
              'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.', 'MANUTENÇÃO DE VEÍCULOS', 'CARTÃO COMBUSTÍVEL'],
    'Orçamento': [5272.79, 4583.69, 1452.00, 9801.00, 13794.00, 7121.47, 120.00, 454.24, 6534.00, 7078.50, 816.75, 3601.07]
}

data_ut31 = {
    'Conta': ['UNIFORME', 'EPI', 'FERRAMENTAS', 'MATERIAL APLICADO', 'MATERIAL CONSUMO', 'LOCAÇÃO CARROS',
              'LOCAÇÃO GESTÃO ATIVOS', 'LOCAÇÃO MÁQUINAS', 'DESPESA INFORMÁTICA', 'DESPESA TELEFONES CELULARES', 
              'SERVIÇOS CONTRATADOS', 'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.', 'MANUTENÇÃO DE VEÍCULOS', 'CARTÃO COMBUSTÍVEL'],
    'Orçamento': [5272.79, 4583.69, 1452.00, 9801.00, 13794.00, 5262.80, 11980.64, 7121.47, 120.00, 454.24, 
                  6534.00, 7078.50, 816.75, 3601.07]
}


data_ut20 = {
    'Conta': ['UNIFORME', 'EPI', 'FERRAMENTAS', 'MATERIAL APLICADO', 'MATERIAL CONSUMO', 'LOCAÇÃO MÁQUINAS',
              'DESPESA INFORMÁTICA', 'DESPESA TELEFONES CELULARES', 'SERVIÇOS CONTRATADOS',
              'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.', 'MANUTENÇÃO DE VEÍCULOS', 'CARTÃO COMBUSTÍVEL'],
    'Orçamento': [1100.30, 2780.20, 1400.00, 3100.00, 790.00, 370.00, 90.00, 430.00, 1120.00, 300.00, 140.00, 40.00]
}

# Carregar as despesas da planilha para cada UT
df_excel = pd.read_excel('Controle_orcamento.xlsx', sheet_name='Base')

# Filtrar os dados para cada UT
df_ut12_cru = df_excel[df_excel['UTS'] == 'UT-12']
df_ut31_cru = df_excel[df_excel['UTS'] == 'UT-31']
df_ut26_cru = df_excel[df_excel['UTS'] == 'UT-26']
df_ut20_cru = df_excel[df_excel['UTS'] == 'UT-20']

# Criar DataFrames baseados nos dados filtrados
df_ut12 = pd.DataFrame(data_ut12)
df_ut31 = pd.DataFrame(data_ut31)
df_ut26 = pd.DataFrame(data_ut26)
df_ut20 = pd.DataFrame(data_ut20)

# Adicionar despesas e categorias às tabelas de cada UT
df_ut12['Despesas'] = df_ut12_cru['Despesas']
df_ut12['Categoria'] = df_ut12_cru['CATEGORIA']
df_ut31['Despesas'] = df_ut31_cru['Despesas']
df_ut31['Categoria'] = df_ut31_cru['CATEGORIA']
df_ut26['Despesas'] = df_ut26_cru['Despesas']
df_ut26['Categoria'] = df_ut26_cru['CATEGORIA']
df_ut20['Despesas'] = df_ut20_cru['Despesas']
df_ut20['Categoria'] = df_ut20_cru['CATEGORIA']


# Calcular as diferenças entre Orçamento e Despesas para cada UT
df_ut12['Diferença'] = df_ut12['Orçamento'] - df_ut12['Despesas']
df_ut31['Diferença'] = df_ut31['Orçamento'] - df_ut31['Despesas']
df_ut26['Diferença'] = df_ut26['Orçamento'] - df_ut26['Despesas']
df_ut20['Diferença'] = df_ut20['Orçamento'] - df_ut20['Despesas']

# Cálculos do resultado final para cada UT
orçamento_total_ut12 = df_ut12['Orçamento'].sum()
despesas_totais_ut12 = df_ut12['Despesas'].sum()
saldo_final_ut12 = orçamento_total_ut12 - despesas_totais_ut12

orçamento_total_ut31 = df_ut31['Orçamento'].sum()
despesas_totais_ut31 = df_ut31['Despesas'].sum()
saldo_final_ut31 = orçamento_total_ut31 - despesas_totais_ut31

orçamento_total_ut26 = df_ut26['Orçamento'].sum()
despesas_totais_ut26 = df_ut26['Despesas'].sum()
saldo_final_ut26 = orçamento_total_ut26 - despesas_totais_ut26

orçamento_total_ut20 = df_ut20['Orçamento'].sum()
despesas_totais_ut20 = df_ut20['Despesas'].sum()
saldo_final_ut20 = orçamento_total_ut20 - despesas_totais_ut20

# Gráfico de barras verticais para UT-12
fig_ut12 = go.Figure()
fig_ut12.add_trace(go.Bar(
    x=df_ut12['Conta'], y=df_ut12['Orçamento'], name='Orçamento',
    marker=dict(color='rgba(58, 71, 80, 0.6)')
))
fig_ut12.add_trace(go.Bar(
    x=df_ut12['Conta'], y=df_ut12['Despesas'], name='Despesas',
    marker=dict(color='rgba(246, 78, 139, 0.6)')
))
fig_ut12.add_trace(go.Bar(
    x=df_ut12['Conta'], y=df_ut12['Diferença'], name='Diferença',
    marker=dict(color=df_ut12['Diferença'].apply(lambda x: 'red' if x < 0 else 'green'))
))
fig_ut12.update_layout(title="Controle Financeiro UT-12", yaxis_title="Valor em R$", xaxis_title="Contas", barmode='stack')

# Gráfico de barras verticais para UT-31
fig_ut31 = go.Figure()
fig_ut31.add_trace(go.Bar(
    x=df_ut31['Conta'], y=df_ut31['Orçamento'], name='Orçamento',
    marker=dict(color='rgba(58, 71, 80, 0.6)')
))
fig_ut31.add_trace(go.Bar(
    x=df_ut31['Conta'], y=df_ut31['Despesas'], name='Despesas',
    marker=dict(color='rgba(246, 78, 139, 0.6)')
))
fig_ut31.add_trace(go.Bar(
    x=df_ut31['Conta'], y=df_ut31['Diferença'], name='Diferença',
    marker=dict(color=df_ut31['Diferença'].apply(lambda x: 'red' if x < 0 else 'green'))
))
fig_ut31.update_layout(title="Controle Financeiro UT-31", yaxis_title="Valor em R$", xaxis_title="Contas", barmode='stack')

# Gráfico de barras verticais para UT-26
fig_ut26 = go.Figure()
fig_ut26.add_trace(go.Bar(
    x=df_ut26['Conta'], y=df_ut26['Orçamento'], name='Orçamento',
    marker=dict(color='rgba(58, 71, 80, 0.6)')
))
fig_ut26.add_trace(go.Bar(
    x=df_ut26['Conta'], y=df_ut26['Despesas'], name='Despesas',
    marker=dict(color='rgba(246, 78, 139, 0.6)')
))
fig_ut26.add_trace(go.Bar(
    x=df_ut26['Conta'], y=df_ut26['Diferença'], name='Diferença',
    marker=dict(color=df_ut26['Diferença'].apply(lambda x: 'red' if x < 0 else 'green'))
))
fig_ut26.update_layout(title="Controle Financeiro UT-26", yaxis_title="Valor em R$", xaxis_title="Contas", barmode='stack')

# Gráfico de barras verticais para UT-20
fig_ut20 = go.Figure()
fig_ut20.add_trace(go.Bar(
    x=df_ut20['Conta'], y=df_ut20['Orçamento'], name='Orçamento',
    marker=dict(color='rgba(58, 71, 80, 0.6)')
))
fig_ut20.add_trace(go.Bar(
    x=df_ut20['Conta'], y=df_ut20['Despesas'], name='Despesas',
    marker=dict(color='rgba(246, 78, 139, 0.6)')
))
fig_ut20.add_trace(go.Bar(
    x=df_ut20['Conta'], y=df_ut20['Diferença'], name='Diferença',
    marker=dict(color=df_ut20['Diferença'].apply(lambda x: 'red' if x < 0 else 'green'))
))
fig_ut20.update_layout(title="Controle Financeiro UT-20", yaxis_title="Valor em R$", xaxis_title="Contas", barmode='stack')



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

    # UT-12
    dbc.Row([
        dbc.Col([
            # Informações de Orçamento UT-12
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"Orçamento Total UT-12: R$ {orçamento_total_ut12:,.2f}"),
                    html.H5(f"Total Gasto UT-12: R$ {despesas_totais_ut12:,.2f}"),
                    html.H5(f"Saldo Final UT-12: R$ {saldo_final_ut12:,.2f}",
                            style={"color": "red" if saldo_final_ut12 < 0 else "green"}),
                ], style={'padding': '10px'})
            ], style={'height': '120px', 'margin-bottom': '10px'}),
            # Gráfico UT-12
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut12, style={'width': '100%', 'height': '600px'})
                ])
            ]),
        ], width=12),
    ], style={'margin-bottom': '20px'}),  # Espaçamento entre os blocos

    # UT-31
    dbc.Row([
        dbc.Col([
            # Informações de Orçamento UT-31
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"Orçamento Total UT-31: R$ {orçamento_total_ut31:,.2f}"),
                    html.H5(f"Total Gasto UT-31: R$ {despesas_totais_ut31:,.2f}"),
                    html.H5(f"Saldo Final UT-31: R$ {saldo_final_ut31:,.2f}",
                            style={"color": "red" if saldo_final_ut31 < 0 else "green"}),
                ], style={'padding': '10px'})
            ], style={'height': '120px', 'margin-bottom': '10px'}),
            # Gráfico UT-31
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut31, style={'width': '100%', 'height': '600px'})
                ])
            ]),
        ], width=12),
    ], style={'margin-bottom': '20px'}),  # Espaçamento entre os blocos

    # Outros gráficos e informações seguem o mesmo padrão, por exemplo UT-26 e UT-20
    # UT-26
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"Orçamento Total UT-26: R$ {orçamento_total_ut26:,.2f}"),
                    html.H5(f"Total Gasto UT-26: R$ {despesas_totais_ut26:,.2f}"),
                    html.H5(f"Saldo Final UT-26: R$ {saldo_final_ut26:,.2f}",
                            style={"color": "red" if saldo_final_ut26 < 0 else "green"}),
                ], style={'padding': '10px'})
            ], style={'height': '120px', 'margin-bottom': '10px'}),
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut26, style={'width': '100%', 'height': '600px'})
                ])
            ]),
        ], width=12),
    ], style={'margin-bottom': '20px'}),

    # UT-20
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"Orçamento Total UT-20: R$ {orçamento_total_ut20:,.2f}"),
                    html.H5(f"Total Gasto UT-20: R$ {despesas_totais_ut20:,.2f}"),
                    html.H5(f"Saldo Final UT-20: R$ {saldo_final_ut20:,.2f}",
                            style={"color": "red" if saldo_final_ut20 < 0 else "green"}),
                ], style={'padding': '10px'})
            ], style={'height': '120px', 'margin-bottom': '10px'}),
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig_ut20, style={'width': '100%', 'height': '600px'})
                ])
            ]),
        ], width=12),
    ], style={'margin-bottom': '20px'}),
],
    fluid=True  # Faz o container ocupar toda a largura da tela
)

# Run the app
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
