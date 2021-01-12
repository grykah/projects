import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

PROJ_ROOT = os.path.join(os.pardir)
data_path = os.path.join(PROJ_ROOT, 'MentalHealth', 'clean_mht_survey.csv')

data = pd.read_csv(data_path)

app = dash.Dash(__name__)
server = app.server

country_names = data.Country.unique()
country_names.sort()

app.layout = html.Div([
    html.Div([dcc.Dropdown(id='country-select', 
                           options=[{'label': i, 'value': i} for i in country_names],
                           value='TOR', style={'width': '140px'})]),
    dcc.Graph('shot-dist-graph', config={'displayModeBar': False})])

@app.callback(
    Output('shot-dist-graph', 'figure'),
    [Input('country-select', 'value')]
)

def update_graph(cntrname = 'United States'):
    import plotly.express as px
    return px.scatter(data[data.Country == cntrname], 
                      x = 'Age', y = 'state', 
                      color = 'treatment')

if __name__ == '__main__':
    app.run_server(debug=False)