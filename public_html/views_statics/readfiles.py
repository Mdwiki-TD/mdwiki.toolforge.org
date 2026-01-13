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

views_by_year_path = Path(__file__).parent.parent / "update_med_views" / "views_by_year"
languages_counts_by_year_path = Path(__file__).parent.parent / "languages_counts_by_year.json"

languages_counts_by_year_data = {
    "ab": {
        "2024": 0,
        "2025": 0
    }
}


def dump_final_data():
    with open(languages_counts_by_year_path, "w", encoding="utf-8") as f:
        json.dump(languages_counts_by_year_data, f, ensure_ascii=False, indent=4)
    print(f"Dumped final data to {languages_counts_by_year_path}")


@functools.lru_cache(maxsize=None)
def create_year_folder(year: str):
    year_folder = views_by_year_path / year
    year_folder.mkdir(parents=True, exist_ok=True)
    return year_folder


def start():
    ...


if __name__ == "__main__":
    start()
