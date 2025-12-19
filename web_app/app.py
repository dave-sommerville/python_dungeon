from flask import Flask, request, jsonify, render_template
from ..game_engine.engine import GameEngine
from ..game_engine.locations.dungeon import Dungeon
# Import your other classes...

app = Flask(__name__)
engine = GameEngine()
dungeon = Dungeon()

@app.route('/action', methods=['POST'])
def handle_action():
    data = request.json
    user_input = data.get("action", "").lower()
    
    # Process logic and get the state packet
    response_data = engine.resolve_action(dungeon, user_input)
    
    return jsonify(response_data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    """Reinitialize the in-memory engine and dungeon state.

    Optional POST JSON: { "user_id": "..." } (not implemented yet)
    Returns the same response shape as `/action` with initial describe output.
    """
    global engine, dungeon

    # Create fresh game state (in future, load by user_id)
    engine = GameEngine()
    dungeon = Dungeon()

    # Return an initial describe packet so the client has logs and menu
    response_data = engine.resolve_action(dungeon, 'describe')
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)