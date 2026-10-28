
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import gf2m4
import gf2m8


def run_full(field, f, g, m):
    cmd = [
        sys.executable, str(ROOT / "run.py"),
        "--field", str(field),
        "--f", f,
        "--g", g,
        "--m", m
    ]

    p = subprocess.run(cmd, capture_output=True, text=True)

    for line in p.stdout.splitlines():
        if line.startswith("Nhi phan:"):
            return int(line.split(":")[1].strip(), 2)

    return None


def test_benchmark():
    path = Path(__file__).parent / "benchmark.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    passed = 0
    total = 0

    for field, module in [(4, gf2m4), (8, gf2m8)]:
        print(f"\nKiem traGF(2^{field})")

        for name, keys in [
            ("xor", ("a", "b")),
            ("xtime", ("g", "m")),
            ("multiply", ("f", "g", "m"))
        ]:
            for case in data[f"gf{field}"][name]:
                args = [
                    int(case[k], 16 if k == "m" else 2)
                    for k in keys
                ]

                actual = getattr(module, name)(*args)
                expected = int(case["expected"], 2)

                ok = actual == expected
                print(f"kiem tra {name}{tuple(args)} -> {ok}")

                passed += ok
                total += 1

    print("\nKiem tra toan bo chuong trinh")

    for case in data["cli"]:
        actual = run_full(
            case["field"],
            case["f"],
            case["g"],
            case["m"]
        )

        expected = int(case["expected"], 2)
        ok = actual == expected

        print(f"kiem tra full GF(2^{case['field']}) -> {ok}")

        passed += ok
        total += 1

    print(f"\nTong ket: {passed}/{total} dung")


def test_custom():
    field = int(input("GF(2^4) hay GF(2^8)? (4/8): "))
    module = gf2m4 if field == 4 else gf2m8

    name = input("Ham (xor/xtime/multiply/full): ").strip()

    if name == "xor":
        a = int(input("a (binary): "), 2)
        b = int(input("b (binary): "), 2)
        actual = module.xor(a, b)

    else:
        if name == "xtime":
            g = int(input("g (binary): "), 2)
        else:
            f = int(input("f (binary): "), 2)
            g = int(input("g (binary): "), 2)

        m = int(input("m (hex): "), 16)

        if name == "xtime":
            actual = module.xtime(g, m)

        elif name == "multiply":
            actual = module.multiply(f, g, m)

        else:
            actual = run_full(
                field,
                format(f, f"0{field}b"),
                format(g, f"0{field}b"),
                hex(m)
            )

    expected = int(input("Dap an dung (binary): "), 2)

    print(f"\nkiem tra {name} -> {actual == expected}")

    if actual is not None:
        print(f"Ket qua thuc te: {actual:0{field}b}")


if __name__ == "__main__":
    if "--custom" in sys.argv:
        test_custom()
    else:
        test_benchmark()
