"""

"""
from pathlib import Path
import json
from tqdm import tqdm
from collections import defaultdict

# Path definitions
base_path = Path(__file__).parent / "update_med_views"
views_by_year_path = base_path / "views_by_year"

# To store summary counts
languages_counts_by_year_data = defaultdict(lambda: defaultdict(int))


def dump_final_data():
    years_data = {}
    for lang, years in languages_counts_by_year_data.items():
        for year, count in years.items():
            years_data.setdefault(year, {})[lang] = count

    for year, lang_counts in years_data.items():
        # sort lang_counts DESC by count
        lang_counts = dict(sorted(lang_counts.items(), key=lambda item: item[1], reverse=True))
        year_file = views_by_year_path / f"{year}_languages_counts.json"
        with open(year_file, "w", encoding="utf-8") as f:
            json.dump(lang_counts, f, ensure_ascii=False, indent=4)
        print(f"Dumped year data to {year_file}")


def start() -> None:
    years_paths = [p for p in views_by_year_path.glob("*/") if p.is_dir()]
    for year_path in tqdm(years_paths, desc="Processing years"):
        year = year_path.name
        # Process each json file in the source directory
        for file_path in year_path.glob("*.json"):
            lang = file_path.stem

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    continue

            languages_counts_by_year_data[lang][year] = sum(data.values())

    dump_final_data()


if __name__ == "__main__":
    start()
