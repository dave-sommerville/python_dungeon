from flask import Flask, request, jsonify, render_template
from game_engine.game_engine import GameEngine
from game_engine.locations.dungeon import Dungeon
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

if __name__ == '__main__':
    app.run(debug=True)