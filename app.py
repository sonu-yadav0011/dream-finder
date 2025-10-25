from flask import Flask, render_template, request
from cs50 import SQL

app = Flask(__name__)

# Connect to database
db = SQL("sqlite:///roadmaps.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    field = request.form.get("field").lower()

    # Fetch roadmap data for the field
    roadmap = db.execute("SELECT * FROM roadmaps WHERE field = ?", field)

    if not roadmap:
        return render_template("roadmap.html", error="No roadmap found for that field.")

    return render_template("roadmap.html", roadmap=roadmap, field=field.title())

if __name__ == "__main__":
    app.run(debug=True)
