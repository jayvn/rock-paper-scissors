import pickle
from random import choice

import dash

from dash.dependencies import Output, Input

from app_layout import layout
from game_objects import Player, get_winner


def parse_move_string(trigger):
    if trigger.endswith('rock'):
        return "Rock"
    elif trigger.endswith('paper'):
        return "Paper"
    elif trigger.endswith('scissors'):
        return "Scissors"


if __name__ == '__main__':
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    player2_is_computer = False

    app = dash.Dash(__name__)
    app.layout = layout


    @app.callback(Output('player names', 'children'),
                  [Input('names-submit-button', 'n_clicks')],
                  [dash.dependencies.State('player1-name', 'value'),
                   dash.dependencies.State('player2-name', 'value')],
                  prevent_initial_call=True)
    def set_player_names(n_clicks, player1_name, player2_name):
        player1.name = player1_name
        player2.name = player2_name
        return f'''Player 1: "{player1.name}" vs Player 2: "{player2.name}"'''


    @app.callback([Output('player2-status', 'children'),
                   Output('player2-rock', 'disabled'),
                   Output('player2-paper', 'disabled'),
                   Output('player2-scissors', 'disabled'),
                   Output('choose-move-2', 'style')
                   ],
                  [Input('computer-player', 'value')])
    def set_computer_player(value):
        global player2_is_computer
        player2_is_computer = value
        if value:
            return f'{player2.name} is computer', True, True, True, {'display': 'none'}

        return f'{player2.name} is not computer', False, False, False, {'display': 'block'}


    @app.callback([Output('score', 'children'),
                   Output('output-container-button', 'children'),
                   Output('who-played-what', 'children')
                   ],
                  [Input('player1-rock', 'n_clicks'),
                   Input('player1-paper', 'n_clicks'),
                   Input('player1-scissors', 'n_clicks'),
                   Input('player2-rock', 'n_clicks'),
                   Input('player2-paper', 'n_clicks'),
                   Input('player2-scissors', 'n_clicks')],
                  prevent_initial_call=True)
    def update_output(n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6):

        prop_id = dash.callback_context.triggered[0]['prop_id']
        if prop_id.startswith('player1'):
            trigger = prop_id.split('.')[0]
            player1.move = parse_move_string(trigger)
        elif prop_id.startswith('player2'):
            trigger = prop_id.split('.')[0]
            player2.move = parse_move_string(trigger)

        scoreboard = dash.no_update
        who_played_what = dash.no_update

        yet_to_play = ""
        if player1.move is None:
            yet_to_play = ','.join([player1.name, yet_to_play])
        if player2.move is None:
            if player2_is_computer:
                player2.move = choice(["Rock", "Paper", "Scissors"])
            else:
                yet_to_play = ','.join([player2.name, yet_to_play])

        if yet_to_play:
            return scoreboard, f'Yet to play: {yet_to_play}', who_played_what

        winner = get_winner(player1, player2)
        if winner is None:
            result = 'Tie!'
        else:
            winner.add_score()
            scoreboard = f'Scoreboard--:>  {player1.name} : [ {player1.score} ] |  {player2.name} : [ {player2.score} ]'
            who_played_what = f'{player1.name} played {player1.move} and {player2.name} played {player2.move}'
            result = f'{winner.name} wins! Start a new round by playing a move.'
            player1.move = player2.move = None

        return scoreboard, result, who_played_what


    @app.callback(Output('save-output-container-button', 'children'),
                  [Input('save-button', 'n_clicks')])
    def save_game(n_clicks):
        # pickle players if clicked
        if n_clicks > 0:
            with open('players.pickle', 'wb') as f:
                pickle.dump((player1, player2), f)
            return 'Game saved'


    @app.callback(Output('load-output-container-button', 'children'),
                  [Input('load-button', 'n_clicks')])
    def load_game(n_clicks):
        # load players if clicked
        if n_clicks > 0:
            with open('players.pickle', 'rb') as f:
                player1, player2 = pickle.load(f)
            return 'Game loaded. You can continue playing and the names will be refreshed'


    app.run_server(debug=True)
