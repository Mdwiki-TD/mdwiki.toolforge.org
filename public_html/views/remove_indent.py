"""

"""
from pathlib import Path
import json

# Path definitions
base_path = Path(__file__).parent / "update_med_views"
for file_path in base_path.rglob("*.json"):
    print(f"Processing file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Write the updated data back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
