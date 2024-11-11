from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import io
from flask import Flask

# Inicializar o servidor Flask
server = Flask(__name__)

# Criar o app Dash usando o servidor Flask
app2 = Dash(__name__, server=server, external_stylesheets=[dbc.themes.FLATLY, dbc.themes.DARKLY])

# Carregar os dados para uso em `app2.py`
df_outubro = pd.read_excel('Controle_orcamento_outubro.xlsx', sheet_name='Base')
df_novembro = pd.read_excel('Controle_orcamento_novembro.xlsx', sheet_name='Base')

# Layout do segundo dashboard
app2.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("Dashboard Número RQ"), width="auto")
    ]),
    dbc.Row([
        dbc.Col(dcc.Input(id="rq-input", type="text", placeholder="Digite o Número RQ")),
        dbc.Col(dcc.DatePickerSingle(id='data-inicio', placeholder='Data Início')),
        dbc.Col(dcc.DatePickerSingle(id='data-fim', placeholder='Data Fim')),
        dbc.Col(dbc.Button("Buscar", id="buscar-rq", n_clicks=0)),
        dbc.Col(dbc.Button("Baixar Excel", id="download-excel", n_clicks=0, color="success"))
    ]),
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id="rq-table",
            style_table={'overflowX': 'auto'},
            style_data={'color': 'black', 'backgroundColor': 'white'},  # Cor do texto preta e fundo branco
            style_header={'backgroundColor': 'lightgrey', 'color': 'black', 'fontWeight': 'bold'}
        )),
        dcc.Download(id="download-dataframe-xlsx")
    ])
])


# Callback para atualizar a tabela com base no Número RQ e no intervalo de datas
@app2.callback(
    Output("rq-table", "data"),
    Output("rq-table", "columns"),
    Output("download-dataframe-xlsx", "data"),
    Input("buscar-rq", "n_clicks"),
    Input("download-excel", "n_clicks"),
    State("rq-input", "value"),
    State("data-inicio", "date"),
    State("data-fim", "date"),
    prevent_initial_call=True
)
def update_table_and_download(n_clicks_buscar, n_clicks_download, rq_number, data_inicio, data_fim):
    # Concatenar os dados de outubro e novembro
    df_combined = pd.concat([df_outubro, df_novembro])

    # Filtrar pelo Número RQ, se fornecido
    if rq_number:
        df_filtered = df_combined[df_combined['REQUISICAO'] == rq_number]
    else:
        df_filtered = df_combined

    # Filtrar pelo intervalo de datas, se ambas as datas forem fornecidas
    if data_inicio and data_fim:
        df_filtered = df_filtered[
            (df_filtered['DATA CRIACAO'] >= data_inicio) &
            (df_filtered['DATA CRIACAO'] <= data_fim)
            ]

    # Formatar a coluna 'DATA CRIACAO' para o formato DD/MM/AAAA
    if 'DATA CRIACAO' in df_filtered.columns:
        df_filtered['DATA CRIACAO'] = pd.to_datetime(df_filtered['DATA CRIACAO']).dt.strftime('%d/%m/%Y')

    # Formatar a coluna 'DESPESAS' como moeda em R$
    if 'DESPESAS' in df_filtered.columns:
        df_filtered['DESPESAS'] = df_filtered['DESPESAS'].apply(lambda x: f"R$ {x:,.2f}")

    # Configurar as colunas para o dash_table.DataTable
    columns = [{"name": col, "id": col} for col in df_filtered.columns]

    # Preparar os dados para exibição na tabela
    data = df_filtered.to_dict('records')

    # Se o botão de download for clicado, gerar o arquivo Excel em memória
    if n_clicks_download > 0 and not df_filtered.empty:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Converte a coluna 'DESPESAS' para número antes de salvar no Excel
            df_excel = df_filtered.copy()
            df_excel['DESPESAS'] = df_excel['DESPESAS'].replace({'R\$ ': '', ',': ''}, regex=True).astype(float)
            df_excel.to_excel(writer, index=False, sheet_name='Dados Filtrados')
            writer.close()
        buffer.seek(0)
        return data, columns, dcc.send_bytes(buffer.getvalue(), "dados_filtrados.xlsx")

    return data, columns, None


# Defina a rota para a URL /app2
@app2.server.route('/app2')
def serve_app2():
    return app2.layout  # Retorna o layout de app2

# Não é necessário redefinir o 'server' aqui. O servidor já foi atribuído.
