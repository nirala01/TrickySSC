"""Official key per global Q number (1-90) from the shift's source JSON. MTS 2025 order:
Q1-20 Maths, Q21-40 Reasoning, Q41-65 GA, Q66-90 English."""
import json, os
OFF = (('MATH', 0), ('REAS', 20), ('GK', 40), ('ENG', 65))


def load(src):
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', src + '.json')
    d = json.load(open(p, encoding='utf-8'))
    out = {}
    for s, off in OFF:
        for n in range(1, 26):
            x = d.get(f'{s}|{n}')
            if x: out[off + n] = x
    assert sorted(out) == list(range(1, 91)), sorted(out)[:5]
    return out


def keys(src):
    return {n: 'ABCD'[int(x['correct']) - 1] for n, x in load(src).items()}
