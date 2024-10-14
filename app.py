import pandas as pd
from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO

# Inicializando o app Dash com tema Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.themes.DARKLY])

# Carregar as despesas da planilha
df_excel = pd.read_excel('Controle_orcamento.xlsx', sheet_name='Base')

# Exemplo de Orçamento Fixo para cada UT e Categoria
data = {
    '12': {'UNIFORME': 1459.10, 'EPI': 3315.28, 'FERRAMENTAS': 1633.50, 'MATERIAL APLICADO': 3448.50,
           'MATERIAL CONSUMO': 889.35, 'LOCAÇÃO MÁQUINAS': 381.15, 'DESPESA INFORMÁTICA': 80.00,
           'DESPESA TELEFONES CELULARES': 419.35, 'SERVIÇOS CONTRATADOS': 1089.00,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 290.40,
           'MANUTENÇÃO DE VEÍCULOS': 108.90, 'BENS DE VALORES IRRELEVANTES': 308.55},
    '31': {'UNIFORME': 5272.79, 'EPI': 4583.69, 'FERRAMENTAS': 1452.00, 'MATERIAL APLICADO': 9801.00,
           'MATERIAL CONSUMO': 13794.00, 'LOCAÇÃO CARROS': 5262.80, 'LOCAÇÃO GESTÃO ATIVOS': 11980.64,
           'LOCAÇÃO MÁQUINAS': 7121.47, 'DESPESA INFORMÁTICA': 120.00, 'DESPESA TELEFONES CELULARES': 454.24,
           'SERVIÇOS CONTRATADOS': 6534.00, 'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 7078.50,
           'MANUTENÇÃO DE VEÍCULOS': 816.75,
           'CARTÃO COMBUSTÍVEL': 3601.07, 'REFEIÇÕES EXTRAS': 110.00, 'PEDAGIO': 180.00,
           'BENS DE VALORES IRRELEVANTES': 290.40,
           'ESTACIONAMENTO': 20.00},
    '26': {'UNIFORME': 2968.74, 'EPI': 2546.63, 'FERRAMENTAS': 889.35, 'MATERIAL APLICADO': 5000.00,
           'MATERIAL CONSUMO': 5000.00, 'LOCAÇÃO MÁQUINAS': 10890.00, 'DESPESA INFORMÁTICA': 320.00,
           'DESPESA TELEFONES CELULARES': 429.27, 'SERVIÇOS CONTRATADOS': 889.35,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 2286.90,
           'MANUTENÇÃO DE VEÍCULOS': 108.90, 'CARTÃO COMBUSTÍVEL': 2281.90, 'PEDAGIO': 680.00,
           'BENS DE VALORES IRRELEVANTES': 1089.00,
           'LOCAÇÃO DE CARROS LEVES': 4531.56},
    '20': {'UNIFORME': 930.12, 'EPI': 1329.40, 'FERRAMENTAS': 771.38, 'MATERIAL APLICADO': 95269.68,
           'MATERIAL CONSUMO': 12514.75, 'LOCAÇÃO MÁQUINAS': 8893.50, 'DESPESA INFORMÁTICA': 120.00,
           'DESPESA TELEFONES CELULARES': 93.19, 'SERVIÇOS CONTRATADOS': 9801.00,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 4083.75,
           'MANUTENÇÃO DE VEÍCULOS': 381.15, 'CARTÃO COMBUSTÍVEL': 653.40, 'BENS DE VALORES IRRELEVANTES': 2178.00,
           'MANUT. FERRAM. DISPOSITIVOS MOVEIS': 199.65,
           'LOCAÇÃO DE CARROS LEVES': 1197.90, 'LOCAÇÃO GESTAO DE ATIVOS': 972.33}
}


# Função para processar os dados de cada UT
def process_ut_data(ut_key, data, df_excel):
    # Converter a coluna 'UTS' para string e filtrar os dados da UT correspondente
    df_cru = df_excel[df_excel['UTS'].astype(str) == str(ut_key)]

    # Agrupar os dados pela categoria e somar as despesas
    df_grouped = df_cru.groupby('CATEGORIA')['DESPESAS'].sum().reset_index()

    # Adicionar as categorias e seus orçamentos ao DataFrame
    df_grouped['Orçamento'] = df_grouped['CATEGORIA'].map(data)

    # Calcular a diferença
    df_grouped['SALDO'] = df_grouped['Orçamento'] - df_grouped['DESPESAS']

    # Calcular totais
    orçamento_total = df_grouped['Orçamento'].sum()
    despesas_totais = df_grouped['DESPESAS'].sum()
    saldo_final = orçamento_total - despesas_totais

    return df_grouped, orçamento_total, despesas_totais, saldo_final


# Função para criar gráfico
def criar_grafico(df, ut_key):
    fig = go.Figure()

    # Traço para Orçamento
    fig.add_trace(go.Bar(
        x=df['CATEGORIA'], y=df['Orçamento'], name='Orçamento',
        marker=dict(color='rgba(58, 71, 80, 0.6)')
    ))

    # Traço para Despesas
    fig.add_trace(go.Bar(
        x=df['CATEGORIA'], y=df['DESPESAS'], name='DESPESAS',
        marker=dict(color='rgba(255, 165, 0, 0.6)')  # Cor laranja
    ))

    # Traço para Diferença, com cores baseadas no valor
    fig.add_trace(go.Bar(
        x=df['CATEGORIA'], y=df['SALDO'], name='SALDO',
        marker=dict(color=df['SALDO'].apply(lambda x: 'red' if x < 0 else 'green'))
    ))

    # Atualizar layout
    fig.update_layout(
        title=f"Controle Financeiro {ut_key}",
        yaxis_title="Valor em R$",
        xaxis_title="Categorias",
        barmode='group',  # Barras agrupadas
        height=700
    )

    return fig


# Criar os dados processados e gráficos para cada UT
ut_data = {ut_key: process_ut_data(ut_key, data[ut_key], df_excel) for ut_key in data.keys()}
figures = {ut_key: criar_grafico(ut_data[ut_key][0], ut_key) for ut_key in ut_data.keys()}

# Layout do dashboard
app.layout = dbc.Container([
    # Troca de tema e título
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Controle de Orçamento", style={'font-size': '20px', 'font-weight': 'bold'}),
                            html.P("JOHNSON & KENVUE ",
                                   style={'font-size': '16px', 'font-weight': 'bold'})
                        ], sm=12, md=8),

                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.FLATLY, dbc.themes.DARKLY]),
                        ], sm=12, md=4),
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Oracle", href="https://login-euld-saasfaprod1.fa.ocs.oraclecloud.com/",
                                   target="_blank", color="danger")
                    ], style={'margin-top': '30px'})
                ])
            ], style={'height': '100%'})
        ], sm=12, lg=4)
    ]),

    # Criar linhas para cada UT
    *[
        dbc.Row([
            dbc.Col([
                # Dropdown de filtro de categoria
                dcc.Dropdown(
                    id=f'categoria-dropdown-ut-{ut_key}',
                    options=[{'label': categoria, 'value': categoria} for categoria in df_excel['CATEGORIA'].unique()],
                    value=None,  # Valor inicial
                    placeholder="Selecione uma categoria",
                ),
                # Informações de Orçamento
                dbc.Card([
                    dbc.CardBody([
                        html.H5(f"Orçamento Total {ut_key}: R$ {ut_data[ut_key][1]:,.2f}"),
                        html.H5(f"Total Gasto {ut_key}: R$ {ut_data[ut_key][2]:,.2f}"),
                        html.H5(f"Saldo Final {ut_key}: R$ {ut_data[ut_key][3]:,.2f}",
                                style={"color": "red" if ut_data[ut_key][3] < 0 else "green"}),
                    ], style={'padding': '10px'})
                ], style={'height': '120px', 'margin-bottom': '10px'}),
                # Gráfico da UT
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id=f'graph-ut-{ut_key}', figure=figures[ut_key], style={'width': '100%', 'height': '600px'})
                    ])
                ]),
            ], width=12),
        ], style={'margin-bottom': '20px'})
        for ut_key in data.keys()
    ]
], fluid=True)


# Callbacks para atualizar os gráficos ao selecionar uma categoria no dropdown
for ut_key in data.keys():
    @app.callback(
        Output(f'graph-ut-{ut_key}', 'figure'),
        [Input(f'categoria-dropdown-ut-{ut_key}', 'value')]
    )
    def update_graph(categoria_selecionada, ut_key=ut_key):
        df, _, _, _ = process_ut_data(ut_key, data[ut_key], df_excel)
        if categoria_selecionada:
            df = df[df['CATEGORIA'] == categoria_selecionada]  # Filtrar a categoria selecionada
        return criar_grafico(df, ut_key)


# Run the app
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
