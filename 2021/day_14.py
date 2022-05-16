from typing import Dict
from collections import Counter
from functools import cache

test_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

data = """BNBBNCFHHKOSCHBKKSHN

CH -> S
KK -> V
FS -> V
CN -> P
VC -> N
CB -> V
VK -> H
CF -> N
PO -> O
KC -> S
HC -> P
PP -> B
KO -> B
BK -> P
BH -> N
CC -> N
PC -> O
FK -> N
KF -> F
FH -> S
SS -> V
ON -> K
OV -> K
NK -> H
BO -> C
VP -> O
CS -> V
KS -> K
SK -> B
OP -> S
PK -> S
HF -> P
SV -> P
SB -> C
BC -> C
FP -> H
FC -> P
PB -> N
NV -> F
VO -> F
VH -> P
BB -> N
SF -> F
NB -> K
KB -> S
VV -> S
NP -> N
SO -> O
PN -> B
BP -> H
BV -> V
OB -> C
HV -> N
PF -> B
SP -> N
HN -> N
CV -> H
BN -> V
PS -> V
CO -> S
BS -> N
VB -> H
PV -> P
NN -> P
HS -> C
OS -> P
FB -> S
HO -> C
KH -> H
HB -> K
VF -> S
CK -> K
FF -> H
FN -> P
OK -> F
SC -> B
HH -> N
OH -> O
VS -> N
FO -> N
OC -> H
NF -> F
PH -> S
HK -> K
NH -> H
FV -> S
OF -> V
NC -> O
HP -> O
KP -> B
BF -> N
NO -> S
CP -> C
NS -> N
VN -> K
KV -> N
OO -> V
SN -> O
KN -> C
SH -> F"""

transforms: Dict[str, str] = {}


@cache
def expand(a, b, depth=40):
    global transforms
    if depth == 0:
        return Counter()

    x = transforms[a+b]

    return Counter(x) + expand(a, x, depth-1) + expand(x, b, depth-1)


def main():
    global data, transforms

    template, transform_lines = data.split("\n\n")
    transforms = dict(line.split(" -> ") for line in transform_lines.split("\n"))

    #elements = ""
    #for t in transforms:
    #    for c in t:
    #        if c not in elements:
    #            elements += c
    #    for c in transforms[t]:
    #        if c not in elements:
    #            elements += c
    #print(f"{elements=}")

    counts = Counter(template)
    for i in range(1, len(template)):
        if template[i-1: i+1] in transforms:
            counts += expand(template[i-1], template[i])
    print(counts)
    print(max(counts.values()) - min(counts.values()))

    #c = sum(map(expand, template, template[1:]), Counter(template))
    #print(max(c.values()) - min(c.values()))

    #print(0, ":", len(template))

    #for step_no in range(40):
    #    new_string = template[0]
    #    for i in range(1, len(template)):
    #        if template[i-1: i+1] in transforms:
    #            new_string += transforms[template[i-1: i+1]]
    #        new_string += template[i]
    #    template = new_string
    #    print(step_no+1, ":", len(template))

    #element_counts = list(sorted([[e, template.count(e)] for e in elements], key=lambda x: x[1], reverse=True))
    #for e, count in element_counts:
    #    print(e, ":", count)
    #print(f"Answer: {counts[0][1] - counts[-1][1]}")


if __name__ == '__main__':
    main()
