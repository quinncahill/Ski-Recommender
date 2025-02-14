from flask import Flask, render_template, request, jsonify
from DataGathering import get_ski_resorts_with_scores

app = Flask(__name__)

ski_resorts = get_ski_resorts_with_scores()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/resorts')
def get_resorts():
    resorts = get_ski_resorts_with_scores()
    # Extract only the name and score for each resort
    filtered_resorts = [{"name": resort["name"], "score": resort.get("score", "N/A")} for resort in resorts]
    return jsonify(filtered_resorts)  # Sends only name and score to the frontend

if __name__ == "__main__":
    app.run(debug=True)
