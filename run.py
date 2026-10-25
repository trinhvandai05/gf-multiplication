"""CLI cho GF(2^4) va GF(2^8).

Vi du:
    python run.py --field 4 --f 1011 --g 0110 --steps
    python run.py --field 8 --f 01010111 --g 10000011 --steps
    python run.py --field 4 --f 1011 --g 0101 --m 0x19
    python run.py --field 8 --list-moduli
    python run.py --compile --field 4 --f 1011 --g 0110
"""

import argparse
from pathlib import Path
import py_compile

import gf2m4
import gf2m8


def polynomial(value: int) -> str:
    """Doi bieu dien so nguyen sang da thuc co he so 0/1."""
    terms = []
    for degree in range(value.bit_length() - 1, -1, -1):
        if value & (1 << degree):
            if degree == 0:
                terms.append("1")
            elif degree == 1:
                terms.append("x")
            else:
                terms.append(f"x^{degree}")
    return " + ".join(terms) if terms else "0"


def parse_binary(raw: str, bits: int, name: str) -> int:
    """Nhan chuoi nhi phan, co the them tien to 0b."""
    text = raw.removeprefix("0b").removeprefix("0B")
    if not text or any(c not in "01" for c in text):
        raise ValueError(f"{name} phai la chuoi nhi phan (vi du: 1011)")

    value = int(text, 2)
    if value >= (1 << bits):
        raise ValueError(f"{name} vuot qua {bits} bit cua truong GF(2^{bits})")
    return value


def show_output(field_bits: int, f: int, g: int, m: int,
                result: int) -> None:
    print(f"\n=== GF(2^{field_bits}) ===")
    print(f"m(x) = {polynomial(m)} (0x{m:X})")
    print(f"f(x) = {polynomial(f)} ({f:0{field_bits}b})")
    print(f"g(x) = {polynomial(g)} ({g:0{field_bits}b})")
    print(f"h(x) = f(x)*g(x) mod m(x) = {polynomial(result)}")
    print(f"Nhi phan: {result:0{field_bits}b}")
    print(f"Hex: 0x{result:X}")
    print(f"Thap phan: {result}")


def run_gf4(f_bits: str, g_bits: str, m: int = gf2m4.DEFAULT_MODULUS,
            steps: bool = False) -> int:
    """Nhan hai phan tu trong GF(2^4), nhan dau vao dang chuoi bit."""
    f = parse_binary(f_bits, gf2m4.BITS, "f")
    g = parse_binary(g_bits, gf2m4.BITS, "g")
    result = gf2m4.multiply(f, g, m, show_steps=steps)
    show_output(4, f, g, m, result)
    return result


def run_gf8(f_bits: str, g_bits: str, m: int = gf2m8.DEFAULT_MODULUS,
            steps: bool = False) -> int:
    """Nhan hai phan tu trong GF(2^8), nhan dau vao dang chuoi bit."""
    f = parse_binary(f_bits, gf2m8.BITS, "f")
    g = parse_binary(g_bits, gf2m8.BITS, "g")
    result = gf2m8.multiply(f, g, m, show_steps=steps)
    show_output(8, f, g, m, result)
    return result


def compile_sources() -> None:
    """Kiem tra cu phap va tao bytecode .pyc; Python khong can file .exe."""
    folder = Path(__file__).resolve().parent
    for filename in ("gf2m4.py", "gf2m8.py", "run.py"):
        py_compile.compile(str(folder / filename), doraise=True)
        print(f"Compiled: {filename}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Nhan hai da thuc trong GF(2^4) hoac GF(2^8)"
    )
    parser.add_argument("--field", type=int, choices=(4, 8), default=4,
                        help="Chon 4 hoac 8 (mac dinh: 4)")
    parser.add_argument("--f", help="Da thuc f dang bit, vi du 1011")
    parser.add_argument("--g", help="Da thuc g dang bit, vi du 0110")
    parser.add_argument("--m", type=lambda s: int(s, 0),
                        help="Da thuc bat kha quy, vi du 0x13 hoac 0x11B")
    parser.add_argument("--steps", action="store_true",
                        help="In ra cac vong lap trong phep nhan")
    parser.add_argument("--list-moduli", action="store_true",
                        help="Liet ke cac da thuc bat kha quy duoc ho tro")
    parser.add_argument("--compile", action="store_true",
                        help="Kiem tra cu phap truoc khi chay")
    args = parser.parse_args()

    try:
        if args.compile:
            compile_sources()
            if args.f is None and args.g is None and not args.list_moduli:
                return

        module = gf2m4 if args.field == 4 else gf2m8
        if args.list_moduli:
            print(f"Cac da thuc bat kha quy bac {args.field}:")
            for m in module.MODULI:
                print(f"  0x{m:X} : {polynomial(m)}")
            return

        if args.f is None or args.g is None:
            parser.error("Can cung cap ca --f va --g (dang nhi phan)")

        m = args.m if args.m is not None else module.DEFAULT_MODULUS
        if args.field == 4:
            run_gf4(args.f, args.g, m, args.steps)
        else:
            run_gf8(args.f, args.g, m, args.steps)
    except (ValueError, py_compile.PyCompileError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
