import pandas as pd
from dash import dcc, html, Dash, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO


# Inicialize o app com tema Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.themes.DARKLY])
app.config.suppress_callback_exceptions = True



# Carregar as despesas da planilha
df_outubro = pd.read_excel('Controle_orcamento_outubro.xlsx', sheet_name='Base')
df_novembro = pd.read_excel('Controle_orcamento_novembro.xlsx', sheet_name='Base')
df_dezembro = pd.read_excel('Controle_orcamento_dezembro.xlsx', sheet_name='Base')



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
           'MANUT. FERRAM. DISPOSITIVOS MOVEIS': 199.65, 'REFEIÇÕES EXTRAS': 420.00, 'TREINAMENTOS OBRIGATORIOS': 726.00,
           'HOSPEDAGEM': 653.40, 'COMBUSTIVEL': 72.60,
           'LOCAÇÃO DE CARROS LEVES': 1197.90, 'LOCAÇÃO GESTAO DE ATIVOS': 972.33}
}

data_novembro = {
    '12': {'UNIFORME': 1459.10, 'EPI': 3315.28, 'FERRAMENTAS': 1633.50, 'MATERIAL APLICADO': 3448.50,
           'MATERIAL CONSUMO': 889.35, 'LOCAÇÃO MÁQUINAS': 381.15, 'DESPESA INFORMÁTICA': 80.00,
           'DESPESA TELEFONES CELULARES': 419.35, 'SERVIÇOS CONTRATADOS': 1089.00,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 290.40,
           'MANUTENÇÃO DE VEÍCULOS': 108.90, 'BENS DE VALORES IRRELEVANTES': 308.55},
    '31': {'UNIFORME': 5272.79, 'EPI': 4583.69, 'FERRAMENTAS': 1452.00, 'MATERIAL APLICADO': 9801.00,
           'MATERIAL CONSUMO': 13794.00, 'LOCAÇÃO CARROS': 5262.80, 'LOCAÇÃO GESTÃO ATIVOS': 11980.64,
           'LOCAÇÃO MÁQUINAS': 7168.47, 'DESPESA INFORMÁTICA': 120.00, 'DESPESA TELEFONES CELULARES': 454.24,
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
           'MATERIAL CONSUMO': 12877.75, 'LOCAÇÃO MÁQUINAS': 8893.50, 'DESPESA INFORMÁTICA': 120.00,
           'DESPESA TELEFONES CELULARES': 93.19, 'SERVIÇOS CONTRATADOS': 9801.00,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 4083.75,
           'MANUTENÇÃO DE VEÍCULOS': 381.15, 'CARTÃO COMBUSTÍVEL': 653.40, 'BENS DE VALORES IRRELEVANTES': 2178.00,
           'MANUT. FERRAM. DISPOSITIVOS MOVEIS': 199.65, 'REFEIÇÕES EXTRAS': 420.00, 'TREINAMENTOS OBRIGATORIOS': 726.00,
           'HOSPEDAGEM': 653.40, 'COMBUSTIVEL': 72.60,
           'LOCAÇÃO DE CARROS LEVES': 1197.90, 'LOCAÇÃO GESTAO DE ATIVOS': 972.33}
}
data_dezembro = {
    '12': {'UNIFORME': 1493.48, 'EPI': 3315.28, 'FERRAMENTAS': 1633.50, 'MATERIAL APLICADO': 3448.50,
           'MATERIAL CONSUMO': 889.35, 'LOCAÇÃO MÁQUINAS': 381.15, 'DESPESA INFORMÁTICA': 80.00,
           'DESPESA TELEFONES CELULARES': 419.35, 'SERVIÇOS CONTRATADOS': 1089.00,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 290.40,
           'MANUTENÇÃO DE VEÍCULOS': 108.90, 'BENS DE VALORES IRRELEVANTES': 308.55},
    '31': {'UNIFORME': 5272.79, 'EPI': 4583.69, 'FERRAMENTAS': 1452.00, 'MATERIAL APLICADO': 9801.00,
           'MATERIAL CONSUMO': 13794.00, 'LOCAÇÃO CARROS': 5262.80, 'LOCAÇÃO GESTÃO ATIVOS': 11980.64,
           'LOCAÇÃO MÁQUINAS': 6974.38, 'DESPESA INFORMÁTICA': 120.00, 'DESPESA TELEFONES CELULARES': 454.24,
           'SERVIÇOS CONTRATADOS': 6534.00, 'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 7078.50,
           'MANUTENÇÃO DE VEÍCULOS': 816.75,
           'CARTÃO COMBUSTÍVEL': 3601.07, 'REFEIÇÕES EXTRAS': 110.00, 'PEDAGIO': 180.00,
           'BENS DE VALORES IRRELEVANTES': 290.40,
           'ESTACIONAMENTO': 20.00},
    '26': {'UNIFORME': 2968.74, 'EPI': 2546.63, 'FERRAMENTAS': 889.35, 'MATERIAL APLICADO': 5000.00,
           'MATERIAL CONSUMO': 5000.00, 'LOCAÇÃO MÁQUINAS': 10890.00, 'DESPESA INFORMÁTICA': 320.00,
           'DESPESA TELEFONES CELULARES': 429.77, 'SERVIÇOS CONTRATADOS': 889.35,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 2286.90,
           'MANUTENÇÃO DE VEÍCULOS': 108.90, 'CARTÃO COMBUSTÍVEL': 2281.90, 'PEDAGIO': 680.00,
           'BENS DE VALORES IRRELEVANTES': 1089.00,
           'LOCAÇÃO DE CARROS LEVES': 4531.56},
    '20': {'UNIFORME': 930.12, 'EPI': 1102.52, 'FERRAMENTAS': 771.38, 'MATERIAL APLICADO': 90732.18,
           'MATERIAL CONSUMO': 12877.75, 'LOCAÇÃO MÁQUINAS': 8893.50, 'DESPESA INFORMÁTICA': 120.00,
           'DESPESA TELEFONES CELULARES': 93.19, 'SERVIÇOS CONTRATADOS': 9801.00,
           'MATERIAIS E PEÇAS DE REPOSIÇÃO EQUIP.': 4083.75,
           'MANUTENÇÃO DE VEÍCULOS': 381.15, 'CARTÃO COMBUSTÍVEL': 653.40, 'BENS DE VALORES IRRELEVANTES': 2178.00,
           'MANUT. FERRAM. DISPOSITIVOS MOVEIS': 199.65, 'REFEIÇÕES EXTRAS': 420.00, 'TREINAMENTOS OBRIGATORIOS': 726.00,
           'HOSPEDAGEM': 653.40, 'COMBUSTIVEL': 72.60,
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


# Função para processar os dados de cada UT
def process_ut_data(ut_key, data, df_excel):
    df_cru = df_excel[df_excel['UTS'].astype(str) == str(ut_key)]
    df_grouped = df_cru.groupby('CATEGORIA')['DESPESAS'].sum().reset_index()
    df_grouped['Orçamento'] = df_grouped['CATEGORIA'].map(data)
    df_grouped['SALDO'] = df_grouped['Orçamento'] - df_grouped['DESPESAS']
    orçamento_total = df_grouped['Orçamento'].sum()
    despesas_totais = df_grouped['DESPESAS'].sum()
    saldo_final = orçamento_total - despesas_totais
    return df_grouped, orçamento_total, despesas_totais, saldo_final

# Função para criar gráfico
def criar_grafico(df, ut_key):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['CATEGORIA'], y=df['Orçamento'], name='Orçamento', marker=dict(color='rgba(58, 71, 80, 0.6)')))
    fig.add_trace(go.Bar(x=df['CATEGORIA'], y=df['DESPESAS'], name='Despesas', marker=dict(color='rgba(255, 165, 0, 0.6)')))
    fig.add_trace(go.Bar(x=df['CATEGORIA'], y=df['SALDO'], name='Saldo', marker=dict(color=df['SALDO'].apply(lambda x: 'red' if x < 0 else 'green'))))
    fig.update_layout(title=f"Controle Financeiro {ut_key}", yaxis_title="Valor em R$", xaxis_title="Categorias", barmode='group', height=700)
    return fig


# Dados e gráficos para cada UT
ut_data = {ut_key: process_ut_data(ut_key, data[ut_key], df_outubro) for ut_key in data.keys()}
ut_data = {ut_key: process_ut_data(ut_key, data_dezembro[ut_key], df_dezembro) for ut_key in ['12', '31', '26', '20']}
figures = {ut_key: criar_grafico(ut_data[ut_key][0], ut_key) for ut_key in ut_data.keys()}

# Configuração do menu hambúrguer com ícone personalizado
hamburger_menu = html.Div(
    [
        dbc.Button(
            html.Img(
                src="/assets/menu.png",  # Caminho para o ícone no diretório assets
                style={
                    "width": "35px",  # Tamanho do ícone
                    "height": "35px",
                    "cursor": "pointer",  # Mostra que é clicável
                }
            ),
            id="open-offcanvas",
            color="secondary",
            style={"width": "30px", "height": "30px", "padding": "5px", "background-color": "transparent", "border": "none"}
        ),
        dbc.Offcanvas(
            [
                html.H5("Menu", className="offcanvas-title"),
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            "CLICK AQUI PARA PESQUISAR RQ",
                            href="https://controle-rq-2.onrender.com",  # Link para a página do projeto
                            target="_blank",  # Abre em uma nova aba
                            id="num-rq-link",
                        ),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            id="offcanvas",
            is_open=False,
            placement="start"
        ),
    ]
)





# Layout do dashboard
app.layout = dbc.Container([
    # Linha para o menu hambúrguer
    dbc.Row(
        [
            dbc.Col(hamburger_menu, width="auto"),  # Inclui o menu com o ícone personalizado
        ],
        style={'margin-bottom': '20px', 'justify-content': 'flex-start'}  # Alinha o menu no canto superior esquerdo
    ),

    # Linha para o dropdown do mês
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        # Texto de título e legenda ao lado do dropdown
                        dbc.Col([
                            html.Legend("Controle de Orçamento", style={'font-size': '20px', 'font-weight': 'bold'}),
                            html.P("JOHNSON & KENVUE", style={'font-size': '16px', 'font-weight': 'bold'}),
                        ], width="auto"),

                        # Dropdown de mês ao lado do título
                        dbc.Col([
                            dbc.Card([
                                dcc.Dropdown(
                                    id='mes-dropdown',
                                    options=[{'label': 'Outubro', 'value': 'outubro'},
                                             {'label': 'Novembro', 'value': 'novembro'},
                                             {'label': 'Dezembro', 'value': 'dezembro'}],
                                    value='dezembro',
                                    placeholder="Selecione um mês",
                                    style={
                                        'width': '150px',
                                        'background-color': '#f8f9fa',  # Cor de fundo dentro do dropdown
                                        'color': '#333333',  # Cor do texto
                                        'border': '1px solid #cccccc'  # Borda cinza claro
                                    }
                                )
                            ], style={'background-color': '#f5f5f5', 'padding': '5px'})
                            # Fundo cinza bem claro e padding ao redor do dropdown
                        ], width="auto"),

                        # Botão de troca de tema
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.FLATLY, dbc.themes.DARKLY])
                        ], width="auto")
                    ], align="center", justify="start", style={'margin-top': '10px'}),

                    # Botão Oracle
                    dbc.Row([
                        dbc.Button("Oracle", href="https://login-euld-saasfaprod1.fa.ocs.oraclecloud.com/",
                                   target="_blank", color="danger")
                    ], style={'margin-top': '30px'})
                ])
            ], style={'height': '100%'})
        ], sm=12, lg=4)
    ], style={'margin-bottom': '20px'}),

    # Cartões e gráficos para cada UT
    *[
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5(f"Orçamento Total {ut_key}: R$ {ut_data[ut_key][1]:,.2f}",
                                id=f'orçamento-total-{ut_key}'),
                        html.H5(f"Total Gasto {ut_key}: R$ {ut_data[ut_key][2]:,.2f}", id=f'total-gasto-{ut_key}'),
                        html.H5(f"Saldo Final {ut_key}: R$ {ut_data[ut_key][3]:,.2f}",
                                id=f'saldo-final-{ut_key}',
                                style={"color": "red" if ut_data[ut_key][3] < 0 else "green"})
                    ], style={'padding': '10px'})
                ], style={'height': '120px', 'margin-bottom': '10px'}),

                # Gráfico para a UT
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id=f'graph-ut-{ut_key}', figure=figures[ut_key],
                                  style={'width': '100%', 'height': '600px'})
                    ])
                ]),
            ], width=12),
        ], style={'margin-bottom': '20px'})
        for ut_key in data.keys()
    ]
], fluid=True)


## Callback para atualizar os gráficos e as informações ao selecionar um mês
@app.callback(
    [Output(f'graph-ut-{ut_key}', 'figure') for ut_key in data.keys()] +
    [Output(f'orçamento-total-{ut_key}', 'children') for ut_key in data.keys()] +
    [Output(f'total-gasto-{ut_key}', 'children') for ut_key in data.keys()] +
    [Output(f'saldo-final-{ut_key}', 'children') for ut_key in data.keys()],
    [Input('mes-dropdown', 'value')]
)
def update_graphs(selected_month):
    if selected_month == 'outubro':
        df_excel = df_outubro
        current_data = data
    elif selected_month == 'novembro':
        df_excel = df_novembro
        current_data = data_novembro
    elif selected_month == 'dezembro':
        df_excel = df_dezembro  # Aqui, você precisa definir o df_dezembro
        current_data = data_dezembro  # E também o data_dezembro
    else:
        # Se o mês selecionado não for outubro, novembro nem dezembro, você pode definir um comportamento padrão
        df_excel = df_outubro
        current_data = data

    ut_data = {ut_key: process_ut_data(ut_key, current_data[ut_key], df_excel) for ut_key in data.keys()}

    figures = [criar_grafico(ut_data[ut_key][0], ut_key) for ut_key in ut_data.keys()]
    orcamentos = [f"Orçamento Total {ut_key}: R$ {ut_data[ut_key][1]:,.2f}" for ut_key in data.keys()]
    gastos = [f"Total Gasto {ut_key}: R$ {ut_data[ut_key][2]:,.2f}" for ut_key in data.keys()]
    saldos = [f"Saldo Final {ut_key}: R$ {ut_data[ut_key][3]:,.2f}" for ut_key in data.keys()]

    return figures + orcamentos + gastos + saldos

# Callback para abrir e fechar o menu
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    State("offcanvas", "is_open")
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open




# Run the app
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)





# ESSE E A ULTIMA ATUALIZAÇÃO DO APP.PY
