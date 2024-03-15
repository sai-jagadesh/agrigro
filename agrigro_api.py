from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load crop data from JSON file
with open('intents.json') as file:
    data = json.load(file)

# Route to get all crops
@app.route('/crops', methods=['GET'])
def get_crops():
    crops = data['intents'][1]['patterns']
    return jsonify({"crops": crops})
	
def get_crops_by_season(season):
    crops_by_season = [crop for crop in data['crops'] if crop['season'] == season]
    return jsonify({"crops": crops_by_season})

if __name__ == '__main__':
    app.run(debug=True)
