# DreamFinder  
*A Lightweight Flask Web Application for Exploring Learning Roadmaps*

DreamFinder is a simple yet powerful web application designed to help learners explore learning roadmaps for different fields of study. Whether someone is interested in computer science, cybersecurity, data science, or any other discipline, DreamFinder provides a visual, structured path outlining what to learn, in what order, and with links to helpful resources. The intent is to make navigating complex fields easier by breaking them down into digestible, progressive learning stages.

This project was developed using **Flask**, **SQLite**, and basic web technologies. Its design emphasizes clarity, usability, and extendability. While lightweight, it is structured so future contributors can easily add new fields, levels, and resources.

---

## Features

- **Searchable Homepage**  
  Users can type any field of interest into a search bar. If a roadmap for the field already exists in the database, the app displays it. This encourages exploration and curiosity while keeping the interface minimal and easy to understand.

- **Roadmap Visualization Page**  
  Roadmaps are shown as ordered learning levels. Each level contains descriptions, topics to explore, programming languages or tools to learn, and resource summaries. This offers clarity on what to learn step-by-step.

- **Extendable Data Structure**  
  Data is stored in a clean SQLite schema. Topics, tools, and summaries are stored as JSON arrays, making the app flexible, compact, and easy to update.

---

## Requirements

The application runs on most systems, but the environment below was tested on **Windows 10+**.

### Software Requirements
- Python 3.8+
- pip
- SQLite3
- (Recommended) Virtual Environment: `venv` or `pipenv`

### Required Python Libraries
| Package | Usage |
|--------|--------|
| Flask | Handles web server and routing |
| cs50 | Database convenience helper (optional; may use `sqlite3`) |

To export dependencies:
```
pip freeze > requirements.txt
```

---

## Quick Start (Windows)

1. **Navigate to the project folder:**
```powershell
cd path\to\project
```

2. **Create and activate a virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install flask cs50
```

4. **Ensure the SQLite database exists**  
   If it does not, create it using the SQL commands below.

5. **Run the application:**
```powershell
python app.py
```

6. **Open in browser:**
```
http://139.0.0.1:5000
```

---

## Database Schema

DreamFinder stores data across **three tables**:

| Table | Purpose |
|------|---------|
| `fields` | Defines each learning field |
| `levels` | Defines sequential learning levels per field |
| `resources` | Stores external resource links |

### Schema Definition

```sql
CREATE TABLE IF NOT EXISTS fields (
  field_id INTEGER PRIMARY KEY AUTOINCREMENT,
  field_name TEXT NOT NULL UNIQUE,
  about TEXT
);

CREATE TABLE IF NOT EXISTS levels (
  level_id INTEGER PRIMARY KEY AUTOINCREMENT,
  field_id INTEGER NOT NULL,
  order_no INTEGER,
  level_name TEXT,
  about TEXT,
  topics TEXT,
  languages TEXT,
  resources_summary TEXT,
  FOREIGN KEY(field_id) REFERENCES fields(field_id)
);

CREATE TABLE IF NOT EXISTS resources (
  resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
  level_id INTEGER NOT NULL,
  resource_name TEXT,
  resource_link TEXT,
  FOREIGN KEY(level_id) REFERENCES levels(level_id)
);
```

### Sample Data

```sql
INSERT INTO fields (field_name, about)
VALUES ('computer science', 'Core CS fundamentals');

INSERT INTO levels (field_id, order_no, level_name, about, topics, languages, resources_summary)
VALUES (
  1, 1, 'Programming Fundamentals', 'Basic programming concepts',
  '["Variables","Control Flow","Functions","Data Structures"]',
  '["Python","C"]',
  '["Intro courses","Practice problems"]'
);

INSERT INTO resources (level_id, resource_name, resource_link) VALUES
(1, 'CS50', 'https://cs50.harvard.edu/x/'),
(1, 'freeCodeCamp', 'https://www.freecodecamp.org/');
```

---

## File Structure

```
project/
│ app.py
│ roadmaps.db
│ requirements.txt (optional)
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   └── roadmap.html
│
└── static/
    ├── styles.css
    └── roadmap.css (optional)
```

---

## Troubleshooting

| Issue | Solution |
|------|----------|
| Roadmap page JSON decode error | Ensure topics/languages/resources_summary are valid JSON (`["item1","item2"]`) |
| CSS not displaying | Confirm correct static path in templates |
| Field not appearing in search | Ensure spelling matches database entry exactly |

---

If you would like, I can also:
- Add an **auto database setup script**
- Create sample roadmap data for multiple subjects
- Help format this for CS50 final submission standards

Just let me know!
