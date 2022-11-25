import re

pattern_parts = []
for _i in range(26):
    pattern_parts.append(chr(65 + _i) + chr(97 + _i))
    pattern_parts.append(chr(97 + _i) + chr(65 + _i))
pattern = "|".join(pattern_parts)


def collapse(mol):
    global pattern
    done = False
    while not done:
        done = True
        start_len = len(mol)
        mol = re.sub(pattern, "", mol)
        done = len(mol) == start_len
    return mol


def part_1():
    with open("input.txt", "r") as fh:
        mol = fh.read().strip()

    print("Starting Length:", len(mol))
    mol = collapse(mol)
    print("Ending Length:", len(mol))


def part_2():
    with open("input.txt", "r") as fh:
        mol = fh.read().strip()

    best_len = len(mol)
    best_char = "a"

    for i in range(26):
        test_mol = mol
        test_mol = test_mol.replace(chr(65 + i), "")
        test_mol = test_mol.replace(chr(97 + i), "")
        test_mol = collapse(test_mol)
        if len(test_mol) < best_len:
            best_len = len(test_mol)
            best_char = chr(65 + i)

    print(best_len)
    print(best_char)


if __name__ == '__main__':
    part_2()

