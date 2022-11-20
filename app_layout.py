from dash import html, dcc

layout = html.Div(children=[
    html.H1(children='Rock Paper Scissors'),
    html.Div(id='score'),
    html.Div(children='Enter player 1 name:'),
    dcc.Input(id='player1-name', value='Player 1', type='text'),
    html.Div(children='Enter player 2 name:'),
    dcc.Input(id='player2-name', value='Player 2', type='text'),
    html.Button('Set player names', id='names-submit-button'),
    html.Br(),

    html.Div(children='Set computer as player 2?:'),
    dcc.RadioItems(
        id='computer-player',
        options=[
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False}
        ],
        value=False
    ),
    html.Div(id='player2-status', children="Player 2 is not computer"),

    html.Br(),
    html.Div(id='player names'),
    html.Div(
        html.Div([
            'Player 1 choose a move:   ',
            html.Button('🪨Rock', id='player1-rock', n_clicks=0),
            html.Button('📜Paper', id='player1-paper', n_clicks=0),
            html.Button('✂Scissors', id='player1-scissors', n_clicks=0),
        ],
            id='choose-move-1', ),
    ),
    html.Div([
        "Player 2 choose a move:   ",
        html.Button('🪨Rock', id='player2-rock', n_clicks=0),
        html.Button('📜Paper', id='player2-paper', n_clicks=0),
        html.Button('✂Scissors', id='player2-scissors', n_clicks=0),
        # simple text
    ], id='choose-move-2',  # children='Player 2 choose a move:'),
    ),

    html.Br(),
    html.P(id='output-container-button',
           children='Select a move and click submit'),
    html.P(id='who-played-what', children=''),
    html.Br(),

    html.Button('Save game', id='save-button', n_clicks=0),
    html.Div(id='save-output-container-button'),

    html.Button('Load game', id='load-button', n_clicks=0),
    html.Div(id='load-output-container-button'),
])
