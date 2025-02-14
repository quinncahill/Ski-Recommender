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
    return jsonify(resorts)  # Converts the list to JSON for the frontend

if __name__ == "__main__":
    app.run(debug=True)
