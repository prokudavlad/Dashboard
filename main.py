import csv
import json
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Sony PlayStation games
games = ['The Last of Us', 'Uncharted 4: A Thief\'s End', 'Bloodborne', 'Horizon Zero Dawn',
         'God of War', 'Shadow of the Colossus', 'Persona 5', 'Marvel\'s Spider-Man',
         'The Witcher 3: Wild Hunt', 'Death Stranding']

# entry in CSV-file
with open('playstation_games.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Game'])
    for game in games:
        writer.writerow([game])

# entry in JSON-file
with open('playstation_games.json', mode='w') as file:
    json.dump(games, file)

# Loading data
data = pd.read_csv('playstation_games.csv')

# Application initialization Dash
app = dash.Dash(__name__)

# Defining the Application Layout
app.layout = html.Div([
    # Header
    html.H1('Sony PlayStation games'),

    # Controls for filtering data
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': game, 'value': game} for game in data['Game']],
        value=data['Game'][0],
        clearable=False
    ),

    # Schedule
    dcc.Graph(id='graph'),

    # Table with data
    html.Table(id='table', children=[
        html.Thead([
            html.Tr([html.Th('Game')])
        ]),
        html.Tbody([
            html.Tr([html.Td(game)]) for game in data['Game']
        ])
    ]),

    # Number of games
    html.P(f'Number of games: {len(data)}'),

    # List of developers
    html.P(f'Developers: Naughty Dog, FromSoftware, Guerrilla Games, Santa Monica Studio, '
           f'Bluepoint Games, Atlus, Insomniac Games, CD Projekt RED, Kojima Productions')
])

# Function to update graph and table
@app.callback(
    [Output('graph', 'figure'),
     Output('table', 'children')],
    [Input('dropdown', 'value')]
)
def update_figure_and_table(selected_game):
    filtered_data = data[data['Game'] == selected_game]
    # Creating a Graph
    fig = {
        'data': [{'x': [selected_game], 'y': [1], 'type': 'bar'}],
        'layout': {'title': f'Number of games: {len(filtered_data)}'}
    }

    # Create a table
    table = html.Table(id='table', children=[
        html.Thead([
            html.Tr([html.Th('Game')])
        ]),
        html.Tbody([
            html.Tr([html.Td(selected_game)])
        ])
    ])
    return fig, table

# Application launch
if __name__ == '__main__':
    app.run_server(debug=True)
