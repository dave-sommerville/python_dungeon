from flask import Flask, request, jsonify
from game_engine import GameEngine
# Import your other classes...

app = Flask(__name__)
engine = GameEngine()
dungeon = Dungeon() # In a real app, you'd load this from a database/session

@app.route('/action', methods=['POST'])
def handle_action():
    data = request.json
    user_input = data.get("action", "").lower()
    
    # Process logic and get the state packet
    response_data = engine.resolve_action(dungeon, user_input)
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)