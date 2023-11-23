import argparse
import datetime
from pathlib import Path

import requests
import webbrowser


def main():
    today = datetime.date.today()
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, default=today.day)
    parser.add_argument("--year", type=int, default=today.year)
    args = parser.parse_args()

    day_dir = Path(f"{args.year}/day_{args.day:0>2d}")
    try:
        day_dir.mkdir(exist_ok=False, parents=True)
    except FileExistsError:
        print("Day dir already exists, exiting.")
        exit()

    template_path = Path("day_template.py")
    day_script_path = day_dir / f"day_{args.day:0>2d}.py"
    day_script_path.write_bytes(template_path.read_bytes())

    day_url = f"https://adventofcode.com/{args.year}/day/{args.day}"
    input_url = day_url + "/input"
    with open("session_token.txt", "r") as fh:
        token = fh.read().strip()

    input_text = requests.get(input_url, cookies={'session': token}, verify=False).text

    day_input_path = day_dir / "input.txt"
    with open(day_input_path, "w") as fh:
        fh.write(input_text)

    webbrowser.open(day_url)


if __name__ == "__main__":
    main()
