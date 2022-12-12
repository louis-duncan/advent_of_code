import json
import re


def valgo_height(x):
    match = re.findall(r"^(\d.*)(cm|in)$", x)
    if len(match) == 0:
        return False
    else:
        match = match[0]
        if match[1] == "cm":
            return 150 <= int(match[0]) <= 193
        elif match[1] == "in":
            return 59 <= int(match[0]) <= 76
        else:
            raise ValueError


field_reqs = {
    'byr': lambda x: (len(x) == 4) and (1920 <= int(x) <= 2002),
    'iyr': lambda x: (len(x) == 4) and (2010 <= int(x) <= 2020),
    'eyr': lambda x: (len(x) == 4) and (2020 <= int(x) <= 2030),
    'hgt': valgo_height,
    'hcl': lambda x: bool(re.match(r"^#[0-9,a-f]{6}$", x)),
    'ecl': lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
    'pid': lambda x: bool(re.match(r"^[0-9]{9}$", x)),
    'cid': lambda x: True
}


def main():
    with open("input.txt", "r") as fh:
        passports = []
        for seg in fh.read().split("\n\n"):
            parts = [part.split(":") for part in seg.split()]
            new = {
                'valid': True,
                'reason': ""
            }
            for k, v in parts:
                if k in new:
                    new['valid'] = False
                    new['reason'] = f"Duplicate value {k}"
                else:
                    new[k] = v
            passports.append(new.copy())

    count = 0
    for p in passports:
        if p['valid']:
            for rk, valgo in field_reqs.items():
                try:
                    field_valid = valgo(p.get(rk, ""))
                    if not field_valid:
                        p['valid'] = False
                        p['reason'] = f"Invalid value for field '{rk}'"

                except ValueError:
                    p['valid'] = False
                    p['reason'] = f"Invalid value for field '{rk}'"

                if not p['valid']:
                    break

        count += p['valid']

    with open("results.json", "w") as fh:
        json.dump(passports, fh)

    print(count)


if __name__ == '__main__':
    main()
