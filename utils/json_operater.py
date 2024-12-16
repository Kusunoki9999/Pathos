from pathlib import Path
import json

JSON_FILE_PATH = "form_data.json"

def save_to_json(data):
    try:
        if Path(JSON_FILE_PATH).exists():
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.append(data)

        with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data to JSON: {e}")