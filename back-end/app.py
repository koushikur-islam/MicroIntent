from flask import Flask, jsonify, request
from flask_cors import CORS
import placement_generator
import json

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

@app.route('/api/placement', methods=['GET', 'POST', 'OPTIONS'])

def placement():
    if request.method == 'OPTIONS':
        return '', 204
    if request.method == 'POST':
        data = request.get_json() or {}
        infrastructure_description = data.get('infrastructureDescription')
        intents = data.get('intents')
        if infrastructure_description and intents:
            placement_strategy = placement_generator.generate_placement_strategy(intents, infrastructure_description)
            # print(json.dumps(placement_strategy, indent=4))
        return jsonify({'data': placement_strategy})
    return jsonify({'data': 'Invalid request!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)