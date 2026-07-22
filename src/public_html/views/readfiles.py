"""
read all json files in `update_med_views/views_new/all`

example of `update_med_views/views_new/all/ab.json` file:

{"Аџьар Ҟаԥшь": { "2021": 672, "2022": 1548, "2023": 2365, "2024": 1136, "2025": 549, "all": 6270 }, "Иҳәаадоу аҳақьымцәа": { "2017": 85, "2018": 319, "2019": 680, "2020": 763, "2021": 567, "2022": 838, "2023": 1135, "2024": 1019, "2025": 444, "all": 5850 },}

- for each year create folder in views_by_year_path

- for each json file create a new json file in each year folder with only titles that have views for that year,
    - the new json file should have the same name as the original file
    - example:
        - file: views_by_year_path/2021/ab.json
        - content: { "Аџьар Ҟаԥшь": 672, "Иҳәаадоу аҳақьымцәа": 85 }
- also create languages_counts_by_year.json file that contains number of titles with views for each language for each year
    - example:
        {
            "ab": {
                "2021": 2,
                "2022": 3,
                "2023": 4,
                "2024": 1,
                "2025": 0
            }
        }
"""
import functools
from pathlib import Path
import json
from collections import defaultdict

# Path definitions
base_path = Path(__file__).parent / "update_med_views"
source_path = base_path / "views_new" / "all"
views_by_year_path = base_path / "views_by_year_all_agents"

# To store summary counts
languages_titles_by_year_data = defaultdict(lambda: defaultdict(int))
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


@functools.lru_cache(maxsize=None)
def create_year_folder(year: str):
    year_folder = views_by_year_path / year
    year_folder.mkdir(parents=True, exist_ok=True)
    return year_folder


def start() -> None:
    if not source_path.exists():
        print(f"Source path {source_path} does not exist.")
        return

    # Process each json file in the source directory
    for file_path in source_path.glob("*.json"):
        lang = file_path.stem
        print(f"Processing {lang}...")

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue

        # Dictionary to hold year-specific data for this file
        # Format: { "2021": { "Title": 123 }, "2022": { ... } }
        year_split_data = defaultdict(dict)

        for title, views_dict in data.items():
            for key, count in views_dict.items():
                if key == "all" or not key.isdigit():
                    continue
                year = key

                if year == "2025":
                    continue  # Skip year 2025 as per instructions

                if count > 0:
                    year_split_data[year][title] = count
                    languages_counts_by_year_data[lang][year] += count
                    languages_titles_by_year_data[lang][year] += 1

        # Save the split files
        for year, titles_data in year_split_data.items():
            year_dir = create_year_folder(year)
            output_file = year_dir / f"{lang}.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(titles_data, f, ensure_ascii=False, indent=4)

    dump_final_data()


if __name__ == "__main__":
    start()
