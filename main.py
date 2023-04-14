import csv
import json
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Список игр Sony PlayStation
games = ['The Last of Us', 'Uncharted 4: A Thief\'s End', 'Bloodborne', 'Horizon Zero Dawn',
         'God of War', 'Shadow of the Colossus', 'Persona 5', 'Marvel\'s Spider-Man',
         'The Witcher 3: Wild Hunt', 'Death Stranding']

# Запись в CSV-файл
with open('playstation_games.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Game'])
    for game in games:
        writer.writerow([game])

# Запись в JSON-файл
with open('playstation_games.json', mode='w') as file:
    json.dump(games, file)

# Загрузка данных
data = pd.read_csv('playstation_games.csv')

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Определение макета приложения
app.layout = html.Div([
    # Заголовок
    html.H1('Sony PlayStation games'),

    # Элементы управления для фильтрации данных
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': game, 'value': game} for game in data['Game']],
        value=data['Game'][0],
        clearable=False
    ),

    # График
    dcc.Graph(id='graph'),

    # Таблица с данными
    html.Table(id='table', children=[
        html.Thead([
            html.Tr([html.Th('Game')])
        ]),
        html.Tbody([
            html.Tr([html.Td(game)]) for game in data['Game']
        ])
    ]),

    # Количество игр
    html.P(f'Number of games: {len(data)}'),

    # Список разработчиков
    html.P(f'Developers: Naughty Dog, FromSoftware, Guerrilla Games, Santa Monica Studio, '
           f'Bluepoint Games, Atlus, Insomniac Games, CD Projekt RED, Kojima Productions')
])

# Функция для обновления графика и таблицы
@app.callback(
    [Output('graph', 'figure'),
     Output('table', 'children')],
    [Input('dropdown', 'value')]
)
def update_figure_and_table(selected_game):
    filtered_data = data[data['Game'] == selected_game]
    # Создание графика
    fig = {
        'data': [{'x': [selected_game], 'y': [1], 'type': 'bar'}],
        'layout': {'title': f'Number of games: {len(filtered_data)}'}
    }

    # Создание таблицы
    table = html.Table(id='table', children=[
        html.Thead([
            html.Tr([html.Th('Game')])
        ]),
        html.Tbody([
            html.Tr([html.Td(selected_game)])
        ])
    ])
    return fig, table

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
