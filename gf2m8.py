"""Phep nhan trong GF(2^8) tu phep cong XOR va nhan voi x (xtime)."""

BITS = 8
MASK = (1 << BITS) - 1       # 0b11111111: giu 8 bit thap
TOP_BIT = 1 << (BITS - 1)  # 0b10000000: bit he so x^7

# Ca 30 da thuc bat kha quy bac 8 tren GF(2).
MODULI = (
    0x11B, 0x11D, 0x12B, 0x12D, 0x139, 0x13F,
    0x14D, 0x15F, 0x163, 0x165, 0x169, 0x171,
    0x177, 0x17B, 0x187, 0x18B, 0x18D, 0x19F,
    0x1A3, 0x1A9, 0x1B1, 0x1BD, 0x1C3, 0x1CF,
    0x1D7, 0x1DD, 0x1E7, 0x1F3, 0x1F5, 0x1F9,
)
DEFAULT_MODULUS = 0x11B   # x^8 + x^4 + x^3 + x + 1 (AES)


def xor(a: int, b: int) -> int:
    """Cong hai da thuc co he so thuoc GF(2)."""
    return a ^ b


def xtime(g: int, m: int = DEFAULT_MODULUS) -> int:
    """Tra ve (x * g(x)) mod m(x)."""
    if not 0 <= g <= MASK:
        raise ValueError("g phai nam trong khoang 0..255")
    if m not in MODULI:
        raise ValueError("m khong thuoc danh sach da thuc bat kha quy bac 8")

    carry = (g & TOP_BIT) != 0
    shifted = (g << 1) & MASK

    if carry:
        shifted = xor(shifted, m & MASK)

    return shifted


def multiply(f: int, g: int, m: int = DEFAULT_MODULUS,
             show_steps: bool = False) -> int:
    """Tra ve (f(x) * g(x)) mod m(x), su dung xtime va XOR."""
    if not (0 <= f <= MASK and 0 <= g <= MASK):
        raise ValueError("f va g phai nam trong khoang 0..255")
    if m not in MODULI:
        raise ValueError("m khong thuoc danh sach da thuc bat kha quy bac 8")

    result = 0
    term = g   # Ban dau la x^0 * g(x) mod m(x)

    if show_steps:
        print("\ni | bit f_i | x^i*g mod m | result sau XOR")
        print("--+---------+-------------+----------------")

    for i in range(BITS):
        bit = (f >> i) & 1
        if bit:
            result = xor(result, term)

        if show_steps:
            print(f"{i} |    {bit}    |   {term:08b}  |    {result:08b}")

        if i < BITS - 1:
            term = xtime(term, m)

    return result
