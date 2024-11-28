from flask import Flask, render_template, request, jsonify, session
from game_logic import TicTacToe

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    if 'game' not in session:
        session['game'] = TicTacToe().__dict__
    game = TicTacToe()
    game.__dict__ = session['game']
    
    enumerated_board = [[(i, j, cell) for j, cell in enumerate(row)] for i, row in enumerate(game.board)]
    return render_template(
        'index.html',
        board=enumerated_board,
        player_score=game.player_score,
        ai_score=game.ai_score,
        winner=game.winner
    )

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    row, col = data['row'], data['col']
    
    game = TicTacToe()
    game.__dict__ = session['game']
    
    game.make_move(row, col)
    
    if not game.winner and not game.is_board_full():
        game.ai_move()
    
    if not game.winner and game.is_board_full():
        game.winner = 'Draw'
    
    session['game'] = game.__dict__
    
    enumerated_board = [[(i, j, cell) for j, cell in enumerate(row)] for i, row in enumerate(game.board)]
    return jsonify({
        'board': enumerated_board,
        'winner': game.winner,
        'player_score': game.player_score,
        'ai_score': game.ai_score
    })

@app.route('/reset', methods=['POST'])
def reset():
    game = TicTacToe()
    game.__dict__ = session['game']
    game.reset_game()
    session['game'] = game.__dict__
    
    enumerated_board = [[(i, j, cell) for j, cell in enumerate(row)] for i, row in enumerate(game.board)]
    return jsonify({
        'board': enumerated_board,
        'winner': game.winner,
        'player_score': game.player_score,
        'ai_score': game.ai_score
    })

if __name__ == "__main__":
    app.run(debug=True)
