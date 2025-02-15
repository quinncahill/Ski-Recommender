from flask import Flask, render_template, request, jsonify
from DataGathering import get_ski_resorts_with_scores

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/resorts')
def get_resorts():
    resorts_1 = get_ski_resorts_with_scores(1)
    resorts_2 = get_ski_resorts_with_scores(2)

    # Combine both results into a single list with scores from both calls
    merged_resorts = []
    for r1, r2 in zip(resorts_1, resorts_2):
        merged_resorts.append({
            "name": r1["name"],
            "Current Score:": r1.get("score_1", "N/A"),
            "Next Time Section Score": r2.get("score_2", "N/A")
        })

    return jsonify(merged_resorts)  # Sends merged data to frontend

if __name__ == "__main__":
    app.run(debug=True)
