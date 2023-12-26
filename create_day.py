import argparse
import datetime
import re
from pathlib import Path

import requests
import webbrowser


def main():
    today = datetime.date.today()

    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, default=today.day)
    parser.add_argument("--year", type=int, default=today.year)
    args = parser.parse_args()

    assumed_day_dir = Path(f"{args.year}/day_{args.day:0>2d}")

    if args.year == today.year and (today.month != 12 or today.day not in range(1, 26)):
        given = input("Not currently in AoC period.\nEnter DAY YEAR or re-run with args: ")
        day, year = [int(p) for p in given.split(" ")]
    elif assumed_day_dir.exists():
        given = input("Looks like today already exists.\nEnter DAY YEAR or re-run with args: ")
        day, year = [int(p) for p in given.split(" ")]
    else:
        day, year = args.day, args.year

    day_dir = Path(f"{year}/day_{day:0>2d}")
    try:
        day_dir.mkdir(exist_ok=False, parents=True)
    except FileExistsError:
        print("Day dir already exists, exiting.")
        exit()

    day_url = f"https://adventofcode.com/{year}/day/{day}"

    template_path = Path("day_template.py")
    day_script_path = day_dir / f"day_{day:0>2d}.py"
    with open(day_script_path, "w") as out_stream:
        with open(template_path, "r") as in_stream:
            template_text = in_stream.read()
            template_text = template_text.replace("{DAY_LINK}", day_url)
            out_stream.write(template_text)

    input_url = day_url + "/input"
    with open("session_token.txt", "r") as fh:
        token = fh.read().strip()

    input_text = requests.get(input_url, cookies={'session': token}, verify=False).text

    day_input_path = day_dir / "input.txt"
    with open(day_input_path, "w") as fh:
        fh.write(input_text)

    day_test_input_path = day_dir / "test_input.txt"
    day_page_raw = requests.get(day_url, verify=False).text
    code_blocks = re.findall(r"(?<=<code>).*?(?=</code>)", day_page_raw, flags=re.DOTALL)
    test_input = ""
    for c in code_blocks:
        if c.count("\n") > 4:
            test_input = c
            break
    with open(day_test_input_path, "w") as fh:
        fh.write(test_input)

    webbrowser.open(day_url)


if __name__ == "__main__":
    main()
