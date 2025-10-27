from flask import Flask, render_template, request, redirect, url_for
from cs50 import SQL
import json  # To handle JSON strings stored in the database

app = Flask(__name__)

# Connect to database using cs50.SQL
# Ensure 'roadmaps.db' is the correct name of your SQLite database file
db = SQL("sqlite:///roadmaps.db")


@app.route("/")
def index():
    # You might want to fetch some popular fields here for your homepage if you have them
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    field_name = request.form.get("field")
    if field_name:
        # normalize for URL (lowercase) but preserve original for display later
        return redirect(url_for("show_roadmap", field_name=field_name.lower()))
    return redirect(url_for("index"))


@app.route("/roadmap/<field_name>")
def show_roadmap(field_name):
    # Try to find the field in the 'fields' table (expects columns: field_id, field_name)
    field_info = db.execute(
        "SELECT field_id, field_name FROM fields WHERE lower(field_name) = ?",
        field_name.lower()
    )

    if not field_info:
        # Field not found — render roadmap.html with an error message
        return render_template(
            "roadmap.html",
            field_name=field_name.title(),
            roadmap_data=[],
            error="No roadmap found for that field."
        )

    field_id = field_info[0]["field_id"]
    field_display_name = field_info[0]["field_name"].title()

    # Fetch levels for this field ordered by order_no (expects levels table with level_id, level_name, about, topics, languages, resources_summary, order_no, field_id)
    levels_data_raw = db.execute(
        "SELECT * FROM levels WHERE field_id = ? ORDER BY order_no",
        field_id
    )

    roadmap_data = []
    for level_row in levels_data_raw:
        level_id = level_row.get("level_id")

        # Fetch specific resources for the current level (expects resources table with resource_name, resource_link, level_id)
        specific_resources = db.execute(
            "SELECT resource_name, resource_link FROM resources WHERE level_id = ?",
            level_id
        )

        # Parse JSON strings back into Python objects (lists). Be defensive in case of NULL/empty or invalid JSON.
        def parse_json_field(value):
            if not value:
                return []
            try:
                return json.loads(value)
            except (ValueError, TypeError):
                return []

        topics = parse_json_field(level_row.get("topics"))
        languages = parse_json_field(level_row.get("languages"))
        resources_summary = parse_json_field(level_row.get("resources_summary"))

        roadmap_data.append({
            "level_name": level_row.get("level_name"),
            "about": level_row.get("about"),
            "topics": topics,
            "languages": languages,
            "resources_summary": resources_summary,
            "specific_resources": specific_resources
        })

    return render_template(
        "roadmap.html",
        field_name=field_display_name,
        roadmap_data=roadmap_data
    )


if __name__ == "__main__":
    app.run(debug=True)
