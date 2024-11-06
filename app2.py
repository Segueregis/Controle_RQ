import pandas as pd
from dash import dcc, html, Dash, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Inicialize o novo app com tema Bootstrap
app2 = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.themes.DARKLY])

# Carregar os dados para uso em `app2.py`
df_outubro = pd.read_excel('Controle_orcamento_outubro.xlsx', sheet_name='Base')
df_novembro = pd.read_excel('Controle_orcamento_novembro.xlsx', sheet_name='Base')

# Layout do segundo dashboard
app2.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H3("Dashboard Número RQ"), width="auto")
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Input(id="rq-input", type="text", placeholder="Digite o Número RQ")
        ),
        dbc.Col(
            dbc.Button("Buscar", id="buscar-rq", n_clicks=0)
        )
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="rq-table"))
    ])
])


# Callback para atualizar a tabela com base no Número RQ
@app2.callback(
    Output("rq-table", "figure"),
    Input("buscar-rq", "n_clicks"),
    State("rq-input", "value")
)
def update_table(n_clicks, rq_number):
    if n_clicks > 0 and rq_number:  # Verifica se o botão foi clicado e se há um número de RQ
        # Filtra em ambos os DataFrames de Outubro e Novembro
        df_filtered = pd.concat([
            df_outubro[df_outubro['REQUISICAO'] == rq_number],
            df_novembro[df_novembro['REQUISICAO'] == rq_number]
        ])

        if not df_filtered.empty:
            fig = go.Figure(data=[go.Table(
                columnwidth=[200 for _ in df_filtered.columns],  # Largura padrão de 200 pixels por coluna
                header=dict(values=list(df_filtered.columns), align="left"),
                cells=dict(values=[df_filtered[col].tolist() for col in df_filtered.columns], align="left")
            )])
        else:
            fig = go.Figure(data=[go.Table(
                header=dict(values=["Nenhum dado encontrado"]),
                cells=dict(values=[["Verifique o Número RQ inserido"]])
            )])
        return fig

    # Retorna uma tabela em branco se nada for filtrado
    return go.Figure()


if __name__ == "__main__":
    app2.run_server(debug=True)
